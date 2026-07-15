"""Mock register data for device-1 — 3-phase grid-tied solar inverter.

Holding registers 1400–1431 (32 total) — configuration, control, aggregate status.
Input registers  2000–2031 (32 total) — real-time sensor readings, per-phase measurements.

Holding register layout:
  1400–1410  INT16 measurements (distinct non-overlapping numeric bands, see table below).
  1411–1414  Not defined — absent from register map (client should treat as unavailable).
  1415–1420  Enum registers — integer 1–N representing a named state.
  1421–1430  Bitfield registers — each bit is an independent boolean flag.
  1431       Reserved.

Numeric bands used by 1400–1410 (raw register values, ascending, no overlap):
  [0,10]       1408 fault code
  [11,45]      1406 output current ×10 A
  [50,180]     1405 PV string current ×10 A
  [200,750]    1404 temperature ×10 °C
  [850,999]    1407 power factor ×1000
  [1000,2900]  1403 active power W
  [3000,4800]  1401 PV array voltage ×10 V
  [4990,5010]  1402 grid frequency ×100 Hz
  [5200,6500]  1409 apparent power VA
  [7000,8000]  1400 DC bus voltage ×10 V
  [8100,9500]  1410 total runtime hours

Input register layout:
  2000–2010  INT16 per-phase and environmental measurements.
             Note: L1/L2/L3 voltage and current registers intentionally share overlapping
             numeric bands — they represent the same physical quantity on each phase.
  2011–2014  Not defined — absent from register map.
  2015–2020  Enum registers — integer 1–N representing a named state.
  2021–2030  Bitfield registers — each bit is an independent boolean flag.
  2031       Reserved.
"""
from __future__ import annotations

from app.models import DeviceSpec, RegisterSpec

