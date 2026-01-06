import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, CONF_IMAGE_ENTITY
from .decoder import decode_wifi_qr

_LOGGER = logging.getLogger(__name__)


class WifiQRCoordinator(DataUpdateCoordinator):
    """Coordinator for decoding WiFi QR codes."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=None,  # Only on demand / service
        )
        self.entry = entry

    async def _async_update_data(self):
        """Decode the QR code for the configured image entity."""
        entity_id = self.entry.data[CONF_IMAGE_ENTITY]

        state = self.hass.states.get(entity_id)
        if not state:
            _LOGGER.warning("No state for image entity %s", entity_id)
            return {"status": "no_image"}

        picture = state.attributes.get("entity_picture")
        if not picture:
            _LOGGER.warning("No entity_picture for %s", entity_id)
            return {"status": "no_picture"}

        ssid, password = await decode_wifi_qr(self.hass, picture)

        status = "ok" if ssid else "decode_failed"
        _LOGGER.debug("Decoded result for %s: ssid=%s status=%s", entity_id, ssid, status)

        return {
            "ssid": ssid,
            "password": password,
            "status": status,
        }
