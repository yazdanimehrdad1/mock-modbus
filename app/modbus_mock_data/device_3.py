"""Mock register data for device-3 — utility-scale PV plant.

Sourced from a real operational site's register map
(PV_Asset_Mock_Modbus_Register_Map.csv): POI meter, weather station, PV
fleet aggregates, and 4 named inverters. Holding registers only (the real
site's map defines no FC04 input registers).

Addressing: this server's default zero_mode=False ("1-based addressing —
standard Modbus, Modbus Poll, most PLCs", see settings.py) means a register
typed/sent as address N on the wire lands on dict key N+1. So dict keys here
are the CSV's literal `Offset` column **plus 1** — i.e. each key is exactly
the address you'd type into a standard Modbus client to read that point,
the same convention device_1.py/device_2.py already use.

16-bit simplification: 19 of the real points are 32-bit (int32/uint32,
2 registers) — POI meter electrical totals and 5 PV-fleet aggregates. Each
of those is kept as a single 16-bit register at its *primary* offset only;
the old low-word offset (primary + 1) is omitted, same as the "not defined"
gaps already used in device_1/device_2. Where the real engineering range
didn't fit 16 bits at the original scale, the unit/scale was rebased
(W->kW, A x0.001->x0.1, Wh/kWh->MWh) to preserve the real magnitude.
PV_AVG_INVERTER_EFFICIENCY also fixes a source-CSV bug (scale 0.001
overflows uint16 at 100% -> rescaled to 0.01).

Holding register layout:
  1–37   POI Meter — site-level electrical totals (even offsets 2-38 are
         gaps: former low words of the 32-bit fields above).
  39–48  Weather — GHI + 2x POA irradiance/temperature sensors.
  49–67  PV Fleet — inverter-count aggregates + plant-level totals (gaps at
         55/57/59/61/63: former low words of the 32-bit aggregates).
  68–99  Inverters 01–04 — 8 registers each (MODE, AC_ACTIVE_POWER,
         AC_REACTIVE_POWER, GRID_VOLTAGE_AB, GRID_CURRENT_A, PV_INPUT_POWER,
         INTERNAL_TEMP, FAULT_CODE), contiguous, no gaps.

Randomness: every dynamic register draws uniformly across its own min/max
band via DynamicRegisterBlock. Time-of-day / generation-correlated
behaviour is intentionally not modelled yet, and will be revisited.

INV0x_MODE encodes the real site's bit-flag mode codes as sequential
integers (the random generator can't usefully pick discrete bit values
out of a flat numeric range): 1=Derate(0x0800) 2=Running(0x1000)
3=Standby(0x2000) 4=Check(0x4000) 5=Fault(0x8000).
"""
from __future__ import annotations

from app.models import DeviceSpec, RegisterSpec

