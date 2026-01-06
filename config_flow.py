from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers import selector

from .const import DOMAIN, CONF_IMAGE_ENTITY


class WifiQRConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for WiFi QR Decoder."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            image_entity = user_input[CONF_IMAGE_ENTITY]
            title = f"WiFi QR Decoder ({image_entity})"

            return self.async_create_entry(
                title=title,
                data={CONF_IMAGE_ENTITY: image_entity},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IMAGE_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain="image")
                    )
                }
            ),
        )
