# Bambu Heater Control

A small Python tool/package to automate temperature control for Bambu Lab printers using TP-Link Smart Strips (HS300).  

## Features

- Monitors the chamber temperature by subscribing to printer MQTT messages.
- Looks up desired temperature based on the currently loaded filament type.
- Automates turning on/off a TP-Link smart power strip outlet to maintain the target temperature.


## Installation

### Local Development

1. **Clone** the repository:
   ```bash
   git clone https://github.com/YourUsername/bambulabs_heater_mod.git
   cd bambulabs_heater_mod
   ```

2. **Install** in editable mode (so changes are reflected immediately):
   ```bash
   pip install -e .
   ```
   Or use [poetry](https://python-poetry.org/) if you prefer:
   ```bash
   poetry install
   ```

### Usage

After installation, you can run the package in several ways:

1. **Module mode**:
   ```bash
   python -m bambu_heater --help
   ```
   You can pass `--host` and `--password` arguments directly:
   ```bash
   python -m bambu_heater --host 192.168.42.87 --password 12345678
   ```

2. **Console script** (if you set one up in `pyproject.toml`—see below):
   ```bash
   bambu-heater --host 192.168.42.87 --password 12345678
   ```

## Environment Variables

If you don’t provide `--host` or `--password` on the command line, the tool looks for:
- `BAMBU_PRINTER_IP`
- `BAMBU_PRINTER_ACCESS_CODE`

```bash
export BAMBU_PRINTER_IP="192.168.42.87"
export BAMBU_PRINTER_ACCESS_CODE="12345678"
python -m bambu_heater
```

## Contributing

1. **Fork** the repository and create your branch from `main`.
2. **Make changes** and ensure tests pass (add your own tests as needed).
3. **Submit a pull request** for review.

## License

[BSD 3-Clause](LICENSE) (or choose a license that suits your needs).
