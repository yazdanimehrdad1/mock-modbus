"""Mock register data for device-2 — battery energy storage system (BESS).

Holding registers 3000–3015 (16 total) — configuration, control, aggregate status.
Input registers  4000–4015 (16 total) — real-time cell measurements and BMS diagnostics.

Holding register layout:
  3000–3004  INT16 measurements.
  3005–3008  Not defined — absent from register map (client should treat as unavailable).
  3009–3011  Enum registers — integer 1–N representing a named state.
  3012–3014  Bitfield registers — each bit is an independent boolean flag.
  3015       Reserved.

Input register layout:
  4000–4004  INT16 cell-level and energy measurements.
             Note: min/max/avg cell voltage registers share the same numeric band
             intentionally — they represent the same physical quantity at cell level.
  4005–4008  Not defined — absent from register map.
  4009–4011  Enum registers — integer 1–N representing a named state.
  4012–4014  Bitfield registers — each bit is an independent boolean flag.
  4015       Reserved.
"""
from __future__ import annotations

UNIT_ID = 2
HOST = "0.0.0.0"
PORT = 5021

HOLDING_REGISTERS: dict[int, dict[str, int]] = {
    # ── INT16 measurements (3000–3004) ──────────────────────────────────────
    3000: {"base": 4800, "min": 3800, "max": 5600},  # Pack voltage ×10 V (380–560 V)
    3001: {"base":  500, "min":    0, "max": 1500},  # Charge/discharge current ×10 A (0–150 A)
    3002: {"base":  280, "min":  150, "max":  600},  # Pack temperature ×10 °C (15–60 °C)
    3003: {"base":  750, "min":    0, "max": 1000},  # State of charge ×10 % (0–100 %)
    3004: {"base": 5000, "min":    0, "max":10000},  # Inverter output power W (0–10 kW)

    # 3005–3008 not defined — absent from register map.

    # ── Enum registers (3009–3011) — valid range 1–N ────────────────────────
    # 1=Standby 2=Charging 3=Discharging 4=Balancing 5=Fault
    3009: {"base": 3, "min": 1, "max": 5},
    # 1=CC 2=CV 3=CC-CV 4=Solar-MPPT
    3010: {"base": 3, "min": 1, "max": 4},
    # 1=Island 2=Grid-Follow 3=Grid-Form
    3011: {"base": 2, "min": 1, "max": 3},

    # ── Bitfield registers (3012–3014) — each bit is an independent flag ────
    # bits 0–7: cell group health (bit N set = group N healthy)
    3012: {"base": 255, "min": 0, "max": 255},
    # bits 0–7: protection triggers (0=OVP 1=UVP 2=OCP 3=OTP 4=short 5=leakage 6=BMS-fault 7=balance-active)
    3013: {"base":   0, "min": 0, "max": 255},
    # bits 0–4: system control (0=grid-connected 1=AC-relay 2=DC-contactor 3=precharge 4=remote-shutdown)
    3014: {"base":   6, "min": 0, "max":  31},

    # ── Reserved (3015) ─────────────────────────────────────────────────────
    3015: {"base": 0, "min": 0, "max": 0},
}

INPUT_REGISTERS: dict[int, dict[str, int]] = {
    # ── INT16 cell-level & energy measurements (4000–4004) ──────────────────
    # min/max/avg cell voltage share the same band — same physical quantity per cell.
    4000: {"base": 3200, "min": 2800, "max": 4200},  # Cell voltage min ×1 mV (2800–4200 mV, LFP)
    4001: {"base": 3300, "min": 2800, "max": 4200},  # Cell voltage max ×1 mV
    4002: {"base": 3250, "min": 2800, "max": 4200},  # Cell voltage avg ×1 mV
    4003: {"base": 2500, "min":    0, "max": 5000},  # Total charge today ×10 Wh (0–500 Wh)
    4004: {"base": 2000, "min":    0, "max": 5000},  # Total discharge today ×10 Wh (0–500 Wh)

    # 4005–4008 not defined — absent from register map.

    # ── Enum registers (4009–4011) — valid range 1–N ────────────────────────
    # 1=Init 2=Idle 3=Charging 4=Discharging 5=Balancing 6=Fault
    4009: {"base": 4, "min": 1, "max": 6},
    # 1=LFP 2=NMC 3=NCA 4=LTO
    4010: {"base": 1, "min": 1, "max": 4},
    # 1=Normal 2=Warm 3=Hot 4=Critical
    4011: {"base": 1, "min": 1, "max": 4},

    # ── Bitfield registers (4012–4014) — each bit is an independent flag ────
    # bits 0–7: cell group balancing active (bit N set = group N currently balancing)
    4012: {"base":   0, "min": 0, "max": 255},
    # bits 0–7: alarm status (0=overtemp 1=undertemp 2=cell-OV 3=cell-UV 4=SOC-low 5=SOC-high 6=I-high 7=BMS-err)
    4013: {"base":   0, "min": 0, "max": 255},
    # bits 0–3: diagnostics (0=cell-drift 1=capacity-fade 2=high-resistance 3=aging-alert)
    4014: {"base":   0, "min": 0, "max":  15},

    # ── Reserved (4015) ─────────────────────────────────────────────────────
    4015: {"base": 0, "min": 0, "max": 0},
}
