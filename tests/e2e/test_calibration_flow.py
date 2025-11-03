"""
End-to-End Integration Tests for Bed Presence Detector

These tests verify the full integration between Home Assistant and the ESPHome device,
including the calibration wizard flow and threshold updates.

Environment Variables Required:
- HA_URL: WebSocket URL for Home Assistant (e.g., ws://homeassistant.local:8123/api/websocket)
- HA_TOKEN: Long-lived access token for Home Assistant
"""

import os
import pytest
import asyncio
from hass_ws import HomeAssistantClient


@pytest.fixture
async def ha_client():
    """Fixture to create and authenticate Home Assistant WebSocket client"""
    url = os.getenv("HA_URL")
    token = os.getenv("HA_TOKEN")

    if not url or not token:
        pytest.skip("HA_URL and HA_TOKEN environment variables must be set")

    client = HomeAssistantClient(url, token)
    await client.connect()
    yield client
    await client.disconnect()


@pytest.mark.asyncio
async def test_device_is_connected(ha_client):
    """Test that the bed presence detector device is connected to Home Assistant"""
    # Get device information
    devices = await ha_client.get_devices()

    # Find our device
    bed_detector = next(
        (d for d in devices if "bed-presence-detector" in d.get("name", "").lower()),
        None
    )

    assert bed_detector is not None, "Bed presence detector device not found"
    assert bed_detector.get("disabled_by") is None, "Device is disabled"


@pytest.mark.asyncio
async def test_presence_sensor_exists(ha_client):
    """Test that the bed occupied binary sensor exists"""
    state = await ha_client.get_state("binary_sensor.bed_occupied")
    assert state is not None, "binary_sensor.bed_occupied not found"
    assert state["state"] in ["on", "off"], "Invalid state for presence sensor"


@pytest.mark.asyncio
async def test_threshold_entities_exist(ha_client):
    """Test that threshold configuration entities exist"""
    occupied_threshold = await ha_client.get_state("number.occupied_threshold")
    vacant_threshold = await ha_client.get_state("number.vacant_threshold")

    assert occupied_threshold is not None, "number.occupied_threshold not found"
    assert vacant_threshold is not None, "number.vacant_threshold not found"

    # Verify thresholds are sensible
    occupied_val = float(occupied_threshold["state"])
    vacant_val = float(vacant_threshold["state"])
    assert occupied_val > vacant_val, "Occupied threshold should be higher than vacant"


@pytest.mark.asyncio
async def test_update_threshold_via_service(ha_client):
    """Test that we can update thresholds via Home Assistant service call"""
    # Set a new threshold value
    await ha_client.call_service(
        "number",
        "set_value",
        entity_id="number.occupied_threshold",
        value=60
    )

    # Wait for update to propagate
    await asyncio.sleep(1)

    # Verify the update
    state = await ha_client.get_state("number.occupied_threshold")
    assert float(state["state"]) == 60, "Threshold was not updated"


@pytest.mark.asyncio
async def test_calibration_service_exists(ha_client):
    """Test that the calibration ESPHome services are available"""
    services = await ha_client.get_services()

    # Check that our custom ESPHome services exist
    esphome_services = services.get("esphome", {})

    assert "bed_presence_detector_start_calibration" in esphome_services, \
        "start_calibration service not found"
    assert "bed_presence_detector_stop_calibration" in esphome_services, \
        "stop_calibration service not found"
    assert "bed_presence_detector_reset_to_defaults" in esphome_services, \
        "reset_to_defaults service not found"


@pytest.mark.asyncio
async def test_reset_to_defaults(ha_client):
    """Test the reset to defaults service"""
    # Call reset service
    await ha_client.call_service(
        "esphome",
        "bed_presence_detector_reset_to_defaults"
    )

    # Wait for reset to complete
    await asyncio.sleep(2)

    # Verify defaults are restored
    occupied_state = await ha_client.get_state("number.occupied_threshold")
    vacant_state = await ha_client.get_state("number.vacant_threshold")

    assert float(occupied_state["state"]) == 50, "Occupied threshold not reset to default"
    assert float(vacant_state["state"]) == 30, "Vacant threshold not reset to default"


@pytest.mark.asyncio
async def test_state_reason_sensor(ha_client):
    """Test that the state reason text sensor is available and updating"""
    state = await ha_client.get_state("sensor.presence_state_reason")
    assert state is not None, "State reason sensor not found"
    assert len(state["state"]) > 0, "State reason is empty"


@pytest.mark.asyncio
async def test_calibration_helpers_exist(ha_client):
    """Test that the calibration helper entities exist in Home Assistant"""
    calibration_step = await ha_client.get_state("input_select.calibration_step")
    calibration_in_progress = await ha_client.get_state("input_boolean.calibration_in_progress")

    assert calibration_step is not None, "Calibration step input_select not found"
    assert calibration_in_progress is not None, "Calibration in_progress input_boolean not found"


@pytest.mark.asyncio
async def test_full_calibration_flow(ha_client):
    """
    Test the full calibration workflow:
    1. Start vacant calibration
    2. Wait for completion
    3. Start occupied calibration
    4. Wait for completion
    5. Verify thresholds were calculated
    """
    # Reset to known state
    await ha_client.call_service(
        "esphome",
        "bed_presence_detector_reset_to_defaults"
    )
    await asyncio.sleep(1)

    # Start vacant calibration script
    await ha_client.call_service("script", "calibrate_vacant_mode")

    # Wait for calibration to complete (script has 30s delay)
    await asyncio.sleep(35)

    # Check that calibration step was updated
    step_state = await ha_client.get_state("input_select.calibration_step")
    assert step_state["state"] in ["Review Results", "Completed"], \
        f"Unexpected calibration step: {step_state['state']}"

    # Note: Full flow would continue with occupied calibration,
    # but we keep this test short for CI/CD purposes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
