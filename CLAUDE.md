# CLAUDE.md

Guidance for Claude Code (and humans) working in this repo.

## Overview

A **dynamic Modbus TCP register simulator**. It emulates industrial energy devices
(solar inverter, battery/BESS, utility-scale PV plant) by serving Modbus **holding
registers (FC 03)** and **input registers (FC 04)**. On *every read*, each register
returns a fresh random value drawn from its configured `[min, max]` band
(`rng.randint(min, max) & 0xFFFF`). Addresses not in a device's map return
`default_register_value`. **Writes are silently ignored** — this is a read-only mock.

Stack: **pymodbus 3.5–3.6**, **pydantic v2**, **pydantic-settings**. Python **3.11**
(Docker image). Async throughout.

## Run it

Local (from repo root):

```bash
pip install -r requirements.txt
python -m app.server            # binds 0.0.0.0:502 by default
```

Port 502 is privileged on Linux/macOS — for local runs use a high port:

```bash
MODBUS_PORT=5020 python -m app.server
```

Container:

```bash
docker compose up --build       # or: make up
```

> Dependencies are managed with **pip + `requirements.txt`** (not uv). There is no
> `pyproject.toml`, lockfile, linter, or CI configured in this repo.

## Architecture — the read path

```
app/modbus_mock_data/device_N.py   →  exports DEVICE = DeviceSpec(...)
app/modbus_mock_data/__init__.py   →  auto-discovers every module's DEVICE into DEVICES
app/models.py                      →  DeviceSpec / RegisterSpec (pydantic v2, validated at import)
app/datastore.py                   →  build_device_blocks() → DynamicRegisterBlock.getValues() draws the random value
app/server.py                      →  entry point; aggregator and/or per-device TCP servers
```

- [app/models.py](app/models.py) — `RegisterSpec(base, min, max)` and
  `DeviceSpec(name, unit_id, host, port, holding_registers, input_registers)`. Both use
  `extra="forbid"`; `RegisterSpec` rejects `min > max`.
- [app/datastore.py](app/datastore.py) — `DynamicRegisterBlock` (a `ModbusSequentialDataBlock`)
  where `getValues` produces the random value per read and `setValues` is a no-op;
  `build_device_blocks(...)` builds the holding + input blocks sharing one `random.Random(seed)`.
- [app/modbus_mock_data/__init__.py](app/modbus_mock_data/__init__.py) — discovery; a module
  without a `DEVICE` export is skipped, a `DEVICE` that isn't a `DeviceSpec` raises `TypeError`.
- [app/server.py](app/server.py) — `_start_aggregator`, `_start_per_device`, `run_server`.

## How to add a device

Drop a new file `app/modbus_mock_data/device_4.py` exporting a `DEVICE`. No other
change is needed — it's auto-discovered, and its register map is validated at import
(fail-fast, so a bad map crashes startup rather than serving bad reads).

```python
from app.models import DeviceSpec, RegisterSpec

DEVICE = DeviceSpec(
    name="my_device",
    unit_id=4,                 # unique per device; how the aggregator addresses it
    host="0.0.0.0",
    port=5023,                 # only used in per-device mode
    holding_registers={
        1400: RegisterSpec(base=480, min=470, max=490),
    },
    input_registers={
        2000: RegisterSpec(base=100, min=90, max=110),
    },
)
```

Existing devices for reference: `device_1.py` (solar inverter, unit 1),
`device_2.py` (BESS, unit 2), `device_3.py` (utility PV plant, unit 3, holding-only).

## Configuration (env vars)

Set via environment (`env_prefix=""`, so the var name is the field name uppercased).
Defined in [app/settings.py](app/settings.py):

| Variable                 | Default   | Meaning                                                                 |
|--------------------------|-----------|-------------------------------------------------------------------------|
| `AGGREGATOR_ENABLED`     | `true`    | All devices on one server (`MODBUS_HOST:MODBUS_PORT`), addressed by `unit_id`. |
| `MODBUS_HOST`            | `0.0.0.0` | Aggregator bind address.                                                |
| `MODBUS_PORT`            | `502`     | Aggregator TCP port.                                                    |
| `PER_DEVICE_ENABLED`     | `false`   | Also run one server per device on its own `host`/`port` from the device file. |
| `DEFAULT_REGISTER_VALUE` | `0`       | Value for any address not in a device's map.                            |
| `LOG_LEVEL`              | `INFO`    | Python log level.                                                       |
| `RANDOM_SEED`            | *(empty)* | Integer seed for deterministic output; empty string ⇒ non-deterministic. |
| `ZERO_MODE`              | `false`   | Addressing base — see gotcha below.                                     |

At least one of `AGGREGATOR_ENABLED` / `PER_DEVICE_ENABLED` must be true, or the
server exits with an error. Both may run at once.

## Conventions

- `from __future__ import annotations` at the top of every module; full type hints on
  all signatures.
- pydantic v2 models with `ConfigDict(extra="forbid")`; config only through the
  `Settings` model — no inline `os.environ` reads.
- `asyncio` throughout (`async def`, `asyncio.gather`, `asyncio.run`).
- One named logger: `logging.getLogger("mock_modbus")`.
- `snake_case`; private module helpers prefixed `_`.

## Gotchas

- **Aggregator vs per-device.** Default is aggregator only: one server on
  `MODBUS_PORT`, clients pick the device via `unit_id` (1/2/3). Per-device mode puts
  each device on its own port (5020/5021/5022) — enable with `PER_DEVICE_ENABLED=true`.
- **`ZERO_MODE`.** `false` (default) = 1-based addressing — standard Modbus (Modbus
  Poll, most PLCs). `true` = 0-based raw PDU addressing (e.g. the pymodbus client). If
  reads come back as the default value when you expect data, this is the usual cause.
- **`RANDOM_SEED=""`** (empty) means non-deterministic; set an integer for repeatable reads.
- **`RegisterSpec.base`** is documentation/nominal only — it is *not* used at read time
  (reads use `min`/`max`).
- **Writes are ignored** (`setValues` is a no-op).
- The `tests/test_server.py` script is a standalone raw-socket smoke test, not a pytest
  suite, and its hardcoded addresses predate the current device maps.

## Known issue

`make up` uses `docker network create shared-network`, but
[docker-compose.yaml](docker-compose.yaml) expects an **external** network named
`pae-shared-network`. The names don't line up — create the network compose wants with
`docker network create pae-shared-network` before `docker compose up`.
