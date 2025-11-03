#include "bed_presence.h"
#include "esphome/core/log.h"

namespace esphome {
namespace bed_presence_engine {

static const char *const TAG = "bed_presence_engine";

void BedPresenceEngine::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Bed Presence Engine...");
  ESP_LOGCONFIG(TAG, "  Occupied Threshold: %d", this->occupied_threshold_);
  ESP_LOGCONFIG(TAG, "  Vacant Threshold: %d", this->vacant_threshold_);
  ESP_LOGCONFIG(TAG, "  Debounce Occupied: %u ms", this->debounce_occupied_ms_);
  ESP_LOGCONFIG(TAG, "  Debounce Vacant: %u ms", this->debounce_vacant_ms_);

  // Initialize to vacant state
  this->state_ = VACANT;
  this->publish_state(false);

  if (this->state_reason_sensor_ != nullptr) {
    this->state_reason_sensor_->publish_state("Initial state: vacant");
  }
}

void BedPresenceEngine::loop() {
  // Check if we have a valid energy reading
  if (this->energy_sensor_ == nullptr || !this->energy_sensor_->has_state()) {
    return;
  }

  float energy = this->energy_sensor_->state;
  this->process_energy_reading(energy);
}

void BedPresenceEngine::process_energy_reading(float energy) {
  switch (this->state_) {
    case VACANT:
      // Check if energy exceeds occupied threshold
      if (energy >= this->occupied_threshold_) {
        this->transition_to_state(DEBOUNCING_OCCUPIED, "Energy exceeded occupied threshold");
      }
      break;

    case DEBOUNCING_OCCUPIED:
      // Check if energy dropped back below threshold
      if (energy < this->occupied_threshold_) {
        this->transition_to_state(VACANT, "Energy dropped during debounce");
      }
      // Check if debounce period completed
      else if (this->is_debounce_complete(this->debounce_occupied_ms_)) {
        this->transition_to_state(OCCUPIED, "Debounce period completed");
        this->publish_state(true);
      }
      break;

    case OCCUPIED:
      // Check if energy dropped below vacant threshold (hysteresis)
      if (energy <= this->vacant_threshold_) {
        this->transition_to_state(DEBOUNCING_VACANT, "Energy dropped below vacant threshold");
      }
      break;

    case DEBOUNCING_VACANT:
      // Check if energy rose back above threshold
      if (energy > this->vacant_threshold_) {
        this->transition_to_state(OCCUPIED, "Energy increased during debounce");
      }
      // Check if debounce period completed
      else if (this->is_debounce_complete(this->debounce_vacant_ms_)) {
        this->transition_to_state(VACANT, "Debounce period completed");
        this->publish_state(false);
      }
      break;
  }
}

void BedPresenceEngine::transition_to_state(PresenceState new_state, const char *reason) {
  if (this->state_ != new_state) {
    ESP_LOGD(TAG, "State transition: %d -> %d. Reason: %s", this->state_, new_state, reason);
    this->state_ = new_state;
    this->debounce_start_time_ = millis();

    if (this->state_reason_sensor_ != nullptr) {
      this->state_reason_sensor_->publish_state(reason);
    }
  }
}

bool BedPresenceEngine::is_debounce_complete(uint32_t debounce_ms) {
  return (millis() - this->debounce_start_time_) >= debounce_ms;
}

void BedPresenceEngine::update_thresholds(int occupied, int vacant) {
  ESP_LOGI(TAG, "Updating thresholds: occupied=%d, vacant=%d", occupied, vacant);
  this->occupied_threshold_ = occupied;
  this->vacant_threshold_ = vacant;
}

void BedPresenceEngine::update_debounce_timers(uint32_t occupied_ms, uint32_t vacant_ms) {
  ESP_LOGI(TAG, "Updating debounce timers: occupied=%u ms, vacant=%u ms", occupied_ms, vacant_ms);
  this->debounce_occupied_ms_ = occupied_ms;
  this->debounce_vacant_ms_ = vacant_ms;
}

}  // namespace bed_presence_engine
}  // namespace esphome
