# Home Assistant VOLIX P1800

Local Bluetooth monitoring and control for the VOLIX P1800 power station. No ALLPOWERS cloud account is required.

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

The integration deliberately does **not** expose an imaginary light, fan state, DC-input scheduling, temperatures, voltage or current. Those features require verified protocol evidence from real P1800 hardware.

## Installation (development release)

1. Add this repository to HACS as a custom integration repository.
2. Install **VOLIX P1800** and restart Home Assistant.
3. Ensure the station is visible to a Home Assistant Bluetooth adapter or active ESPHome Bluetooth proxy.
4. Open **Settings → Devices & services** and accept the discovered VOLIX P1800.

Only one BLE client can normally control the station at a time. Disconnect the official mobile application and disable any dedicated ESPHome BLE-client firmware before configuring this integration. An ESP32 may remain in use as a standard active Bluetooth proxy.

## Privacy and security

The repository contains no device addresses, Wi-Fi credentials, Home Assistant tokens, API keys or private network details. The station address is learned through Home Assistant Bluetooth discovery and stored in Home Assistant's config entry.

## Protocol credits

The packet format is derived from the MIT-licensed [`madninjaskillz/allpowers-ble`](https://github.com/madninjaskillz/allpowers-ble) project and the independently maintained MIT-licensed [`dedalodaelus/esphome-allpowers-ble`](https://github.com/dedalodaelus/esphome-allpowers-ble) implementation. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Status

Version `0.1.0` is an early development release and still requires validation on Home Assistant with a physical VOLIX P1800.

## License

MIT
