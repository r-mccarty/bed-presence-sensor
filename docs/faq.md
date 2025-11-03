# Frequently Asked Questions

## General Questions

### What is the detection range of the LD2410 sensor?

The LD2410 can detect presence up to 6 meters, but for bed detection we typically configure it for 1-2 meters for best accuracy.

### Can I use this with a different ESP32 board?

Yes! The code is portable. You'll need to update the pin assignments in `packages/hardware_m5stack_ld2410.yaml` to match your board.

### Does this work with adjustable beds?

Yes, the sensor detects presence regardless of bed position. However, you may need to recalibrate if the bed adjustment significantly changes the sensor's view.

### Will this detect pets on the bed?

Possibly. The sensor detects any presence, not specifically humans. You may need to tune thresholds to account for pet size and movement.

## Technical Questions

### Why use still energy instead of moving energy?

Still energy is more reliable for bed occupancy detection because people are mostly stationary while sleeping. Moving energy can be useful for detecting restlessness but is more prone to false positives.

### What's the purpose of the debounce timers?

Debounce timers prevent rapid state changes due to momentary fluctuations. For example, brief movements near the bed won't immediately trigger an "occupied" state.

### Can I use multiple sensors for a king-size bed?

Yes, but you'll need to deploy multiple ESPHome devices (one per sensor) and combine their states in Home Assistant using a template sensor.

### How does hysteresis prevent flapping?

Hysteresis uses different thresholds for transitions in each direction. The occupied threshold is higher than the vacant threshold, creating a "dead zone" that prevents oscillation around a single value.

## Development Questions

### How do I run the C++ unit tests locally?

```bash
cd esphome
platformio test -e native
```

### Can I test without hardware?

Yes! The C++ unit tests run on your development machine without any hardware. However, full E2E tests require a physical device and Home Assistant instance.

### How do I contribute to this project?

See the GitHub repository for contribution guidelines. All contributions are welcome!
