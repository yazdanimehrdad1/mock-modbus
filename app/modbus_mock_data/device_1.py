"""Mock register data for device-1 — 3-phase grid-tied solar inverter.

Holding registers 1400–1431 (32 total).
All multi-decimal values use ×10 scaling unless noted otherwise.
32-bit energy counters are stored as a single high-word register (low word not modelled).
Each base value has ±10% variance to simulate realistic fluctuation.
"""
from __future__ import annotations

UNIT_ID = 1
HOST = "0.0.0.0"
PORT = 5020

HOLDING_REGISTERS: dict[int, dict[str, int]] = {
    1400: {"base": 289,   "min": 260,   "max": 318},   # PV array input voltage (V, nominal 289 V)
    1401: {"base": 6,     "min": 5,     "max": 7},     # MPPT operating state (6 = normal tracking)
    1402: {"base": 3,     "min": 2,     "max": 4},     # active MPPT tracker count (fixed: 3 strings)
    1403: {"base": 63745, "min": 61955, "max": 65535}, # lifetime energy exported, high word (Wh)
    1404: {"base": 65529, "min": 65523, "max": 65535}, # total reactive energy delivered, high word (VARh)
    1405: {"base": 63949, "min": 62363, "max": 65535}, # total apparent energy delivered, high word (VAh)
    1406: {"base": 2393,  "min": 2153,  "max": 2633},  # AC output active power total (W)
    1407: {"base": 4870,  "min": 4383,  "max": 5357},  # phase A output current (mA, 4.87 A)
    1408: {"base": 4877,  "min": 4389,  "max": 5365},  # phase B output current (mA, 4.88 A)
    1409: {"base": 4890,  "min": 4401,  "max": 5379},  # phase C output current (mA, 4.89 A)
    1410: {"base": 4,     "min": 3,     "max": 5},     # active alarm count
    1411: {"base": 2819,  "min": 2537,  "max": 3101},  # total DC input power from PV array (W)
    1412: {"base": 1350,  "min": 1215,  "max": 1485},  # AC reactive power output (VAR)
    1413: {"base": 870,   "min": 783,   "max": 957},   # PV string 1 DC input current (mA, 0.87 A)
    1414: {"base": 480,   "min": 432,   "max": 528},   # heatsink temperature (×10, 48.0 °C)
    1415: {"base": 920,   "min": 828,   "max": 1012},  # power factor (×1000, nominal 0.920)
    1416: {"base": 600,   "min": 540,   "max": 660},   # insulation resistance PV+ to ground (kΩ)
    1417: {"base": 600,   "min": 540,   "max": 660},   # insulation resistance PV− to ground (kΩ)
    1418: {"base": 2750,  "min": 2475,  "max": 3025},  # AC apparent power output (VA; ≥ active power)
    1419: {"base": 4820,  "min": 4338,  "max": 5302},  # phase A grid voltage (×10, 482.0 V)
    1420: {"base": 4835,  "min": 4352,  "max": 5319},  # phase B grid voltage (×10, 483.5 V)
    1421: {"base": 4845,  "min": 4361,  "max": 5330},  # phase C grid voltage (×10, 484.5 V)
    1422: {"base": 35,    "min": 32,    "max": 38},    # voltage THD (×10, 3.5 %)
    1423: {"base": 28,    "min": 25,    "max": 31},    # current THD (×10, 2.8 %)
    1424: {"base": 10,    "min": 9,     "max": 11},    # cooling fan speed level (scale 1–10)
    1425: {"base": 750,   "min": 675,   "max": 825},   # DC overvoltage protection threshold (V)
    1426: {"base": 180,   "min": 162,   "max": 198},   # grid reconnect delay after fault (×10 s, 18.0 s)
    1427: {"base": 4871,  "min": 4383,  "max": 5359},  # phase A inverter output voltage (×10, 487.1 V)
    1428: {"base": 4879,  "min": 4391,  "max": 5367},  # phase B inverter output voltage (×10, 487.9 V)
    1429: {"base": 4896,  "min": 4406,  "max": 5386},  # phase C inverter output voltage (×10, 489.6 V)
    1430: {"base": 17,    "min": 15,    "max": 19},    # firmware major version (v17.x)
    1431: {"base": 7,     "min": 6,     "max": 8},     # hardware revision index
}

INPUT_REGISTERS: dict[int, dict[str, int]] = {}
