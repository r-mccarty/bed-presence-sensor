# Phase 2 Integration Testing Guide

This guide covers testing and monitoring tools for validating the Phase 2 presence detection system.

## Quick Start

### Option 1: Real-time Monitoring (Recommended for First-Time Testing)

Monitor your system in real-time to see how raw energy values map to z-scores and state transitions:

```bash
# From ubuntu-node (recommended - no SSH tunnel needed)
ssh ubuntu-node
cd ~/bed-presence-sensor
python3 scripts/monitor_phase2.py --duration 60 --samples 30 --verbose

# From Codespace (requires SSH tunnel)
# Terminal 1: Create tunnel
ssh -L 8123:192.168.0.148:8123 ubuntu-node

# Terminal 2: Run monitor
python3 scripts/monitor_phase2.py --duration 60 --samples 30 --verbose
```

**What it shows:**
- Raw LD2410 energy readings (%)
- Calculated z-scores (σ)
- Current presence state (PRESENT/VACANT)
- State transitions with timestamps
- Debounce timer configuration
- Session statistics and validation checks

### Option 2: Automated E2E Test Suite

Run comprehensive integration tests to validate all Phase 2 functionality:

```bash
# From ubuntu-node (recommended)
ssh ubuntu-node
cd ~/bed-presence-sensor/tests/e2e
pytest -v

# Run specific Phase 2 tests only
pytest -v -k "phase2"

# From Codespace (requires SSH tunnel)
# Terminal 1: Create tunnel
ssh -L 8123:192.168.0.148:8123 ubuntu-node

# Terminal 2: Run tests
cd /workspaces/bed-presence-sensor/tests/e2e
pytest -v -k "phase2"
```

**Tests included:**
- ✅ Debounce timer entities exist
- ✅ Debounce timer updates work
- ✅ State machine transitions properly
- ✅ Z-score calculations are correct
- ✅ Hysteresis gap is maintained
- ✅ Raw sensor data is available

## Monitoring Script Options

### Basic Usage

```bash
# Monitor for 60 seconds with 30 samples
python3 scripts/monitor_phase2.py

# Monitor for 2 minutes with 60 samples
python3 scripts/monitor_phase2.py --duration 120 --samples 60

# Show detailed state information
python3 scripts/monitor_phase2.py --verbose

# Save results to CSV for analysis
python3 scripts/monitor_phase2.py --csv results.csv
```

### Understanding the Output

**Real-time Display:**
```
2025-11-08 14:23:45.123 | Energy:  12.45% | Z-score:  +1.64σ | State: ○ VACANT
2025-11-08 14:23:47.456 | Energy:  45.67% | Z-score: +11.13σ | State: ✓ PRESENT [VACANT → PRESENT]
```

- **Energy**: Raw LD2410 still energy reading (0-100%)
- **Z-score**: Normalized value in standard deviations from baseline
- **State**: Current presence detection state with transition markers

**Session Analysis:**
- Baseline configuration (μ, σ, thresholds)
- Debounce timer settings
- Energy and z-score statistics (min, max, mean, range)
- State transition count and timing
- Validation checks for Phase 2 functionality

### CSV Export

The `--csv` option saves all data to a CSV file for analysis in Excel, Python, or other tools:

```bash
python3 scripts/monitor_phase2.py --duration 120 --samples 60 --csv session_$(date +%Y%m%d_%H%M%S).csv
```

**CSV Columns:**
- `timestamp`: Sample collection time
- `energy_%`: Raw energy reading
- `z_score`: Calculated z-score
- `presence_state`: PRESENT or VACANT
- `state_reason`: State machine reason text
- `k_on`, `k_off`: Threshold multipliers
- `on_threshold_%`, `off_threshold_%`: Actual threshold values
- `on_debounce_ms`, `off_debounce_ms`, `abs_clear_delay_ms`: Debounce timers

## Test Scenarios

### Scenario 1: Validate Empty Bed Baseline

**Goal**: Verify that z-scores are near zero when bed is empty

```bash
# Ensure bed is completely empty
python3 scripts/monitor_phase2.py --duration 60 --samples 30 --verbose

# Expected results:
# - Energy values should be close to μ=6.7%
# - Z-scores should be in range -2σ to +2σ
# - State should remain VACANT throughout
# - No state transitions
```

### Scenario 2: Validate Occupied Bed Detection

**Goal**: Verify that presence is detected and debouncing works

```bash
# Lie down in bed and remain still
python3 scripts/monitor_phase2.py --duration 60 --samples 30 --verbose

# Expected results:
# - Energy values significantly higher than baseline
# - Z-scores > k_on threshold (default 9.0σ)
# - State transitions: VACANT → PRESENT after on_debounce_ms (3000ms default)
# - State remains PRESENT while energy is high
```

### Scenario 3: Test Debounce Effectiveness

**Goal**: Verify that rapid movements don't cause state oscillation

```bash
# Move around in bed, shift positions, toss/turn
python3 scripts/monitor_phase2.py --duration 120 --samples 60 --verbose --csv debounce_test.csv

# Expected results:
# - Energy may fluctuate during movement
# - State should NOT rapidly oscillate (Phase 2 improvement)
# - Debounce timers prevent false negatives
# - Absolute clear delay prevents premature VACANT transitions
```

