# Home Assistant ALLPOWERS VOLIX P1800

Local Bluetooth monitoring and control for the ALLPOWERS VOLIX P1800 power station. No ALLPOWERS cloud account is required.

> [!CAUTION]
> This is independent community software, not affiliated with VOLIX, ALLPOWERS, Home Assistant or ESPHome. Output controls are experimental: validate them on your own hardware before relying on automations.

## Current features

- Bluetooth discovery through a local Home Assistant adapter or ESPHome Bluetooth proxy
- Battery level, input power, output power and estimated remaining runtime
- Charging and power-supply activity indicators
- AC output and USB output controls
- Car-charger/12 V output and ECO mode controls
- Mute, Standard and Fast charging-mode selection
- Local operation without credentials or cloud access

Additional station features will be added only after their Bluetooth data and control behaviour have been verified on a VOLIX P1800.

## Bluetooth requirements

Home Assistant manages Bluetooth routing automatically. This integration does not bind the station to a particular adapter or ask the user to select a proxy.

A connectable Bluetooth path can be provided by:

- a Bluetooth adapter attached to the Home Assistant host;
- an ESPHome Bluetooth proxy running on a BLE-capable ESP32, including an ESP32-C3; or
- another connectable remote Bluetooth adapter supported by Home Assistant.

An ESP8266 cannot act as a Bluetooth proxy because it has no Bluetooth radio. Place the adapter or proxy within reliable BLE range of the station and ensure it appears under **Settings -> Devices & services -> Bluetooth**.

Only one BLE client can normally control the station at a time. Disconnect the official mobile application and disable any dedicated ESPHome BLE-client firmware before configuring this integration. A dedicated ESP32 may remain in use as a standard active Bluetooth proxy.

### Minimal ESP32-C3 ESPHome proxy example

This generic example contains no installation-specific credentials. Keep the referenced values in ESPHome's `secrets.yaml`, or let the ESPHome device wizard create the Wi-Fi, API and OTA sections.

```yaml
esphome:
  name: volix-bluetooth-proxy
  friendly_name: VOLIX Bluetooth Proxy

esp32:
  board: esp32-c3-devkitm-1
  framework:
    type: esp-idf

logger:

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

api:
  encryption:
    key: !secret bluetooth_proxy_api_key

ota:
  - platform: esphome
    password: !secret bluetooth_proxy_ota_password

esp32_ble_tracker:

bluetooth_proxy:
  active: true
```

The proxy must use `active: true` because the integration establishes a connection, subscribes to notifications and sends commands. Do not include an `esp32_ble_client` for the station in the proxy configuration.

For current proxy options and supported boards, consult the [ESPHome Bluetooth Proxy documentation](https://esphome.io/components/bluetooth_proxy/) and [Home Assistant Bluetooth documentation](https://www.home-assistant.io/integrations/bluetooth/).

## Installation (development release)

1. Add this repository to HACS as a custom integration repository.
2. Install **ALLPOWERS VOLIX P1800** and restart Home Assistant.
3. Ensure the station is within reliable Bluetooth range of the Home Assistant host or an active ESPHome Bluetooth proxy.
4. Open **Settings -> Devices & services** and accept the discovered VOLIX P1800.

If automatic discovery is not displayed, choose **Add integration -> ALLPOWERS VOLIX P1800**. The setup flow will list any unconfigured station currently visible in Home Assistant's Bluetooth cache.

## Protocol credits

The packet format is derived from the MIT-licensed [`madninjaskillz/allpowers-ble`](https://github.com/madninjaskillz/allpowers-ble) project and the independently maintained MIT-licensed [`dedalodaelus/esphome-allpowers-ble`](https://github.com/dedalodaelus/esphome-allpowers-ble) implementation. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Status

Version `0.1.3` is a pre-release build undergoing validation with a physical VOLIX P1800. It should not yet be treated as a stable release.

## License

MIT
