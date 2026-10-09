"""Work-mode selection for VOLIX P1800."""

from homeassistant.components.select import SelectEntity
from homeassistant.exceptions import HomeAssistantError

from . import VolixConfigEntry
from .entity import VolixEntity
from .protocol import make_settings_frame

MODES = {"Mute": 0, "Standard": 1, "Fast": 2}


async def async_setup_entry(hass, entry: VolixConfigEntry, async_add_entities) -> None:
    async_add_entities((WorkModeSelect(entry),))


class WorkModeSelect(VolixEntity, SelectEntity):
    _attr_translation_key = "work_mode"
    _attr_options = list(MODES)
    def __init__(self, entry): super().__init__(entry); self.unique("work_mode")
    @property
    def current_option(self):
        settings = self.coordinator.client.settings if self.coordinator.client else None
        return next((name for name, value in MODES.items() if settings and value == settings.work_mode), None)
    async def async_select_option(self, option: str):
        client = self.coordinator.client
        if not client or not client.settings: raise HomeAssistantError("Station settings are unavailable")
        settings = client.settings
        flags = (settings.flags & ~0x06) | (MODES[option] << 1)
        await client.write(make_settings_frame(flags=flags, eco_hours=settings.eco_hours))
        await self.coordinator.async_request_refresh()
