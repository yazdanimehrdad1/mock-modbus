# Mock Modbus TCP Server

Dynamic Modbus TCP register simulator. It emulates industrial energy devices (solar
inverter, battery/BESS, utility-scale PV plant) and serves **holding registers (FC 03)**
and **input registers (FC 04)**. On every read, each register returns a fresh random
value within its configured `[min, max]` band; unmapped addresses return
`DEFAULT_REGISTER_VALUE`. Writes are ignored (read-only mock).

Built on pymodbus 3.5–3.6, pydantic v2, and pydantic-settings. Python 3.11.

## Quick start

Local:

```bash
pip install -r requirements.txt
MODBUS_PORT=5020 python -m app.server     # port 502 is privileged; use a high port locally
```

Container:

```bash
docker network create pae-shared-network   # if not already created
docker compose up --build                  # or: make up
```

The server listens on port **502** by default and serves 3 devices.

## Run modes

- **Aggregator** (default, `AGGREGATOR_ENABLED=true`): one TCP server on
  `MODBUS_HOST:MODBUS_PORT`; clients select a device by its `unit_id` (1/2/3).
- **Per-device** (`PER_DEVICE_ENABLED=true`): each device also gets its own server on
  its own port (5020 / 5021 / 5022). Both modes may run at once.

## Environment variables

| Variable                 | Default   | Description                                                        |
|--------------------------|-----------|--------------------------------------------------------------------|
| `AGGREGATOR_ENABLED`     | `true`    | Serve all devices on one port, addressed by `unit_id`.             |
| `MODBUS_HOST`            | `0.0.0.0` | Aggregator bind address.                                           |
| `MODBUS_PORT`            | `502`     | Aggregator TCP port.                                               |
| `PER_DEVICE_ENABLED`     | `false`   | Also serve each device on its own host/port.                       |
| `DEFAULT_REGISTER_VALUE` | `0`       | Value for addresses not in a device's register map.                |
| `LOG_LEVEL`              | `INFO`    | Python log level.                                                  |
| `RANDOM_SEED`            | *(empty)* | Integer seed for deterministic output; empty ⇒ non-deterministic.  |
| `ZERO_MODE`              | `false`   | `false` = 1-based (Modbus Poll/PLCs); `true` = 0-based (pymodbus).  |

See [.env.example](.env.example) for a copyable template.

## Register definitions

Devices live in `app/modbus_mock_data/` — one file per device (`device_1.py`,
`device_2.py`, `device_3.py`), each exporting `DEVICE = DeviceSpec(...)`. To add a
device, drop a new `device_N.py` into that folder; it's auto-discovered and validated
at startup. See [CLAUDE.md](CLAUDE.md) for the full architecture and a device template.

## Testing

```python
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("localhost", port=5020)
client.connect()

# Device 1 (solar inverter) exposes holding registers starting at 1400.
result = client.read_holding_registers(1400, count=4, slave=1)
print(result.registers)

client.close()
```

> Note: with default `ZERO_MODE=false` (1-based), request the register address as-is
> (e.g. `1400`). If your client sends 0-based PDU addresses, set `ZERO_MODE=true`.

There is also a standalone raw-socket smoke test:
`python tests/test_server.py --host localhost --port 5020 --unit-id 1`
(not a pytest suite; some hardcoded addresses predate the current device maps).
