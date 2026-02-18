from __future__ import annotations

import logging
import random
from typing import Any, Optional

from pymodbus.datastore.store import BaseModbusDataBlock

logger = logging.getLogger("mock_modbus")


class DynamicRegisterBlock(BaseModbusDataBlock):
    """A data block that generates random values on every read."""

    def __init__(
        self,
        metadata: dict[int, dict[str, int]],
        default_value: int,
        rng: random.Random,
        label: str,
    ) -> None:
        self._metadata = metadata
        self._default = default_value
        self._rng = rng
        self._label = label
        self.address = 0
        self.default_value = default_value
        self.values: dict[int, int] = {}

    def getValues(self, address: int, count: int = 1) -> list[int]:
        logger.info("READ %s address=%d count=%d", self._label, address, count)
        result: list[int] = []
        for addr in range(address, address + count):
            entry = self._metadata.get(addr)
            if entry is not None:
                result.append(self._rng.randint(entry["min"], entry["max"]))
            else:
                result.append(self._default)
        return result

    def setValues(self, address: int, values: Any) -> None:
        pass

    def reset(self) -> None:
        pass


def build_blocks(
    default_value: int = 0,
    seed: Optional[int] = None,
) -> tuple[DynamicRegisterBlock, DynamicRegisterBlock]:
    from app.mock_data import HOLDING_REGISTERS, INPUT_REGISTERS

    rng = random.Random(seed)
    hr = DynamicRegisterBlock(HOLDING_REGISTERS, default_value, rng, "holding")
    ir = DynamicRegisterBlock(INPUT_REGISTERS, default_value, rng, "input")
    return hr, ir
