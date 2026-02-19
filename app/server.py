from __future__ import annotations

import asyncio
import logging
import sys

from pymodbus.datastore import ModbusDeviceContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer

from app.datastore import build_blocks
from app.settings import Settings

logger = logging.getLogger("mock_modbus")


async def run_server() -> None:
    settings = Settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )

    logger.info("Configuration:")
    logger.info("  host          = %s", settings.modbus_host)
    logger.info("  port          = %d", settings.modbus_port)
    logger.info("  unit_id       = %d", settings.modbus_unit_id)
    logger.info("  default_value = %d", settings.default_register_value)
    logger.info("  random_seed   = %s", settings.random_seed)

    hr_block, ir_block = build_blocks(
        default_value=settings.default_register_value,
        seed=settings.random_seed,
    )

    slave_context = ModbusDeviceContext(hr=hr_block, ir=ir_block)

    context = ModbusServerContext(
        devices={settings.modbus_unit_id: slave_context},
        single=False,
    )

    logger.info(
        "Starting Modbus TCP server on %s:%d",
        settings.modbus_host,
        settings.modbus_port,
    )

    await StartAsyncTcpServer(
        context=context,
        address=(settings.modbus_host, settings.modbus_port),
    )


if __name__ == "__main__":
    asyncio.run(run_server())
