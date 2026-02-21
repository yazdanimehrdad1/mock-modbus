from __future__ import annotations

import asyncio
import logging
import sys

from pymodbus.datastore import ModbusDeviceContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer

from app.datastore import build_device_blocks
from app.modbus_mock_data import DEVICES
from app.settings import Settings

logger = logging.getLogger("mock_modbus")


async def _start_aggregator(settings: Settings) -> None:
    """One TCP server, all devices registered by their unit_id."""
    device_contexts: dict[int, ModbusDeviceContext] = {}

    for device in DEVICES:
        hr, ir = build_device_blocks(
            device.holding_registers,
            device.input_registers,
            default_value=settings.default_register_value,
            seed=settings.random_seed,
        )
        device_contexts[device.unit_id] = ModbusDeviceContext(hr=hr, ir=ir)
        logger.info("  Registered %-12s unit_id=%d", device.name, device.unit_id)

    context = ModbusServerContext(devices=device_contexts, single=False)

    logger.info(
        "Starting aggregator server on %s:%d (%d device(s))",
        settings.modbus_host,
        settings.modbus_port,
        len(DEVICES),
    )
    await StartAsyncTcpServer(
        context=context,
        address=(settings.modbus_host, settings.modbus_port),
    )


async def _start_per_device(settings: Settings) -> None:
    """One TCP server per device, each on its own host/port."""
    servers = []

    for device in DEVICES:
        hr, ir = build_device_blocks(
            device.holding_registers,
            device.input_registers,
            default_value=settings.default_register_value,
            seed=settings.random_seed,
        )
        context = ModbusServerContext(
            devices={device.unit_id: ModbusDeviceContext(hr=hr, ir=ir)},
            single=False,
        )
        logger.info(
            "  Starting %-12s on %s:%d  unit_id=%d",
            device.name,
            device.host,
            device.port,
            device.unit_id,
        )
        servers.append(
            StartAsyncTcpServer(context=context, address=(device.host, device.port))
        )

    await asyncio.gather(*servers)


async def run_server() -> None:
    settings = Settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )

    logger.info("Configuration:")
    logger.info("  server_mode   = %s", settings.server_mode)
    logger.info("  devices       = %d", len(DEVICES))
    logger.info("  default_value = %d", settings.default_register_value)
    logger.info("  random_seed   = %s", settings.random_seed)

    if settings.server_mode == "aggregator":
        logger.info("  host          = %s", settings.modbus_host)
        logger.info("  port          = %d", settings.modbus_port)
        await _start_aggregator(settings)
    else:
        await _start_per_device(settings)


if __name__ == "__main__":
    asyncio.run(run_server())
