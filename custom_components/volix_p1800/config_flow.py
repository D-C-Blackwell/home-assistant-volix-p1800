"""Config flow for automatically discovered VOLIX P1800 stations."""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class VolixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Bluetooth discovery and confirmation."""

    VERSION = 1

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
        return self.async_abort(reason="bluetooth_discovery_required")
