import aiohttp
import base64
from io import BytesIO

from PIL import Image
from pyzbar.pyzbar import decode

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url

from .const import DOMAIN, CONF_IMAGE_ENTITY


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    image_entity = entry.options.get(CONF_IMAGE_ENTITY, entry.data[CONF_IMAGE_ENTITY])

    async_add_entities([
        WifiSSIDSensor(hass, image_entity),
        WifiPasswordSensor(hass, image_entity),
    ], update_before_add=True)


class WifiBaseSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, hass: HomeAssistant, image_entity: str):
        self.hass = hass
        self.image_entity = image_entity
        self._attr_native_value = None

    async def fetch_image_bytes(self):
        entity = self.hass.states.get(self.image_entity)
        if not entity:
            return None

        entity_picture = entity.attributes.get("entity_picture")
        if not entity_picture:
            return None

        base_url = get_url(self.hass)
        full_url = f"{base_url}{entity_picture}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(full_url) as resp:
                    if resp.status == 200:
                        return await resp.read()
            except Exception:
                return None

        return None

    async def decode_qr(self):
        image_bytes = await self.fetch_image_bytes()
        if not image_bytes:
            return None

        try:
            img = Image.open(BytesIO(image_bytes))
            decoded = decode(img)
        except Exception:
            return None

        if not decoded:
            return None

        return decoded[0].data.decode("utf-8")

    def parse_wifi(self, qr_text):
        parts = qr_text.split(";")
        ssid = None
        password = None

        for p in parts:
            if p.startswith("S:"):
                ssid = p[2:]
            if p.startswith("P:"):
                password = p[2:]

        return ssid, password


class WifiSSIDSensor(WifiBaseSensor):
    _attr_name = "Guest WiFi SSID"
    _attr_unique_id = "wifi_qr_ssid"

    async def async_update(self):
        qr_text = await self.decode_qr()
        if qr_text:
            ssid, _ = self.parse_wifi(qr_text)
            self._attr_native_value = ssid


class WifiPasswordSensor(WifiBaseSensor):
    _attr_name = "Guest WiFi Password"
    _attr_unique_id = "wifi_qr_password"

    async def async_update(self):
        qr_text = await self.decode_qr()
        if qr_text:
            _, password = self.parse_wifi(qr_text)
            self._attr_native_value = password
