import logging
import re
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def normalize_ssid(ssid: str) -> str:
    ssid = ssid.lower().strip()
    ssid = re.sub(r"[^a-z0-9_]+", "_", ssid)
    ssid = re.sub(r"_+", "_", ssid)
    return ssid.strip("_")


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        WifiSSIDSensor(coordinator, entry),
        WifiPasswordSensor(coordinator, entry),
        WifiDecodeStatusSensor(coordinator, entry),
    ]
    async_add_entities(entities)


class WifiBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for WiFi QR Decoder sensors."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry
        self._ssid = None
        self._safe_ssid = None
        self._update_ssid_context()

    def _update_ssid_context(self):
        data = self.coordinator.data or {}
        ssid = data.get("ssid")
        if ssid:
            self._ssid = ssid
            self._safe_ssid = normalize_ssid(ssid)
        else:
            self._ssid = "Unknown"
            self._safe_ssid = f"entry_{self.entry.entry_id}"

    @property
    def device_info(self) -> DeviceInfo:
        """Group sensors under one device per config entry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry.entry_id)},
            name=self.entry.title,
            manufacturer="WiFi QR Decoder",
            model="QR WiFi Credential Extractor",
        )

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_update(self):
        """Request coordinator refresh."""
        await self.coordinator.async_request_refresh()

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def extra_state_attributes(self):
        attrs = {}
        if self._ssid and self._ssid != "Unknown":
            attrs["decoded_ssid"] = self._ssid
        return attrs

    @property
    def _data(self):
        return self.coordinator.data or {}


class WifiSSIDSensor(WifiBaseSensor):
    """Sensor for decoded SSID."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_{self._safe_ssid}_ssid"

    @property
    def name(self):
        return f"{self._ssid} SSID"

    @property
    def native_value(self):
        self._update_ssid_context()
        return self._data.get("ssid")


class WifiPasswordSensor(WifiBaseSensor):
    """Sensor for decoded WiFi password."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_{self._safe_ssid}_password"

    @property
    def name(self):
        return f"{self._ssid} Password"

    @property
    def native_value(self):
        self._update_ssid_context()
        return self._data.get("password")


class WifiDecodeStatusSensor(WifiBaseSensor):
    """Sensor for decode status."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_{self._safe_ssid}_decode_status"

    @property
    def name(self):
        return f"{self._ssid} Decode Status"

    @property
    def native_value(self):
        self._update_ssid_context()
        return self._data.get("status")
