import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import service

from .const import DOMAIN, PLATFORMS, SERVICE_FORCE_DECODE
from .coordinator import WifiQRCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up from YAML (not used)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up WiFi QR Decoder from a config entry."""
    coordinator = WifiQRCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register service once
    if not hass.services.has_service(DOMAIN, SERVICE_FORCE_DECODE):

        async def handle_force_decode(call):
            """Handle manual force decode for all or a specific entry."""
            target_entry_id = call.data.get("config_entry_id")
            if target_entry_id:
                coord = hass.data[DOMAIN].get(target_entry_id)
                if coord:
                    await coord.async_request_refresh()
            else:
                for coord in hass.data[DOMAIN].values():
                    await coord.async_request_refresh()

        hass.services.async_register(
            DOMAIN,
            SERVICE_FORCE_DECODE,
            handle_force_decode,
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    # If no entries left, remove service
    if not hass.data[DOMAIN]:
        if hass.services.has_service(DOMAIN, SERVICE_FORCE_DECODE):
            hass.services.async_remove(DOMAIN, SERVICE_FORCE_DECODE)

    return unload_ok
