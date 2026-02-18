# Mock Modbus TCP Server

Dynamic Modbus TCP register simulator for holding and input registers. Values are generated randomly within configured bounds on every read request.

## Quick Start

```bash
docker network create pae-shared-network  # if not already created
docker compose up --build
```

The server listens on port **502** by default.

## Environment Variables

| Variable                 | Default   | Description                        |
|--------------------------|-----------|------------------------------------|
| `MODBUS_HOST`            | `0.0.0.0` | Bind address                       |
| `MODBUS_PORT`            | `502`     | TCP port                           |
| `MODBUS_UNIT_ID`         | `1`       | Modbus slave/unit ID               |
| `DEFAULT_REGISTER_VALUE` | `0`       | Value for undefined addresses      |
| `LOG_LEVEL`              | `INFO`    | Python log level                   |
| `RANDOM_SEED`            | *(empty)* | Optional seed for deterministic output |

## Supported Function Codes

- **03** — Read Holding Registers
- **04** — Read Input Registers

All other function codes return Modbus exception 01 (Illegal Function).

## Register Definitions

Edit `app/mock_data.py` to configure register address ranges and value bounds.

## Testing

```python
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("localhost", port=502)
client.connect()

result = client.read_holding_registers(0, 4, slave=1)
print(result.registers)  # e.g. [482, 37, 0, 0]

result = client.read_input_registers(50, 2, slave=1)
print(result.registers)  # e.g. [153, 0]

client.close()
```
