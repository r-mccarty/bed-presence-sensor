"""
Bed Presence Engine Custom Component for ESPHome

This component implements a sophisticated presence detection engine with:
- Temporal debouncing
- Hysteresis-based thresholding
- State machine with reason tracking
"""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, binary_sensor, text_sensor
from esphome.const import (
    CONF_ID,
    CONF_NAME,
    UNIT_EMPTY,
    DEVICE_CLASS_OCCUPANCY,
)

DEPENDENCIES = []
AUTO_LOAD = ["sensor", "binary_sensor", "text_sensor"]

bed_presence_engine_ns = cg.esphome_ns.namespace("bed_presence_engine")
BedPresenceEngine = bed_presence_engine_ns.class_("BedPresenceEngine", cg.Component)

# Configuration keys
CONF_ENERGY_SENSOR = "energy_sensor"
CONF_OCCUPIED_THRESHOLD = "occupied_threshold"
CONF_VACANT_THRESHOLD = "vacant_threshold"
CONF_DEBOUNCE_OCCUPIED = "debounce_occupied"
CONF_DEBOUNCE_VACANT = "debounce_vacant"
CONF_STATE_REASON = "state_reason"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(BedPresenceEngine),
        cv.Required(CONF_ENERGY_SENSOR): cv.use_id(sensor.Sensor),
        cv.Optional(CONF_OCCUPIED_THRESHOLD, default=50): cv.int_range(min=0, max=100),
        cv.Optional(CONF_VACANT_THRESHOLD, default=30): cv.int_range(min=0, max=100),
        cv.Optional(CONF_DEBOUNCE_OCCUPIED, default=2000): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_DEBOUNCE_VACANT, default=5000): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_NAME): cv.string,
        cv.Optional(CONF_STATE_REASON): text_sensor.text_sensor_schema(),
    }
).extend(cv.COMPONENT_SCHEMA).extend(binary_sensor.binary_sensor_schema(device_class=DEVICE_CLASS_OCCUPANCY))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await binary_sensor.register_binary_sensor(var, config)

    energy_sensor = await cg.get_variable(config[CONF_ENERGY_SENSOR])
    cg.add(var.set_energy_sensor(energy_sensor))

    cg.add(var.set_occupied_threshold(config[CONF_OCCUPIED_THRESHOLD]))
    cg.add(var.set_vacant_threshold(config[CONF_VACANT_THRESHOLD]))
    cg.add(var.set_debounce_occupied(config[CONF_DEBOUNCE_OCCUPIED]))
    cg.add(var.set_debounce_vacant(config[CONF_DEBOUNCE_VACANT]))

    if CONF_STATE_REASON in config:
        reason_sensor = await text_sensor.new_text_sensor(config[CONF_STATE_REASON])
        cg.add(var.set_state_reason_sensor(reason_sensor))
