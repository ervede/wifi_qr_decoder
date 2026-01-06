# WiFi QR Decoder – Home Assistant Integration

The **WiFi QR Decoder** integration extracts WiFi credentials (SSID and password) from a QR code provided by an `image.*` entity in Home Assistant.  
It is ideal for guest WiFi dashboards, automations, and dynamic QR displays.

> ## ⚠️ Requirement  
> This integration requires the **UniFi Network** integration to be installed and configured.  
> UniFi Network provides the WiFi QR code image entity that this integration decodes.

---

## ✨ Features

This integration provides:

- **SSID sensor** – Extracted WiFi network name  
- **Password sensor** – Extracted WiFi password  
- **Decode status sensor** – Success/error state  
- **Force‑decode service** – Manually trigger re-decoding  
- **Multi‑SSID support** – Add as many SSIDs as you want  
- **Automatic sensor naming** based on the decoded SSID  
- **Device grouping** in the Integrations UI  

---

## 📡 Multi‑SSID Support

The **WiFi QR Decoder** integration fully supports **multiple SSIDs**, each with its own QR code and its own set of sensors.  
This allows you to decode and manage several WiFi networks at once — perfect for setups with:

- Guest WiFi  
- IoT networks  
- Office / Work VLANs  
- Separate 2.4 GHz / 5 GHz SSIDs  
- Multiple UniFi WiFi networks  

Each SSID is handled as a **separate integration instance**, and each instance creates its own sensors based on the decoded SSID.

### How Multi‑SSID Works

When you add the integration, you select an `image.*` entity containing a WiFi QR code.  
You can repeat this process for **as many SSIDs as you want**.

Each instance automatically creates:

- `sensor.<ssid>_ssid`  
- `sensor.<ssid>_password`  
- `sensor.<ssid>_decode_status`  

Where `<ssid>` is a **safe, normalized version** of the WiFi network name.

### Example

#### Guest WiFi  
Creates:

- `sensor.guest_wifi_ssid`  
- `sensor.guest_wifi_password`  
- `sensor.guest_wifi_decode_status`  

#### Office 5G  
Creates:

- `sensor.office_5g_ssid`  
- `sensor.office_5g_password`  
- `sensor.office_5g_decode_status`  

All sensors appear neatly grouped under their own device in:

**Settings → Devices & Services → WiFi QR Decoder (SSID)**

### Adding Multiple SSIDs

To add another SSID:

1. Go to **Settings → Devices & Services**  
2. Click **Add Integration**  
3. Select **WiFi QR Decoder**  
4. Choose a different `image.*` entity containing another WiFi QR code  

There is **no limit** to how many SSIDs you can add.

---

## 🔧 Installation

### Manual Installation

1. Download or clone this repository.  
2. Copy the folder:

```custom_components/wifi_qr_decoder/```

into your Home Assistant:

```config/custom_components/```

3. Restart Home Assistant.

---

## ⚙️ Configuration

1. Go to **Settings → Devices & Services**  
2. Click **Add Integration**  
3. Search for **WiFi QR Decoder**  
4. Select the `image.*` entity that contains your WiFi QR code  

The integration will automatically create:

- `sensor.<ssid>_ssid`  
- `sensor.<ssid>_password`  
- `sensor.<ssid>_decode_status`  

---

## 🧪 Service: `wifi_qr_decoder.force_decode`

You can manually trigger a re-decode using:

service:
```yaml
wifi_qr_decoder.force_decode
```
Optional field:
```yaml
config_entry_id: "<entry_id>" 
```
If omitted, all instances will refresh.

Useful when:
- The QR code image updates
- You want to refresh sensors on demand

---

## 🔐 Privacy & Security

If you do not want the WiFi password stored in Home Assistant’s database, add this to your configuration.yaml:

```yaml
recorder:
  exclude:
    entities:
      - sensor.<ssid>_password
```
```yaml
logbook:
  exclude:
    entities:
      - sensor.<ssid>_password
```
```yaml
history:
  exclude:
    entities:
      - sensor.<ssid>_password
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
  ## Guest WiFi
  **SSID:** {{ states('sensor.guest_wifi_ssid') }}
  **Password:** {{ states('sensor.guest_wifi_password') }}
```

---

## 🛠️ Troubleshooting
- If the integration does not appear, restart Home Assistant Core.
- If the image entity is missing, ensure your UniFi Network integration is working.
- If decoding fails, check the Decode Status sensor for details.
- If you see old devices with “Unknown”, remove the integration entry and re-add it.

## 📜 License
This project is licensed under the MIT License.
See the LICENSE file for details.
