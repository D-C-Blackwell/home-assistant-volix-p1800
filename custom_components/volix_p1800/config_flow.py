"""Config flow for automatically discovered VOLIX P1800 stations."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, SERVICE_UUID


def _is_supported(discovery_info: BluetoothServiceInfoBleak) -> bool:
    """Return whether an advertisement belongs to a VOLIX P1800."""
    name = discovery_info.name or ""
    service_uuids = {uuid.lower() for uuid in discovery_info.service_uuids}
    return name.upper().startswith("VOLIX P1800") or SERVICE_UUID in service_uuids


class VolixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Bluetooth discovery and confirmation."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        self.context["title_placeholders"] = {"name": discovery_info.name}
        self._set_confirm_only()
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(
                title=self.context["title_placeholders"]["name"], data={}
            )
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders=self.context["title_placeholders"],
        )

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Allow manual setup by selecting a currently visible station."""
        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            discovery_info = self._discovered_devices[address]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=discovery_info.name or "VOLIX P1800", data={}
            )

        current_addresses = self._async_current_ids(include_ignore=False)
        for discovery_info in async_discovered_service_info(
            self.hass, connectable=True
        ):
            address = discovery_info.address
            if address in current_addresses or not _is_supported(discovery_info):
                continue
            self._discovered_devices[address] = discovery_info

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        stations = {
            address: discovery_info.name or "VOLIX P1800"
            for address, discovery_info in self._discovered_devices.items()
        }
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_ADDRESS): vol.In(stations)}),
        )
