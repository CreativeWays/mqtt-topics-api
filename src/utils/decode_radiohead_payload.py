from typing import List, TypedDict

"""Decode RadioHead payload"""


class Payload(TypedDict):
    sensor_id: int
    voltage: float


def decode_radiohead_payload(payload: List[int]) -> Payload:
    # Extract 16-bit sensor ID (bytes 0-1)
    sensor_id = (payload[1] << 8) | payload[0]

    # Extract 16-bit voltage (bytes 2-3)
    voltage_raw = (payload[3] << 8) | payload[2]
    voltage = voltage_raw / 100.0

    return {
        "sensor_id": sensor_id,
        "voltage": voltage,
    }
