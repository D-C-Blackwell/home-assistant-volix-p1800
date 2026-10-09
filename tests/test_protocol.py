"""Protocol regression tests using public, synthetic frames."""

import importlib.util
from pathlib import Path
import sys

_PATH = Path(__file__).parents[1] / "custom_components" / "volix_p1800" / "protocol.py"
_SPEC = importlib.util.spec_from_file_location("volix_protocol", _PATH)
assert _SPEC and _SPEC.loader
_PROTOCOL = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _PROTOCOL
_SPEC.loader.exec_module(_PROTOCOL)

make_output_frame = _PROTOCOL.make_output_frame
make_settings_frame = _PROTOCOL.make_settings_frame
parse_settings = _PROTOCOL.parse_settings
parse_status = _PROTOCOL.parse_status
xor_bytes = _PROTOCOL.xor_bytes


def test_status_frame():
    status = parse_status(bytes.fromhex("A565B1000108011364012C00FA0078A1"))
    assert (status.battery_level, status.input_power, status.output_power, status.remaining_minutes) == (100, 300, 250, 120)
    assert status.usb_output and status.ac_output


def test_settings_frame():
    settings = parse_settings(bytes.fromhex("A565B1000106033704005A12343A"))
    assert settings.flags == 0x37 and settings.car_charger and settings.eco_enabled


def test_control_frames():
    assert make_output_frame(usb_output=True, ac_output=True).hex().upper() == "A56500B10101000372"
    frame = make_settings_frame(flags=0x37, eco_hours=4)
    assert frame.hex().upper() == "A56500B1010202370443" and xor_bytes(frame) == 0
