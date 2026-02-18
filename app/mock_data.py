HOLDING_REGISTERS: dict[int, dict[str, int]] = {
    0: {"min": 400, "max": 600},
    1: {"min": 0, "max": 100},
    10: {"min": 1000, "max": 2000},
    200: {"min": 0, "max": 65535},
    1000: {"min": 200, "max": 240},
}

INPUT_REGISTERS: dict[int, dict[str, int]] = {
    0: {"min": 300, "max": 500},
    50: {"min": 100, "max": 200},
    2000: {"min": 0, "max": 1000},
}