### Scenario 4: Tuning Validation

**Goal**: Compare before/after results when tuning parameters

```bash
# Collect baseline with current settings
python3 scripts/monitor_phase2.py --duration 60 --csv before_tuning.csv

# Adjust parameters via Home Assistant UI
# - Change k_on, k_off for threshold tuning
# - Change debounce timers for temporal filtering

# Collect data with new settings
python3 scripts/monitor_phase2.py --duration 60 --csv after_tuning.csv

# Compare CSV files to see impact of tuning
```

## E2E Test Suite Details

### Running Full Test Suite

```bash
cd tests/e2e
pytest -v
```

**Test Results:**
```
test_device_is_connected PASSED
test_presence_sensor_exists PASSED
test_threshold_entities_exist PASSED
test_update_threshold_via_service PASSED
test_calibration_service_exists PASSED
test_reset_to_defaults PASSED
test_state_reason_sensor PASSED
test_phase2_debounce_entities_exist PASSED
test_phase2_update_debounce_timers PASSED
test_phase2_state_machine_monitoring PASSED
test_phase2_z_score_calculation PASSED
test_phase2_hysteresis_validation PASSED
test_phase2_sensor_raw_data_available PASSED
```

### Running Specific Tests

```bash
# Only Phase 2 tests
pytest -v -k "phase2"

# Only connection tests
pytest -v -k "connected or sensor_exists"

# Only threshold tests
pytest -v -k "threshold"

# Only debounce tests
pytest -v -k "debounce"
```

### Test Debugging

Enable verbose output to see detailed assertion information:

```bash
pytest -vv -s
```

Run a single test function:

```bash
pytest -v tests/e2e/test_calibration_flow.py::test_phase2_state_machine_monitoring
```

## Troubleshooting

### "Connection Error" when running from Codespace

**Problem**: Cannot reach Home Assistant at 192.168.0.148

**Solution**: Create SSH tunnel first:
```bash
# Terminal 1
ssh -L 8123:192.168.0.148:8123 ubuntu-node
# Keep this running

# Terminal 2
python3 scripts/monitor_phase2.py
```

**Better Solution**: Run directly on ubuntu-node:
```bash
ssh ubuntu-node "cd ~/bed-presence-sensor && python3 scripts/monitor_phase2.py"
```

### "HA_TOKEN not found"

**Problem**: Missing authentication credentials

**Solution**: Copy `.env.local` from ubuntu-node:
```bash
ssh ubuntu-node "cat ~/bed-presence-sensor/.env.local" > /workspaces/bed-presence-sensor/.env.local
```

### "Sensor unavailable"

**Problem**: M5Stack device is not connected to Home Assistant

**Solution**:
1. Check device is powered on
2. Verify WiFi connection: Settings → Devices → Bed Presence Detector
3. Check ESPHome logs for connection errors
4. Reflash firmware if needed: `ssh ubuntu-node "~/flash-firmware.sh"`

### Baseline values don't match firmware

**Problem**: Monitoring script reads wrong μ/σ values

**Solution**: The script reads from `bed_presence.h`. Verify the file has correct values:
```bash
grep -A 4 "mu_still_" esphome/custom_components/bed_presence_engine/bed_presence.h
```

Should show:
```cpp
float mu_still_{6.7f};    // Mean still energy
float sigma_still_{3.5f}; // Std dev still energy
```

## Next Steps After Testing

### If All Tests Pass ✅

Your Phase 2 system is working correctly! Consider:
- Fine-tuning debounce timers based on your usage patterns
- Documenting your optimal threshold values
- Setting up automations using the presence sensor

### If Tests Fail ❌

Check the failure type:

**Debounce entity tests fail:**
- Verify firmware has Phase 2 code deployed
- Check `esphome/packages/presence_engine.yaml` has debounce entities
- Reflash firmware: `ssh ubuntu-node "~/sync-and-flash.sh"`

**State machine tests fail:**
- Check ESPHome device logs for errors
- Verify sensor is getting valid readings
- Recalibrate baseline if sensor position changed

**Z-score tests fail:**
- Verify baseline values are correct in firmware
- Check `state_reason` sensor format matches expected pattern
- Review `bed_presence.cpp` for state reason formatting

## Performance Benchmarks

Expected Phase 2 performance characteristics:

**Detection Latency:**
- Empty → Occupied: ~3 seconds (on_debounce_ms)
- Occupied → Empty: ~35 seconds (abs_clear_delay_ms + off_debounce_ms)

**Stability:**
- False positive rate: <1% (with proper calibration)
- State oscillations: 0 (debouncing prevents rapid changes)

**Sensitivity:**
- Can detect: Person lying still in bed
- Can detect: Person sleeping (breathing motion)
- Ignores: Environmental changes (doors, fans, pets outside sensor range)

## Additional Resources

- **Full specification**: `docs/presence-engine-spec.md`
- **Phase 2 deployment guide**: `docs/phase2-completion-steps.md`
- **Troubleshooting**: `docs/troubleshooting.md`
- **Calibration guide**: `docs/calibration.md`

---

**Questions or Issues?**

If you encounter problems not covered here:
1. Check ESPHome device logs in Home Assistant
2. Review `docs/troubleshooting.md`
3. Verify firmware version matches Phase 2 implementation
4. Recalibrate baseline statistics if needed
