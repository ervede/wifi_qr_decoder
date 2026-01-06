import logging
import aiohttp
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO

_LOGGER = logging.getLogger(__name__)


async def decode_wifi_qr(hass, entity_picture_url: str):
    """Download and decode a WiFi QR code image."""
    try:
        # Build absolute URL
        base_url = (
            hass.config.external_url
            or hass.config.internal_url
            or "http://homeassistant.local:8123"
        )

        if entity_picture_url.startswith("/"):
            full_url = base_url.rstrip("/") + entity_picture_url
        else:
            full_url = entity_picture_url

        _LOGGER.debug("Fetching QR image from: %s", full_url)

        async with aiohttp.ClientSession() as session:
            async with session.get(full_url) as resp:
                if resp.status != 200:
                    _LOGGER.error("Failed to download QR image: %s", resp.status)
                    return None, None
                data = await resp.read()

        image = Image.open(BytesIO(data))
        decoded = decode(image)

        if not decoded:
            _LOGGER.warning("No QR code found in image")
            return None, None

        qr_text = decoded[0].data.decode("utf-8")
        _LOGGER.debug("Decoded QR text: %s", qr_text)

        ssid = None
        password = None

        if qr_text.startswith("WIFI:"):
            parts = qr_text[5:].split(";")
            for part in parts:
                if part.startswith("S:"):
                    ssid = part[2:]
                elif part.startswith("P:"):
                    password = part[2:]

        return ssid, password

    except Exception as e:
        _LOGGER.exception("Error decoding WiFi QR code: %s", e)
        return None, None
