"""VOLIX P1800 local Bluetooth integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PLATFORMS
from .coordinator import VolixCoordinator

type VolixConfigEntry = ConfigEntry[VolixCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: VolixConfigEntry) -> bool:
    coordinator = VolixCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: VolixConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        await entry.runtime_data.async_shutdown()
    return unload_ok
