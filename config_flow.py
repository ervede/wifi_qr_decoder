import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, CONF_IMAGE_ENTITY


class WifiQRConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="WiFi QR Decoder",
                data=user_input,
            )

        entity_reg = er.async_get(self.hass)
        image_entities = [
            e.entity_id
            for e in entity_reg.entities.values()
            if e.entity_id.startswith("image.")
        ]

        schema = vol.Schema({
            vol.Required(CONF_IMAGE_ENTITY): vol.In(image_entities)
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry):
        return WifiQROptionsFlow(config_entry)


class WifiQROptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        entity_reg = er.async_get(self.hass)
        image_entities = [
            e.entity_id
            for e in entity_reg.entities.values()
            if e.entity_id.startswith("image.")
        ]

        current = self.config_entry.options.get(
            CONF_IMAGE_ENTITY,
            self.config_entry.data.get(CONF_IMAGE_ENTITY),
        )

        schema = vol.Schema({
            vol.Required(CONF_IMAGE_ENTITY, default=current): vol.In(image_entities)
        })

        return self.async_show_form(step_id="init", data_schema=schema)
