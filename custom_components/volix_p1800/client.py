"""Bluetooth client for the VOLIX P1800."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import logging

from bleak.backends.device import BLEDevice
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from .const import NOTIFY_UUID, STATUS_REQUEST, WRITE_UUID
from .protocol import ProtocolError, SettingsData, StatusData, parse_settings, parse_status

_LOGGER = logging.getLogger(__name__)


class VolixClient:
    """Maintain one safe BLE session and decode station notifications."""

    def __init__(self, device: BLEDevice, name: str) -> None:
        self.device = device
        self.name = name
        self.status: StatusData | None = None
        self.settings: SettingsData | None = None
        self._client: BleakClientWithServiceCache | None = None
        self._packet_event = asyncio.Event()
        self._disconnect_callback: Callable[[], None] | None = None

    @property
    def connected(self) -> bool:
        return bool(self._client and self._client.is_connected)

    async def connect(self, disconnect_callback: Callable[[], None]) -> None:
        """Connect and subscribe to notifications."""
        self._disconnect_callback = disconnect_callback
        if self.connected:
            return
        self._client = await establish_connection(
            BleakClientWithServiceCache,
            self.device,
            self.name,
            disconnected_callback=lambda _client: disconnect_callback(),
            max_attempts=3,
        )
        await self._client.start_notify(NOTIFY_UUID, self._notification)

    def _notification(self, _sender: object, data: bytearray) -> None:
        packet = bytes(data)
        try:
            if len(packet) > 6 and packet[6] == 0x01:
                self.status = parse_status(packet)
            elif len(packet) > 6 and packet[6] == 0x03:
                self.settings = parse_settings(packet)
            else:
                return
        except ProtocolError as err:
            _LOGGER.debug("Rejected VOLIX packet: %s", err)
            return
        self._packet_event.set()

    async def refresh(self) -> None:
        """Request fresh telemetry and wait briefly for a valid packet."""
        if not self._client:
            raise ConnectionError("not connected")
        self._packet_event.clear()
        await self._client.write_gatt_char(WRITE_UUID, STATUS_REQUEST, response=False)
        try:
            await asyncio.wait_for(self._packet_event.wait(), timeout=10)
        except TimeoutError as err:
            raise ConnectionError("station did not return telemetry") from err

    async def write(self, frame: bytes) -> None:
        """Write one verified station command."""
        if not self._client or not self.connected:
            raise ConnectionError("not connected")
        await self._client.write_gatt_char(WRITE_UUID, frame, response=False)

    async def disconnect(self) -> None:
        """Close the BLE session."""
        if self._client and self._client.is_connected:
            await self._client.disconnect()
        self._client = None
