from __future__ import annotations

from typing import Literal, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_mode: Literal["aggregator", "per_device"] = "aggregator"

    # Used in aggregator mode (all devices share one host/port)
    modbus_host: str = "0.0.0.0"
    modbus_port: int = 502

    default_register_value: int = 0
    log_level: str = "INFO"
    random_seed: Optional[int] = None

    model_config = {"env_prefix": ""}

    @field_validator("random_seed", mode="before")
    @classmethod
    def _empty_str_to_none(cls, v: object) -> object:
        if v == "":
            return None
        return v
