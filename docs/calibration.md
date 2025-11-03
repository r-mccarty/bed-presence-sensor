# Calibration Guide

Proper calibration is essential for reliable bed presence detection. This guide walks you through the calibration process.

## Why Calibration Matters

The LD2410 radar sensor returns energy values that vary based on:
- Room size and layout
- Bed size and materials
- Mattress type
- Body position and movement

Calibration helps the system learn the typical energy levels for your specific setup.

## Calibration Process

### Step 1: Vacant Calibration

1. Ensure the bed is completely empty
2. In the Home Assistant dashboard, click "Start Vacant Calibration"
3. Wait 30 seconds while the system samples energy levels
4. The system records the maximum energy level observed while vacant

### Step 2: Occupied Calibration

1. Lie down on the bed in your normal sleeping position
2. Click "Start Occupied Calibration"
3. Remain still for 30 seconds
4. The system records the minimum energy level observed while occupied

### Step 3: Review and Apply

1. The system calculates optimal thresholds with a safety margin
2. Review the calculated thresholds in the dashboard
3. Click "Apply Calibration Results" to save the settings

## Fine-Tuning

After initial calibration, you may need to adjust:

- **Debounce Timers**: Increase if you experience false positives during minor movements
- **Thresholds**: Adjust manually if automatic calibration doesn't work for your scenario

## Best Practices

- Calibrate in the environment where the sensor will be used
- Perform calibration during quiet times (minimal household activity)
- Re-calibrate if you change your mattress or bedding significantly
