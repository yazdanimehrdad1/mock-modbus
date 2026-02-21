"""Mock register data for device-1.

Holding registers start at address 1400 (32 registers, 1400–1431).
Each non-zero base value has ±10% variance; zero values are fixed at 0.
Large values near 65535 have their upper bound capped at 65535.
"""
from __future__ import annotations

UNIT_ID = 1
HOST = "0.0.0.0"
PORT = 5020

HOLDING_REGISTERS: dict[int, dict[str, int]] = {
    1400: {"min": 260, "max": 318},      # base 289
    1401: {"min": 5, "max": 7},          # base 6
    1402: {"min": 0, "max": 0},          # base 0
    1403: {"min": 57370, "max": 65535},  # base 63745 (upper capped at 65535)
    1404: {"min": 58976, "max": 65535},  # base 65529 (upper capped at 65535)
    1405: {"min": 57554, "max": 65535},  # base 63949 (upper capped at 65535)
    1406: {"min": 2153, "max": 2633},    # base 2393
    1407: {"min": 4383, "max": 5357},    # base 4870
    1408: {"min": 4389, "max": 5365},    # base 4877
    1409: {"min": 4401, "max": 5379},    # base 4890
    1410: {"min": 3, "max": 5},          # base 4
    1411: {"min": 2537, "max": 3101},    # base 2819
    1412: {"min": 0, "max": 0},          # base 0
    1413: {"min": 0, "max": 0},          # base 0
    1414: {"min": 0, "max": 0},          # base 0
    1415: {"min": 0, "max": 0},          # base 0
    1416: {"min": 540, "max": 660},      # base 600
    1417: {"min": 540, "max": 660},      # base 600
    1418: {"min": 0, "max": 0},          # base 0
    1419: {"min": 0, "max": 0},          # base 0
    1420: {"min": 0, "max": 0},          # base 0
    1421: {"min": 0, "max": 0},          # base 0
    1422: {"min": 0, "max": 0},          # base 0
    1423: {"min": 0, "max": 0},          # base 0
    1424: {"min": 9, "max": 11},         # base 10
    1425: {"min": 0, "max": 0},          # base 0
    1426: {"min": 0, "max": 0},          # base 0
    1427: {"min": 4383, "max": 5359},    # base 4871
    1428: {"min": 4391, "max": 5367},    # base 4879
    1429: {"min": 4406, "max": 5386},    # base 4896
    1430: {"min": 15, "max": 19},        # base 17
    1431: {"min": 0, "max": 0},          # base 0
}

INPUT_REGISTERS: dict[int, dict[str, int]] = {}
