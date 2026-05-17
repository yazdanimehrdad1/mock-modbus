from __future__ import annotations

import logging
import random
from typing import Any, Optional

from pymodbus.datastore import ModbusSequentialDataBlock

logger = logging.getLogger("mock_modbus")


class DynamicRegisterBlock(ModbusSequentialDataBlock):
    """Data block that generates random values within configured bounds on every read."""

    def __init__(
        self,
        metadata: dict[int, dict[str, int]],
        default_value: int,
        rng: random.Random,
        label: str,
    ) -> None:
        # Initialise parent with a single dummy slot; validate() is overridden
        # so pymodbus never rejects an address that is in our metadata dict.
        super().__init__(1, [default_value])
        self._metadata = metadata
        self._default = default_value
        self._rng = rng
        self._label = label

    def validate(self, address: int, count: int = 1) -> bool:
        return True

    def getValues(self, address: int, count: int = 1) -> list[int]:
        result: list[int] = []
        for addr in range(address, address + count):
            entry = self._metadata.get(addr)
            if entry is not None:
                result.append(self._rng.randint(entry["min"], entry["max"]))
            else:
                result.append(self._default)
        logger.info("READ %s address=%d count=%d -> %s", self._label, address, count, result)
        return result

    def setValues(self, _address: int, _values: Any) -> None:
        pass


def build_device_blocks(
    holding_registers: dict[int, dict[str, int]],
    input_registers: dict[int, dict[str, int]],
    default_value: int = 0,
    seed: Optional[int] = None,
) -> tuple[DynamicRegisterBlock, DynamicRegisterBlock]:
    rng = random.Random(seed)
    holding_register = DynamicRegisterBlock(holding_registers, default_value, rng, "holding")
    input_register = DynamicRegisterBlock(input_registers, default_value, rng, "input")
    return holding_register, input_register