# The real site's register map defines no FC04 input registers, so
# ``input_registers`` is left to its default empty map.
DEVICE = DeviceSpec(
    name="device_3",
    unit_id=3,
    host="0.0.0.0",
    port=5022,
    holding_registers={
        # ── POI Meter (1–37) ─────────────────────────────────────────────────
        1: RegisterSpec(base=5500, min=-7500, max=7500),  # Active power total x0.1 kW (was W, int32)
        3: RegisterSpec(base=200, min=-5000, max=5000),  # Reactive power total x0.1 kVAR (was VAR, int32)
        5: RegisterSpec(base=5600, min=0, max=9000),  # Apparent power total x0.1 kVA (was VA, uint32)
        7: RegisterSpec(base=27600, min=25000, max=30000),  # Voltage avg L-N x0.01 V
        9: RegisterSpec(base=47700, min=43000, max=52000),  # Voltage avg L-L x0.01 V
        11: RegisterSpec(base=6000, min=0, max=12000),  # Current avg x0.1 A (was x0.001, uint32)
        13: RegisterSpec(base=9800, min=-10000, max=10000),  # Power factor x0.0001 pu
        15: RegisterSpec(base=60000, min=59500, max=60500),  # Frequency x0.001 Hz
        17: RegisterSpec(base=27600, min=25000, max=30000),  # Voltage A x0.01 V
        19: RegisterSpec(base=27500, min=25000, max=30000),  # Voltage B x0.01 V
        21: RegisterSpec(base=27700, min=25000, max=30000),  # Voltage C x0.01 V
        23: RegisterSpec(base=6050, min=0, max=12000),  # Current A x0.1 A (was x0.001, uint32)
        25: RegisterSpec(base=5980, min=0, max=12000),  # Current B x0.1 A (was x0.001, uint32)
        27: RegisterSpec(base=6020, min=0, max=12000),  # Current C x0.1 A (was x0.001, uint32)
        29: RegisterSpec(base=1830, min=-2500, max=2500),  # Active power A x0.1 kW (was W, int32)
        31: RegisterSpec(base=1830, min=-2500, max=2500),  # Active power B x0.1 kW (was W, int32)
        33: RegisterSpec(base=1840, min=-2500, max=2500),  # Active power C x0.1 kW (was W, int32)
        35: RegisterSpec(base=800, min=0, max=5000),  # Import energy total x1 MWh (was Wh, uint32)
        37: RegisterSpec(base=42000, min=0, max=80000),  # Export energy total x1 MWh (was Wh, uint32)

        # 2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38 — gaps (former low
        # words of the 32-bit fields above) — not defined.

        # ── Weather (39–48) ──────────────────────────────────────────────────
        39: RegisterSpec(base=850, min=0, max=1200),  # GHI irradiance x1 W/m2
        40: RegisterSpec(base=380, min=-200, max=800),  # GHI sensor body temp x0.1 C
        41: RegisterSpec(base=0, min=0, max=7),  # GHI status bitfield (narrowed from CSV's 0..65535)
        42: RegisterSpec(base=8500, min=0, max=12000),  # POA1 irradiance x0.1 W/m2
        43: RegisterSpec(base=420, min=-100, max=900),  # POA1 cell temp x0.1 C
        44: RegisterSpec(base=280, min=-100, max=600),  # POA1 ambient temp x0.1 C
        45: RegisterSpec(base=35, min=0, max=400),  # POA1 wind speed x0.1 m/s
        46: RegisterSpec(base=8450, min=0, max=12000),  # POA2 irradiance x0.1 W/m2
        47: RegisterSpec(base=415, min=-100, max=900),  # POA2 cell temp x0.1 C
        48: RegisterSpec(base=285, min=-100, max=600),  # POA2 ambient temp x0.1 C

        # ── PV Fleet (49–67) ─────────────────────────────────────────────────
        49: RegisterSpec(base=50, min=0, max=55),  # Available inverter count
        50: RegisterSpec(base=45, min=0, max=55),  # Running inverter count
        51: RegisterSpec(base=0, min=0, max=5),  # Faulted inverter count (narrowed from CSV's 0..55)
        52: RegisterSpec(base=5, min=0, max=55),  # Standby inverter count
        53: RegisterSpec(base=0, min=0, max=8),  # Derated inverter count (narrowed from CSV's 0..55)
        54: RegisterSpec(base=18000, min=0, max=33000),  # Total AC active power x0.1 kW
        56: RegisterSpec(base=800, min=-20000, max=20000),  # Total AC reactive power x0.1 kVAR
        58: RegisterSpec(base=19500, min=0, max=36000),  # Total DC input power x0.1 kW
        60: RegisterSpec(base=15000, min=0, max=30000),  # Total daily energy x1 kWh (was x0.1)
        62: RegisterSpec(base=42000, min=0, max=85000),  # Total lifetime energy x1 MWh (was kWh, uint32)
        64: RegisterSpec(base=9700, min=0, max=10000),  # Avg inverter efficiency x0.01 % (fixes CSV scale-overflow bug, was 0.001)
        65: RegisterSpec(base=480, min=-100, max=1000),  # Max heatsink temp x0.1 C
        66: RegisterSpec(base=460, min=-100, max=1000),  # Max internal temp x0.1 C
        67: RegisterSpec(base=0, min=0, max=7),  # Alarm summary bitfield (narrowed from CSV's 0..65535)

        # 55,57,59,61,63 — gaps (former low words of the 32-bit aggregates above)
        # — not defined.

        # ── Inverter 01 (68–75) ──────────────────────────────────────────────
        # 1=Derate(0x0800) 2=Running(0x1000) 3=Standby(0x2000) 4=Check(0x4000) 5=Fault(0x8000)
        68: RegisterSpec(base=2, min=1, max=5),  # Mode
        69: RegisterSpec(base=480, min=0, max=700),  # AC active power x0.1 kW
        70: RegisterSpec(base=30, min=-700, max=700),  # AC reactive power x0.1 kVAR
        71: RegisterSpec(base=4800, min=4300, max=5200),  # Grid voltage AB x0.1 V
        72: RegisterSpec(base=650, min=0, max=1000),  # Grid current A x0.1 A
        73: RegisterSpec(base=510, min=0, max=750),  # PV input power x0.1 kW
        74: RegisterSpec(base=420, min=-100, max=1000),  # Internal temp x0.1 C
        75: RegisterSpec(base=0, min=0, max=10),  # Fault code (0=none, narrowed from CSV's 0..65535)

        # ── Inverter 02 (76–83) ──────────────────────────────────────────────
        76: RegisterSpec(base=2, min=1, max=5),  # Mode
        77: RegisterSpec(base=470, min=0, max=700),  # AC active power x0.1 kW
        78: RegisterSpec(base=25, min=-700, max=700),  # AC reactive power x0.1 kVAR
        79: RegisterSpec(base=4790, min=4300, max=5200),  # Grid voltage AB x0.1 V
        80: RegisterSpec(base=640, min=0, max=1000),  # Grid current A x0.1 A
        81: RegisterSpec(base=500, min=0, max=750),  # PV input power x0.1 kW
        82: RegisterSpec(base=415, min=-100, max=1000),  # Internal temp x0.1 C
        83: RegisterSpec(base=0, min=0, max=10),  # Fault code

        # ── Inverter 03 (84–91) ──────────────────────────────────────────────
        84: RegisterSpec(base=2, min=1, max=5),  # Mode
        85: RegisterSpec(base=490, min=0, max=700),  # AC active power x0.1 kW
        86: RegisterSpec(base=28, min=-700, max=700),  # AC reactive power x0.1 kVAR
        87: RegisterSpec(base=4810, min=4300, max=5200),  # Grid voltage AB x0.1 V
        88: RegisterSpec(base=660, min=0, max=1000),  # Grid current A x0.1 A
        89: RegisterSpec(base=515, min=0, max=750),  # PV input power x0.1 kW
        90: RegisterSpec(base=425, min=-100, max=1000),  # Internal temp x0.1 C
        91: RegisterSpec(base=0, min=0, max=10),  # Fault code

        # ── Inverter 04 (92–99) ──────────────────────────────────────────────
        92: RegisterSpec(base=2, min=1, max=5),  # Mode
        93: RegisterSpec(base=460, min=0, max=700),  # AC active power x0.1 kW
        94: RegisterSpec(base=22, min=-700, max=700),  # AC reactive power x0.1 kVAR
        95: RegisterSpec(base=4785, min=4300, max=5200),  # Grid voltage AB x0.1 V
        96: RegisterSpec(base=630, min=0, max=1000),  # Grid current A x0.1 A
        97: RegisterSpec(base=495, min=0, max=750),  # PV input power x0.1 kW
        98: RegisterSpec(base=410, min=-100, max=1000),  # Internal temp x0.1 C
        99: RegisterSpec(base=0, min=0, max=10),  # Fault code
    },
)
