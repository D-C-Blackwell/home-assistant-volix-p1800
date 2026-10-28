
"""Data coordinator for VOLIX P1800."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .client import VolixClient
from .const import DOMAIN, UPDATE_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class VolixCoordinator(DataUpdateCoordinator[None]):
    """Coordinate BLE connection, refreshes and entity updates."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )
        self.entry = entry
        self.client: VolixClient | None = None

    async def _async_update_data(self) -> None:
        """Refresh telemetry, reusing an existing BLE connection."""

        # Reuse the active connection whenever possible.
        if self.client is not None and self.client.connected:
            try:
                await self.client.refresh()
                return
            except Exception as err:
                _LOGGER.warning(
                    "VOLIX refresh failed, reconnecting: %s",
                    err,
                )
                await self._disconnect_client()

        # Discover the device only when a new connection is needed.
        device = bluetooth.async_ble_device_from_address(
            self.hass,
            self.entry.unique_id,
            connectable=True,
        )

        if device is None:
            raise UpdateFailed(
                "VOLIX P1800 is not currently visible "
                "to a Bluetooth adapter"
            )

        # Remove any stale client before reconnecting.
        await self._disconnect_client()

        try:
            self.client = VolixClient(device, self.entry.title)
            await self.client.connect(self.async_set_update_error)
            await self.client.refresh()

        except Exception as err:
            _LOGGER.warning(
                "VOLIX Bluetooth connection failed: %s",
                err,
            )
            await self._disconnect_client()
            raise UpdateFailed(
                f"Bluetooth update failed: {err}"
            ) from err

    async def _disconnect_client(self) -> None:
        """Safely disconnect and discard the BLE client."""
        client = self.client
        self.client = None

        if client is None:
            return

        try:
            await client.disconnect()
        except Exception as err:
            _LOGGER.warning(
                "VOLIX Bluetooth disconnect failed: %s",
                err,
            )

    def async_set_update_error(self) -> None:
        """Schedule recovery after an unexpected disconnect."""
        self.hass.loop.call_soon_threadsafe(
            self.async_request_refresh
        )

    async def async_shutdown(self) -> None:
        """Close the BLE connection on shutdown."""
        await self._disconnect_client()
