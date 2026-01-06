# WiFi QR Decoder – Home Assistant Integration

The **WiFi QR Decoder** integration extracts WiFi credentials (SSID and password) from a QR code provided by an `image.*` entity in Home Assistant.  
It is ideal for guest WiFi dashboards, automations, and dynamic QR displays.

> **⚠️ Requirement:**
>  This integration requires the **UniFi Network** integration to be installed and configured.
>  The UniFi integration provides the WiFi QR code image entity used for decoding.

This integration provides:

- **SSID sensor** – Extracted WiFi network name  
- **Password sensor** – Extracted WiFi password  
- **Decode status sensor** – Success/error state  
- **QR code image entity** – For dashboards and sharing  
- **Force-decode service** – Manually trigger re-decoding  


## 🔧 Installation

### Manual Installation

1. Download or clone this repository.
2. Copy the folder:

```
/wifi_qr_decoder/
```

into your Home Assistant:

```
config/custom_components/
```

3. Restart Home Assistant.

---

## ⚙️ Configuration

1. Go to **Settings → Devices & Services**  
2. Click **Add Integration**  
3. Search for **WiFi QR Decoder**  
4. Select the `image.*` entity that contains your WiFi QR code  

The integration will automatically create:

- `sensor.<name>_ssid`  
- `sensor.<name>_password`  
- `sensor.<name>_decode_status`  
- `image.<name>_qr_code`  

---

## 🧪 Service: `wifi_qr_decoder.force_decode`

You can manually trigger a re-decode using:

```yaml
service: wifi_qr_decoder.force_decode
```

Useful when:

- The QR code image updates  
- You want to refresh sensors on demand  

---


## 🔐 Privacy & Security

If you do **not** want the WiFi password stored in Home Assistant’s database, add this to your `configuration.yaml`:

```yaml
recorder:
  exclude:
    entities:
      - sensor.<name>_password

logbook:
  exclude:
    entities:
      - sensor.<name>_password

history:
  exclude:
    entities:
      - sensor.<name>_password
```

This prevents the password from appearing in:

- History  
- Logbook  
- Recorder database  

---

## 🧩 Example Dashboard Card

```yaml
type: markdown
content: |
  # Guest WiFi  
  **SSID:** {{ states('sensor.<name>_ssid') }}  
  **Password:** {{ states('sensor.<name>_password') }}
```

---

## 🛠️ Troubleshooting

- If the integration does not appear, restart Home Assistant Core.  
- If the image entity is missing, ensure your camera or image source is working.  
- If decoding fails, check the **Decode Status** sensor for details.  

---
