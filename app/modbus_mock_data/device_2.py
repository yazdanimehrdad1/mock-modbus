"""Mock register data for device-2.

Holding registers at 2000–2003 (setpoints / configuration).
Input registers at 3000–3003 (live measurements).
Each non-zero base value has ±10% variance.
"""
from __future__ import annotations

UNIT_ID = 2
HOST = "0.0.0.0"
PORT = 5021

HOLDING_REGISTERS: dict[int, dict[str, int]] = {
    2000: {"min": 1980, "max": 2420},  # base 2200  — voltage setpoint (×10, 220.0 V)
    2001: {"min": 450, "max": 550},    # base 500   — frequency setpoint (×10, 50.0 Hz)
    2002: {"min": 1, "max": 1},        # base 1     — control mode (fixed)
    2003: {"min": 900, "max": 1100},   # base 1000  — power limit (×10, 100.0 %)
}

INPUT_REGISTERS: dict[int, dict[str, int]] = {
    3000: {"min": 1976, "max": 2414},  # base 2195  — measured voltage (×10, 219.5 V)
    3001: {"min": 137, "max": 167},    # base 152   — measured current (×10, 15.2 A)
    3002: {"min": 301, "max": 367},    # base 334   — measured power (×10, 33.4 kW)
    3003: {"min": 405, "max": 495},    # base 450   — temperature (×10, 45.0 °C)
}
