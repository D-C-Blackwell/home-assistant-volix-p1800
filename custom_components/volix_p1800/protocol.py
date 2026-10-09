"""Pure-Python codec for the verified ALLPOWERS BLE packet subset."""

from __future__ import annotations

from dataclasses import dataclass


class ProtocolError(ValueError):
    """Raised when a station packet is malformed or unsupported."""


@dataclass(frozen=True, slots=True)
class StatusData:
    """Decoded command-0x01 telemetry."""

    battery_level: int
    input_power: int
    output_power: int
    remaining_minutes: int
    usb_output: bool
    ac_output: bool


@dataclass(frozen=True, slots=True)
class SettingsData:
    """Decoded command-0x03 settings snapshot."""

    flags: int
    eco_hours: int
    eco_enabled: bool
    work_mode: int
    car_charger: bool
    hardware_version: str
    firmware_version: str


def xor_bytes(data: bytes | bytearray) -> int:
    """Return XOR of every byte."""
    checksum = 0
    for value in data:
        checksum ^= value
    return checksum


def validate_frame(data: bytes) -> None:
    """Validate notification envelope, declared length and checksum."""
    if len(data) < 8:
        raise ProtocolError("short frame")
    if data[:2] != b"\xA5\x65":
        raise ProtocolError("unknown header")
    if 8 + data[5] != len(data):
        raise ProtocolError("inconsistent payload length")
    if xor_bytes(data):
        raise ProtocolError("invalid XOR checksum")


def _version(value: int) -> str:
    high, low = value >> 4, value & 0x0F
    return f"{high}.{low}" if high < 10 and low < 10 else f"0x{value:02X}"


def parse_status(data: bytes) -> StatusData:
    """Decode a command-0x01 status notification."""
    validate_frame(data)
    if data[6] != 0x01 or len(data) < 16:
        raise ProtocolError("not a complete status frame")
    if data[8] > 100:
        raise ProtocolError("battery level outside 0-100%")
    state = data[7]
    return StatusData(
        battery_level=data[8],
        input_power=int.from_bytes(data[9:11], "big"),
        output_power=int.from_bytes(data[11:13], "big"),
        remaining_minutes=int.from_bytes(data[13:15], "big"),
        usb_output=bool(state & 0x01),
        ac_output=bool(state & 0x02),
    )


def parse_settings(data: bytes) -> SettingsData:
    """Decode a command-0x03 settings notification."""
    validate_frame(data)
    if data[6] != 0x03 or len(data) < 14:
        raise ProtocolError("not a complete settings frame")
    flags = data[7]
    return SettingsData(
        flags=flags,
        eco_hours=data[8],
        eco_enabled=bool(flags & 0x01),
        work_mode=(flags & 0x06) >> 1,
        car_charger=bool(flags & 0x10),
        hardware_version=_version(data[11]),
        firmware_version=_version(data[12]),
    )


def make_output_frame(*, usb_output: bool, ac_output: bool) -> bytes:
    """Build the verified combined output-control frame."""
    state = (0x01 if usb_output else 0) | (0x02 if ac_output else 0)
    frame = bytearray((0xA5, 0x65, 0x00, 0xB1, 0x01, 0x01, 0x00, state, 0))
    frame[-1] = xor_bytes(frame[:-1])
    return bytes(frame)


def make_settings_frame(*, flags: int, eco_hours: int) -> bytes:
    """Build a settings write while preserving every unmanaged bit."""
    frame = bytearray((0xA5, 0x65, 0x00, 0xB1, 0x01, 0x02, 0x02, flags, eco_hours, 0))
    frame[-1] = xor_bytes(frame[:-1])
    return bytes(frame)
