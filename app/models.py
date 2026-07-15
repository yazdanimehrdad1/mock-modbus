"""Pydantic models for mock-device configuration.

Device modules under ``app/modbus_mock_data`` declare their registers as plain
``{"base": ..., "min": ..., "max": ...}`` dicts for authoring convenience;
those dicts are validated into :class:`RegisterSpec` instances at discovery
time (see ``app/modbus_mock_data/__init__.py``), so a malformed register map
fails fast at startup instead of producing bad reads at runtime.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RegisterSpec(BaseModel):
    """Bounds for a single dynamically-generated Modbus register.

    ``base`` is the nominal/at-rest value (documentation for now); ``min``/``max``
    define the inclusive band the datastore draws a random value from on each read.
    """

    model_config = ConfigDict(extra="forbid")

    base: int
    min: int
    max: int

    @model_validator(mode="after")
    def _check_bounds(self) -> "RegisterSpec":
        if self.min > self.max:
            raise ValueError(f"min ({self.min}) must be <= max ({self.max})")
        return self


class DeviceSpec(BaseModel):
    """A single mock Modbus device discovered from a device module."""

    model_config = ConfigDict(extra="forbid")

    name: str
    unit_id: int
    host: str
    port: int
    holding_registers: dict[int, RegisterSpec] = Field(default_factory=dict)
    input_registers: dict[int, RegisterSpec] = Field(default_factory=dict)
