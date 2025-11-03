# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a bed presence detection system for Home Assistant using an ESP32 microcontroller and LD2410 mmWave radar sensor. The project features:

- **On-device presence engine** running on ESP32 (C++ custom component)
- **Stateful filtering** with temporal debouncing and hysteresis
- **Home Assistant integration** with calibration wizard and operator dashboard
- **End-to-end testing** via C++ unit tests and Python E2E tests

## Monorepo Structure

The repository is organized into distinct subsystems:

- `esphome/` - ESP32 firmware (ESPHome YAML + C++ custom components)
  - `custom_components/` - Core C++ presence engine
  - `packages/` - Reusable ESPHome YAML modules
  - `test/` - C++ unit tests using PlatformIO
- `homeassistant/` - Home Assistant configuration
  - `blueprints/` - Automation blueprints
  - `dashboards/` - Lovelace dashboard YAML
- `tests/e2e/` - Python-based integration tests
- `hardware/` - CAD files for 3D printable parts
- `docs/` - User-facing documentation

## Development Commands

### ESPHome Firmware (run from `esphome/` directory)

**Compile firmware:**
```bash
cd esphome
esphome compile bed-presence-detector.yaml
```

**Run C++ unit tests:**
```bash
cd esphome
platformio test -e native
```

**Flash to device:**
```bash
cd esphome
esphome run bed-presence-detector.yaml
```

### End-to-End Tests (run from `tests/e2e/` directory)

**Install dependencies:**
```bash
cd tests/e2e
pip install -r requirements.txt
```

**Run tests:**
```bash
export HA_URL="ws://your-ha-instance:8123/api/websocket"
export HA_TOKEN="your-long-lived-access-token"
pytest
```

## Development Workflow

1. **Phase 1: Firmware Development**
   - Work in `esphome/` directory
   - Compile firmware with `esphome compile` to validate syntax
   - Run `platformio test -e native` for fast C++ unit test feedback
   - Only flash to device after compilation and tests pass

2. **Phase 2: Home Assistant Configuration**
   - Deploy dashboard from `homeassistant/dashboards/`
   - Deploy blueprints from `homeassistant/blueprints/`
   - Create required helpers per `homeassistant/configuration_helpers.yaml.example`

3. **Phase 3: Integration Testing**
   - Run E2E tests from `tests/e2e/` with live Home Assistant instance
   - Requires configured device and HA credentials

## Key Architecture Concepts

### Presence Engine Design

The core presence detection logic runs entirely on the ESP32 as a C++ custom component. This ensures:
- Fast response times (no Wi-Fi dependency)
- High reliability (continues functioning if Home Assistant is down)
- Sophisticated state machine with debouncing to prevent flapping

The engine processes mmWave radar data through:
1. Threshold comparison (configurable via Home Assistant)
2. Temporal debouncing (configurable delay timers)
3. Hysteresis to prevent oscillation
4. State machine transitions with reason tracking

### Home Assistant Integration

The Home Assistant side provides:
- **Calibration Wizard**: Guided UI flow using Home Assistant helpers and scripts
- **Operator Dashboard**: Live visualization of sensor values, thresholds, and state reasons
- **Configuration Interface**: Exposes tunable parameters (thresholds, debounce timers) as entities

## Testing Strategy

- **C++ Unit Tests**: Test presence engine state machine logic in isolation (fast, no hardware required)
- **ESPHome Compilation**: Validates YAML configuration and C++ compilation (catches syntax errors)
- **E2E Integration Tests**: Verify full system integration with live Home Assistant and device

## Environment Setup

This repository is designed for GitHub Codespaces with automatic environment setup via `.devcontainer/devcontainer.json`:
- ESPHome CLI
- PlatformIO (for C++ testing)
- Python 3 with pytest, yamllint, black

## Important Implementation Details

### ESPHome Custom Component Structure

The custom component is located in `esphome/custom_components/bed_presence_engine/`:
- `__init__.py` - ESPHome component schema and configuration validation
- `bed_presence.h` - C++ header defining the BedPresenceEngine class and state machine
- `bed_presence.cpp` - Implementation of the presence detection logic

The component inherits from both `Component` and `BinarySensor` to integrate with ESPHome's lifecycle.

### State Machine States

The presence engine uses a 4-state machine:
1. `VACANT` - No presence detected
2. `DEBOUNCING_OCCUPIED` - Presence signal detected, waiting for confirmation
3. `OCCUPIED` - Confirmed presence
4. `DEBOUNCING_VACANT` - Absence signal detected, waiting for confirmation

Hysteresis is implemented via separate thresholds: `occupied_threshold` > `vacant_threshold`.

### ESPHome Package System

Configuration is modularized using ESPHome packages:
- `hardware_m5stack_ld2410.yaml` - Hardware-specific config (UART, GPIO pins, LD2410 sensor)
- `presence_engine.yaml` - Presence engine configuration and tuning entities
- `services_calibration.yaml` - ESPHome services for calibration workflow
- `diagnostics.yaml` - Device health monitoring sensors

The main entry point `bed-presence-detector.yaml` includes all packages.

### Secrets Management

Create `esphome/secrets.yaml` from `esphome/secrets.yaml.example` before compiling. Never commit the actual secrets file.

### CI/CD Workflows

- `compile_firmware.yml` - Validates ESPHome compilation and runs C++ unit tests on every push to esphome/
- `lint_yaml.yml` - Validates YAML syntax across the repository

### Known Limitations

- E2E tests require a Home Assistant WebSocket client library (currently placeholder in requirements.txt)
- C++ unit tests are structural placeholders - full test implementation requires mocking ESPHome framework
- Hardware mounting solutions are placeholder STL files
