# Quickstart Guide

This guide will help you get your bed presence detector up and running quickly.

## Prerequisites

- M5Stack ESP32 device
- LD2410 mmWave radar sensor
- Home Assistant instance (version 2023.1 or later)
- USB cable for flashing

## Hardware Assembly

1. Connect the LD2410 sensor to your M5Stack device:
   - TX (LD2410) → GPIO16 (M5Stack)
   - RX (LD2410) → GPIO17 (M5Stack)
   - VCC → 5V
   - GND → GND

2. See the wiring diagram in `docs/assets/wiring_diagram.png` for visual reference

## Firmware Installation

1. Clone this repository
2. Copy `esphome/secrets.yaml.example` to `esphome/secrets.yaml` and fill in your Wi-Fi credentials
3. Compile and flash the firmware:
   ```bash
   cd esphome
   esphome run bed-presence-detector.yaml
   ```
4. Follow the prompts to flash via USB or OTA

## Home Assistant Configuration

1. The device should auto-discover in Home Assistant via ESPHome integration
2. Copy the dashboard configuration to your Home Assistant instance
3. Create the required helpers (see `homeassistant/configuration_helpers.yaml.example`)
4. Reload your Home Assistant configuration

## Calibration

1. Open the Bed Presence Dashboard in Home Assistant
2. Navigate to the "Calibration Wizard" tab
3. Follow the on-screen instructions to calibrate vacant and occupied states

## Next Steps

- See [calibration.md](calibration.md) for detailed calibration instructions
- See [troubleshooting.md](troubleshooting.md) if you encounter issues
