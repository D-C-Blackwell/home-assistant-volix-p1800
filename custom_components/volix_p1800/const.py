"""Constants for the VOLIX P1800 integration."""

from typing import Final

DOMAIN: Final = "volix_p1800"
PLATFORMS: Final = ["binary_sensor", "sensor", "select", "switch"]

SERVICE_UUID: Final = "0000fff0-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID: Final = "0000fff1-0000-1000-8000-00805f9b34fb"
WRITE_UUID: Final = "0000fff2-0000-1000-8000-00805f9b34fb"

STATUS_REQUEST: Final = bytes.fromhex("A565B1000106010000000000")
UPDATE_INTERVAL_SECONDS: Final = 20
