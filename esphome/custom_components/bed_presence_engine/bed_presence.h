#pragma once

#include "esphome/core/component.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"

namespace esphome {
namespace bed_presence_engine {

/**
 * Presence engine states
 */
enum PresenceState {
  VACANT,
  DEBOUNCING_OCCUPIED,
  OCCUPIED,
  DEBOUNCING_VACANT
};

/**
 * BedPresenceEngine Component
 *
 * Implements a stateful presence detection engine with:
 * - Hysteresis-based threshold comparison
 * - Temporal debouncing with separate timers for occupied/vacant
 * - State transition reason tracking for transparency
 */
class BedPresenceEngine : public Component, public binary_sensor::BinarySensor {
 public:
  void setup() override;
  void loop() override;
  float get_setup_priority() const override { return setup_priority::DATA; }

  // Configuration setters
  void set_energy_sensor(sensor::Sensor *sensor) { energy_sensor_ = sensor; }
  void set_occupied_threshold(int threshold) { occupied_threshold_ = threshold; }
  void set_vacant_threshold(int threshold) { vacant_threshold_ = threshold; }
  void set_debounce_occupied(uint32_t ms) { debounce_occupied_ms_ = ms; }
  void set_debounce_vacant(uint32_t ms) { debounce_vacant_ms_ = ms; }
  void set_state_reason_sensor(text_sensor::TextSensor *sensor) { state_reason_sensor_ = sensor; }

  // Public methods for calibration services
  void update_thresholds(int occupied, int vacant);
  void update_debounce_timers(uint32_t occupied_ms, uint32_t vacant_ms);

 protected:
  // Input sensor
  sensor::Sensor *energy_sensor_{nullptr};

  // Configuration
  int occupied_threshold_{50};
  int vacant_threshold_{30};
  uint32_t debounce_occupied_ms_{2000};
  uint32_t debounce_vacant_ms_{5000};

  // State machine
  PresenceState state_{VACANT};
  uint32_t debounce_start_time_{0};

  // Output sensors
  text_sensor::TextSensor *state_reason_sensor_{nullptr};

  // Internal methods
  void process_energy_reading(float energy);
  void transition_to_state(PresenceState new_state, const char *reason);
  bool is_debounce_complete(uint32_t debounce_ms);
};

}  // namespace bed_presence_engine
}  // namespace esphome
