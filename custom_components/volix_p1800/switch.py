"""Verified output switches for VOLIX P1800."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.exceptions import HomeAssistantError

from . import VolixConfigEntry
from .entity import VolixEntity
from .protocol import make_output_frame, make_settings_frame


async def async_setup_entry(hass, entry: VolixConfigEntry, async_add_entities) -> None:
    async_add_entities((OutputSwitch(entry, "ac_output", False), OutputSwitch(entry, "usb_output", True), CarSwitch(entry), EcoSwitch(entry)))


class OutputSwitch(VolixEntity, SwitchEntity):
    def __init__(self, entry, key: str, usb: bool):
        super().__init__(entry)
        self._attr_translation_key = key
        self.usb = usb
        self.unique(key)

    @property
    def is_on(self):
        status = self.coordinator.client.status if self.coordinator.client else None
        return getattr(status, "usb_output" if self.usb else "ac_output") if status else None

    async def _set(self, enabled: bool):
        client = self.coordinator.client
        if not client or not client.status:
            raise HomeAssistantError("Current output state is unavailable")
        status = client.status
        await client.write(make_output_frame(usb_output=enabled if self.usb else status.usb_output, ac_output=status.ac_output if self.usb else enabled))
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, **kwargs): await self._set(True)
    async def async_turn_off(self, **kwargs): await self._set(False)


class CarSwitch(VolixEntity, SwitchEntity):
    _attr_translation_key = "car_charger"
    def __init__(self, entry): super().__init__(entry); self.unique("car_charger")
    @property
    def is_on(self):
        settings = self.coordinator.client.settings if self.coordinator.client else None
        return settings.car_charger if settings else None
    async def _set(self, enabled):
        client = self.coordinator.client
        if not client or not client.settings: raise HomeAssistantError("Station settings are unavailable")
        settings = client.settings
        flags = (settings.flags | 0x10) if enabled else (settings.flags & ~0x10)
        await client.write(make_settings_frame(flags=flags, eco_hours=settings.eco_hours))
        await self.coordinator.async_request_refresh()
    async def async_turn_on(self, **kwargs): await self._set(True)
    async def async_turn_off(self, **kwargs): await self._set(False)


class EcoSwitch(CarSwitch):
    _attr_translation_key = "eco_mode"
    def __init__(self, entry): VolixEntity.__init__(self, entry); self.unique("eco_mode")
    @property
    def is_on(self):
        settings = self.coordinator.client.settings if self.coordinator.client else None
        return settings.eco_enabled if settings else None
    async def _set(self, enabled):
        client = self.coordinator.client
        if not client or not client.settings: raise HomeAssistantError("Station settings are unavailable")
        settings = client.settings
        flags = (settings.flags | 0x01) if enabled else (settings.flags & ~0x01)
        await client.write(make_settings_frame(flags=flags, eco_hours=settings.eco_hours))
        await self.coordinator.async_request_refresh()
