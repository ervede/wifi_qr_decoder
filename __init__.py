from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, SERVICE_FORCE_DECODE


async def async_setup(hass: HomeAssistant, config: dict):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    async def handle_force_decode(call: ServiceCall):
        """Force all wifi_qr_decoder sensors to refresh."""
        ent_reg = er.async_get(hass)
        comp = hass.data["entity_components"]["sensor"]

        for entity_id, entry_data in ent_reg.entities.items():
            if entry_data.platform == DOMAIN:
                obj = comp.get_entity(entity_id)
                if obj and hasattr(obj, "async_update"):
                    await obj.async_update()
                    obj.async_write_ha_state()

    hass.services.async_register(
        DOMAIN,
        SERVICE_FORCE_DECODE,
        handle_force_decode
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
