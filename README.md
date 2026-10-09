# home-assistant-volix-p1800
Local Home Assistant integration for the VOLIX P1800 power station using Bluetooth, with sensor monitoring and output controls, no cloud account required.

A custom Home Assistant integration for locally monitoring and controlling the ALLPOWER VOLIX P1800 portable power station over Bluetooth.
The project aims to expose battery level, input and output power, estimated runtime, charging status, temperatures, output states and other available telemetry directly in Home Assistant. Supported controls are intended to include AC output, USB output, car output and, where the Bluetooth protocol permits, DC charging and scheduling.
Communication remains entirely local and does not require an Allpowers cloud account. Bluetooth connectivity may be provided directly by the Home Assistant host or through a nearby ESPHome Bluetooth proxy, making the integration suitable for power stations installed away from the main Home Assistant system.
The initial implementation is based on protocol behaviour observed from a VOLIX P1800 and may also provide a foundation for supporting compatible Allpowers power stations.