DEVICE = DeviceSpec(
    name="device_1",
    unit_id=1,
    host="0.0.0.0",
    port=5020,
    holding_registers={
        # ── INT16 measurements (1400–1410) ──────────────────────────────────────
        1400: RegisterSpec(base=7600, min=7000, max=8000),  # DC bus voltage ×10 V (700–800 V)
        1401: RegisterSpec(base=3800, min=3000, max=4800),  # PV array voltage ×10 V (300–480 V)
        1402: RegisterSpec(base=5000, min=4990, max=5010),  # Grid frequency ×100 Hz (49.90–50.10 Hz)
        1403: RegisterSpec(base=2300, min=1000, max=2900),  # Active power W (1.0–2.9 kW)
        1404: RegisterSpec(base=380, min=200, max=750),  # Inverter temperature ×10 °C (20–75 °C)
        1405: RegisterSpec(base=130, min=50, max=180),  # PV string current ×10 A (5.0–18.0 A)
        1406: RegisterSpec(base=25, min=11, max=45),  # AC output current ×10 A (1.1–4.5 A)
        1407: RegisterSpec(base=985, min=850, max=999),  # Power factor ×1000 (0.850–0.999)
        1408: RegisterSpec(base=0, min=0, max=10),  # Active fault code (0 = none, 1–10 = fault)
        1409: RegisterSpec(base=5900, min=5200, max=6500),  # Apparent power VA (5.2–6.5 kVA)
        1410: RegisterSpec(base=8760, min=8100, max=9500),  # Total runtime hours (~1 yr baseline)

        # ── Enum registers (1415–1420) — valid range 1–N ────────────────────────
        # 1=Off 2=Startup 3=MPPT 4=Derating 5=Fault 6=Night
        1415: RegisterSpec(base=3, min=1, max=6),
        # 1=Disconnected 2=Connecting 3=Connected 4=Fault
        1416: RegisterSpec(base=3, min=1, max=4),
        # 1=None 2=Info 3=Warning 4=Minor 5=Major
        1417: RegisterSpec(base=1, min=1, max=5),
        # 1=Single-string 2=Dual 3=Triple 4=Quad
        1418: RegisterSpec(base=2, min=1, max=4),
        # 1=Init 2=Running 3=Degraded 4=Offline
        1419: RegisterSpec(base=2, min=1, max=4),
        # 1=Off 2=Low 3=Medium 4=High 5=Max
        1420: RegisterSpec(base=3, min=1, max=5),

        # ── Bitfield registers (1421–1430) — each bit is an independent flag ────
        # bits 0–7: alarm types (overcurrent, overvoltage, overtemp, …)
        1421: RegisterSpec(base=0, min=0, max=255),
        # bits 0–7: warning types (high temp, low irradiance, grid fluctuation, …)
        1422: RegisterSpec(base=0, min=0, max=255),
        # bits 0–5: grid faults (0=overvoltage 1=undervoltage 2=overfreq 3=underfreq 4=phase-loss 5=imbalance)
        1423: RegisterSpec(base=0, min=0, max=63),
        # bits 0–5: inverter faults (0=overtemp 1=DC-overv 2=DC-underv 3=overcurrent 4=short 5=insulation)
        1424: RegisterSpec(base=0, min=0, max=63),
        # bits 0–5: feature enables (0=MPPT 1=anti-island 2=react-pwr-ctrl 3=pwr-limit 4=remote-stop 5=logging)
        1425: RegisterSpec(base=7, min=0, max=63),
        # bits 0–4: digital inputs (0=E-stop 1=door 2=AC-switch 3=DC-switch 4=GFI-relay)
        1426: RegisterSpec(base=12, min=0, max=31),
        # bits 0–4: digital outputs (0=fan 1=fault-relay 2=AC-contactor 3=DC-contactor 4=buzzer)
        1427: RegisterSpec(base=5, min=0, max=31),
        # bits 0–7: PV string health (bit N set = string N connected and healthy)
        1428: RegisterSpec(base=255, min=0, max=255),
        # bits 0–5: comms status (0=Modbus 1=CAN 2=Ethernet 3=WiFi 4=BT 5=RS485)
        1429: RegisterSpec(base=7, min=0, max=63),
        # bits 0–5: hardware health (0=PSU 1=IGBT 2=caps 3=heatsink 4=sensors 5=firmware)
        1430: RegisterSpec(base=63, min=0, max=63),
    },
    input_registers={
        # ── INT16 per-phase & environmental measurements (2000–2010) ────────────
        # L1/L2/L3 voltage bands overlap intentionally — same physical quantity per phase.
        2000: RegisterSpec(base=2350, min=2270, max=2430),  # AC voltage L1-N ×10 V (227–243 V)
        2001: RegisterSpec(base=2348, min=2268, max=2428),  # AC voltage L2-N ×10 V (226.8–242.8 V)
        2002: RegisterSpec(base=2352, min=2272, max=2432),  # AC voltage L3-N ×10 V (227.2–243.2 V)
        2003: RegisterSpec(base=48, min=10, max=80),  # AC current L1 ×10 A (1.0–8.0 A)
        2004: RegisterSpec(base=47, min=10, max=80),  # AC current L2 ×10 A
        2005: RegisterSpec(base=49, min=10, max=80),  # AC current L3 ×10 A
        2006: RegisterSpec(base=850, min=100, max=1100),  # Solar irradiance W/m²
        2007: RegisterSpec(base=220, min=100, max=450),  # Ambient temperature ×10 °C (10–45 °C)
        2008: RegisterSpec(base=380, min=200, max=650),  # Module temperature ×10 °C (20–65 °C)
        2009: RegisterSpec(base=150, min=0, max=500),  # Daily energy generated ×10 Wh (0–50 kWh)
        2010: RegisterSpec(base=5000, min=1000, max=9999),  # Lifetime energy ×100 kWh (100–999.9 MWh)

        # 2011–2014 not defined — absent from register map.

        # ── Enum registers (2015–2020) — valid range 1–N ────────────────────────
        # 1=Fixed 2=Perturb&Observe 3=IncrementalConductance 4=RippleCorrelation
        2015: RegisterSpec(base=2, min=1, max=4),
        # 1=ABC 2=ACB 3=Unknown
        2016: RegisterSpec(base=1, min=1, max=3),
        # 1=Off 2=Passive 3=Active-Low 4=Active-High 5=Emergency
        2017: RegisterSpec(base=3, min=1, max=5),
        # 1=Ok 2=Low 3=Critical 4=Fault
        2018: RegisterSpec(base=1, min=1, max=4),
        # 1=Idle 2=Downloading 3=Verifying 4=Installing 5=Rebooting
        2019: RegisterSpec(base=1, min=1, max=5),
        # 1=Idle 2=Active 3=Busy 4=Error
        2020: RegisterSpec(base=2, min=1, max=4),

        # ── Bitfield registers (2021–2030) — each bit is an independent flag ────
        # bits 0–5: instantaneous over/under per phase (0=L1-OV 1=L1-UV 2=L2-OV 3=L2-UV 4=L3-OV 5=L3-UV)
        2021: RegisterSpec(base=0, min=0, max=63),
        # bits 0–7: protection trips since last clear (OCP, OVP, UVP, OFP, UFP, OTP, GFCI, RCD)
        2022: RegisterSpec(base=0, min=0, max=255),
        # bits 0–7: MPPT tracker active flags (bit N = tracker N currently tracking)
        2023: RegisterSpec(base=3, min=0, max=255),
        # bits 0–7: string input presence (bit N = string N connected and producing)
        2024: RegisterSpec(base=255, min=0, max=255),
        # bits 0–5: phase sync status (0=L1-locked 1=L2-locked 2=L3-locked 3=freq-ok 4=angle-ok 5=ready)
        2025: RegisterSpec(base=63, min=0, max=63),
        # bits 0–5: calibration done flags (0=V-sensor 1=I-sensor 2=temp 3=irr 4=freq 5=energy)
        2026: RegisterSpec(base=63, min=0, max=63),
        # bits 0–7: last self-test result (bit set = sub-system passed)
        2027: RegisterSpec(base=255, min=0, max=255),
        # bits 0–5: external sensor presence (0=pyranometer 1=wind 2=rain 3=amb-temp 4=mod-temp 5=grid-meter)
        2028: RegisterSpec(base=49, min=0, max=63),
        # bits 0–4: network interface link status (0=Modbus-TCP 1=MQTT 2=HTTP 3=SNMP 4=DNP3)
        2029: RegisterSpec(base=3, min=0, max=31),
        # bits 0–3: pending notification flags (0=event-log-full 1=fw-update-avail 2=service-due 3=cert-expiry)
        2030: RegisterSpec(base=0, min=0, max=15),

        # ── Reserved (2031) ─────────────────────────────────────────────────────
        2031: RegisterSpec(base=0, min=0, max=0),
    },
)