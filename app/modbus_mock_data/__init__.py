"""
Auto-discovers all device modules in this package and builds a DEVICES list.

Each device module must define HOLDING_REGISTERS and INPUT_REGISTERS dicts.
It may also define UNIT_ID (int), HOST (str), and PORT (int); these fall back
to the defaults below if omitted.

To add a new device, drop a new file (e.g. device_3.py) into this folder.
No other changes are needed.
"""
from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass, field
from pathlib import Path

_DEFAULT_HOST = "0.0.0.0"
_DEFAULT_PORT = 502


@dataclass
class DeviceSpec:
    name: str
    unit_id: int
    host: str
    port: int
    holding_registers: dict[int, dict[str, int]] = field(default_factory=dict)
    input_registers: dict[int, dict[str, int]] = field(default_factory=dict)


DEVICES: list[DeviceSpec] = []

_pkg_path = Path(__file__).parent

for _mod_info in pkgutil.iter_modules([str(_pkg_path)]):
    _mod = importlib.import_module(f"app.modbus_mock_data.{_mod_info.name}")
    DEVICES.append(
        DeviceSpec(
            name=_mod_info.name,
            unit_id=getattr(_mod, "UNIT_ID", 1),
            host=getattr(_mod, "HOST", _DEFAULT_HOST),
            port=getattr(_mod, "PORT", _DEFAULT_PORT),
            holding_registers=getattr(_mod, "HOLDING_REGISTERS", {}),
            input_registers=getattr(_mod, "INPUT_REGISTERS", {}),
        )
    )
