from __future__ import annotations

from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Enable aggregator mode: all devices on one shared host/port, addressed by unit_id
    aggregator_enabled: bool = True
    modbus_host: str = "0.0.0.0"
    modbus_port: int = 502

    # Enable per-device mode: each device gets its own TCP server (host/port from device file)
    per_device_enabled: bool = False

    # Value returned for any address not present in a device's register map.
    # Matches the docker-compose default (DEFAULT_REGISTER_VALUE=0).
    default_register_value: int = 0
    log_level: str = "INFO"
    random_seed: Optional[int] = None
    # False (default): 1-based addressing — standard Modbus (Modbus Poll, most PLCs)
    # True: 0-based addressing — use when clients send raw PDU addresses (e.g. pymodbus client)
    zero_mode: bool = False

    model_config = {"env_prefix": ""}

    @field_validator("random_seed", mode="before")
    @classmethod
    def _empty_str_to_none(cls, v: object) -> object:
        if v == "":
            return None
        return v
