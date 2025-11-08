#!/usr/bin/env python3
"""
Phase 2 Integration Testing & Monitoring Script

This script monitors the Phase 2 presence detection system in real-time,
showing the relationship between:
- Raw LD2410 energy readings
- Normalized z-scores
- State machine transitions
- Debounce timing

Usage:
    python3 monitor_phase2.py [--duration SECONDS] [--samples N]

Options:
    --duration SECONDS  Total monitoring duration in seconds (default: 60)
    --samples N         Number of samples to collect (default: 30)
    --csv FILE          Save results to CSV file
    --verbose           Show detailed state information

Environment Variables:
    HA_URL: Home Assistant URL (default: http://localhost:8123)
    HA_TOKEN: Long-lived access token (required)
"""

import os
import sys
import time
import argparse
import requests
import csv
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@dataclass
class SensorSnapshot:
    """Snapshot of all relevant sensor states at a point in time"""
    timestamp: str
    energy: float
    z_score: float
    presence_state: bool
    state_reason: str
    k_on: float
    k_off: float
    on_debounce_ms: int
    off_debounce_ms: int
    abs_clear_delay_ms: int


def get_ha_config() -> Tuple[str, str]:
    """Get Home Assistant URL and token from environment or .env.local file."""
    ha_url = os.getenv('HA_URL')
    ha_token = os.getenv('HA_TOKEN')

    # If not in environment, try to load from .env.local
    if not ha_url or not ha_token:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_file = os.path.join(script_dir, '..', '.env.local')

        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('HA_URL=') and not ha_url:
                        ha_url = line.split('=', 1)[1].strip()
                    elif line.startswith('HA_TOKEN=') and not ha_token:
                        ha_token = line.split('=', 1)[1].strip()

    # Use localhost if running on HA host
    if not ha_url:
        ha_url = 'http://localhost:8123'

    if not ha_token:
        print(f"{Colors.FAIL}ERROR: HA_TOKEN not found in environment or .env.local{Colors.ENDC}")
        print(f"Please set the HA_TOKEN environment variable or add it to .env.local")
        sys.exit(1)

    return ha_url, ha_token


def get_entity_state(ha_url: str, ha_token: str, entity_id: str) -> Dict:
    """Get the full state object of an entity."""
    headers = {
        'Authorization': f'Bearer {ha_token}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(
            f'{ha_url}/api/states/{entity_id}',
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(f"HTTP {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to Home Assistant: {e}")


def get_baseline_from_firmware() -> Tuple[float, float]:
    """
    Read baseline values from the firmware source code.

    Returns:
        Tuple of (mu_still, sigma_still)
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    header_file = os.path.join(script_dir, '..', 'esphome', 'custom_components',
                               'bed_presence_engine', 'bed_presence.h')

    mu_still = None
    sigma_still = None

    try:
        with open(header_file, 'r') as f:
            for line in f:
                if 'mu_still_' in line and '{' in line:
                    # Extract value from: float mu_still_{6.7f};
                    value = line.split('{')[1].split('f}')[0]
                    mu_still = float(value)
                elif 'sigma_still_' in line and '{' in line:
                    value = line.split('{')[1].split('f}')[0]
                    sigma_still = float(value)
    except FileNotFoundError:
        print(f"{Colors.WARNING}⚠️  Could not read baseline from bed_presence.h{Colors.ENDC}")
        print(f"Using default values: μ=6.7, σ=3.5")
        return 6.7, 3.5

    if mu_still is None or sigma_still is None:
        return 6.7, 3.5  # Default values from Phase 2

    return mu_still, sigma_still


def calculate_z_score(energy: float, mu: float, sigma: float) -> float:
    """Calculate z-score from raw energy value."""
    if sigma == 0:
        return 0.0
    return (energy - mu) / sigma


def collect_snapshot(ha_url: str, ha_token: str, mu: float, sigma: float) -> SensorSnapshot:
    """Collect a complete snapshot of all sensor states."""

    # Get all entity states
    energy_state = get_entity_state(ha_url, ha_token,
                                     "sensor.bed_presence_detector_ld2410_still_energy")
    presence_state = get_entity_state(ha_url, ha_token,
                                       "binary_sensor.bed_presence_detector_bed_occupied")
    state_reason = get_entity_state(ha_url, ha_token,
                                     "sensor.bed_presence_detector_presence_state_reason")
    k_on_state = get_entity_state(ha_url, ha_token,
                                   "number.bed_presence_detector_k_on_on_threshold_multiplier")
    k_off_state = get_entity_state(ha_url, ha_token,
                                    "number.bed_presence_detector_k_off_off_threshold_multiplier")

    # Get debounce timer entities (Phase 2)
    try:
        on_debounce_state = get_entity_state(ha_url, ha_token,
                                             "number.bed_presence_detector_on_debounce_ms")
        off_debounce_state = get_entity_state(ha_url, ha_token,
                                              "number.bed_presence_detector_off_debounce_ms")
        abs_clear_state = get_entity_state(ha_url, ha_token,
                                           "number.bed_presence_detector_abs_clear_delay_ms")

        on_debounce_ms = int(float(on_debounce_state['state']))
        off_debounce_ms = int(float(off_debounce_state['state']))
        abs_clear_delay_ms = int(float(abs_clear_state['state']))
    except:
        # Default Phase 2 values if entities not found
        on_debounce_ms = 3000
        off_debounce_ms = 5000
        abs_clear_delay_ms = 30000

    # Parse values
    energy = float(energy_state['state'])
    z_score = calculate_z_score(energy, mu, sigma)
    presence = presence_state['state'] == 'on'
    reason = state_reason['state']
    k_on = float(k_on_state['state'])
    k_off = float(k_off_state['state'])

    return SensorSnapshot(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        energy=energy,
        z_score=z_score,
        presence_state=presence,
        state_reason=reason,
        k_on=k_on,
        k_off=k_off,
        on_debounce_ms=on_debounce_ms,
        off_debounce_ms=off_debounce_ms,
        abs_clear_delay_ms=abs_clear_delay_ms
    )


def display_snapshot(snapshot: SensorSnapshot, mu: float, sigma: float,
                     verbose: bool = False, prev_snapshot: Optional[SensorSnapshot] = None):
    """Display a formatted snapshot of current state."""

    # Determine threshold values
    on_threshold = mu + (snapshot.k_on * sigma)
    off_threshold = mu + (snapshot.k_off * sigma)

    # Color code based on state
    if snapshot.presence_state:
        state_color = Colors.OKGREEN
        state_symbol = "✓"
        state_text = "PRESENT"
    else:
        state_color = Colors.OKBLUE
        state_symbol = "○"
        state_text = "VACANT"

    # Check for state transitions
    state_changed = ""
    if prev_snapshot and prev_snapshot.presence_state != snapshot.presence_state:
        if snapshot.presence_state:
            state_changed = f" {Colors.WARNING}[VACANT → PRESENT]{Colors.ENDC}"
        else:
            state_changed = f" {Colors.WARNING}[PRESENT → VACANT]{Colors.ENDC}"

    # Basic display
    print(f"{snapshot.timestamp} | "
          f"Energy: {Colors.OKCYAN}{snapshot.energy:6.2f}%{Colors.ENDC} | "
          f"Z-score: {Colors.OKBLUE}{snapshot.z_score:+6.2f}σ{Colors.ENDC} | "
          f"State: {state_color}{state_symbol} {state_text}{Colors.ENDC}{state_changed}")

    if verbose:
        print(f"  └─ Thresholds: ON={on_threshold:.2f}% (z>{snapshot.k_on:.1f}σ), "
              f"OFF={off_threshold:.2f}% (z<{snapshot.k_off:.1f}σ)")
        print(f"  └─ Debounce: ON={snapshot.on_debounce_ms}ms, "
              f"OFF={snapshot.off_debounce_ms}ms, "
              f"ABS_CLEAR={snapshot.abs_clear_delay_ms}ms")
        print(f"  └─ Reason: {Colors.WARNING}{snapshot.state_reason}{Colors.ENDC}")
        print()


def analyze_session(snapshots: List[SensorSnapshot], mu: float, sigma: float):
    """Analyze the collected session data and display summary statistics."""

    if not snapshots:
        return

    energies = [s.energy for s in snapshots]
    z_scores = [s.z_score for s in snapshots]

    # Count state changes
    state_changes = 0
    for i in range(1, len(snapshots)):
        if snapshots[i].presence_state != snapshots[i-1].presence_state:
            state_changes += 1

    # Calculate time in each state
    present_count = sum(1 for s in snapshots if s.presence_state)
    vacant_count = len(snapshots) - present_count

    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("=" * 80)
    print("  SESSION ANALYSIS")
    print("=" * 80)
    print(f"{Colors.ENDC}")

    print(f"\n{Colors.OKBLUE}Baseline Configuration:{Colors.ENDC}")
    print(f"  μ (mean):              {mu:.2f}%")
    print(f"  σ (std dev):           {sigma:.2f}%")
    print(f"  k_on threshold:        {snapshots[-1].k_on:.1f}σ = {mu + (snapshots[-1].k_on * sigma):.2f}%")
    print(f"  k_off threshold:       {snapshots[-1].k_off:.1f}σ = {mu + (snapshots[-1].k_off * sigma):.2f}%")
    print(f"  Hysteresis gap:        {(snapshots[-1].k_on - snapshots[-1].k_off) * sigma:.2f}%")

    print(f"\n{Colors.OKBLUE}Phase 2 Debounce Configuration:{Colors.ENDC}")
    print(f"  ON debounce:           {snapshots[-1].on_debounce_ms}ms")
    print(f"  OFF debounce:          {snapshots[-1].off_debounce_ms}ms")
    print(f"  Absolute clear delay:  {snapshots[-1].abs_clear_delay_ms}ms")

    print(f"\n{Colors.OKBLUE}Energy Statistics:{Colors.ENDC}")
    print(f"  Min energy:            {min(energies):.2f}%")
    print(f"  Max energy:            {max(energies):.2f}%")
    print(f"  Mean energy:           {sum(energies)/len(energies):.2f}%")
    print(f"  Range:                 {max(energies) - min(energies):.2f}%")

    print(f"\n{Colors.OKBLUE}Z-Score Statistics:{Colors.ENDC}")
    print(f"  Min z-score:           {min(z_scores):+.2f}σ")
    print(f"  Max z-score:           {max(z_scores):+.2f}σ")
    print(f"  Mean z-score:          {sum(z_scores)/len(z_scores):+.2f}σ")

    print(f"\n{Colors.OKBLUE}State Machine Behavior:{Colors.ENDC}")
    print(f"  State transitions:     {state_changes}")
    print(f"  Time PRESENT:          {present_count}/{len(snapshots)} samples ({present_count/len(snapshots)*100:.1f}%)")
    print(f"  Time VACANT:           {vacant_count}/{len(snapshots)} samples ({vacant_count/len(snapshots)*100:.1f}%)")

    # Show state transition log
    if state_changes > 0:
        print(f"\n{Colors.OKBLUE}State Transition Log:{Colors.ENDC}")
        for i in range(1, len(snapshots)):
            if snapshots[i].presence_state != snapshots[i-1].presence_state:
                if snapshots[i].presence_state:
                    print(f"  {snapshots[i].timestamp}: {Colors.OKGREEN}VACANT → PRESENT{Colors.ENDC} "
                          f"(z={snapshots[i].z_score:+.2f}σ, energy={snapshots[i].energy:.2f}%)")
                else:
                    print(f"  {snapshots[i].timestamp}: {Colors.WARNING}PRESENT → VACANT{Colors.ENDC} "
                          f"(z={snapshots[i].z_score:+.2f}σ, energy={snapshots[i].energy:.2f}%)")

    # Phase 2 validation checks
    print(f"\n{Colors.OKBLUE}Phase 2 Validation Checks:{Colors.ENDC}")

    # Check if debouncing is working (no rapid oscillation)
    rapid_changes = 0
    for i in range(1, min(len(snapshots), 10)):
        if snapshots[i].presence_state != snapshots[i-1].presence_state:
            rapid_changes += 1

    if rapid_changes > 3:
        print(f"  {Colors.WARNING}⚠️  High state change rate detected in first 10 samples{Colors.ENDC}")
        print(f"     Consider increasing debounce timers")
    else:
        print(f"  {Colors.OKGREEN}✓{Colors.ENDC} State stability: Good (no rapid oscillation)")

    # Check hysteresis gap
    hysteresis_gap = (snapshots[-1].k_on - snapshots[-1].k_off) * sigma
    if hysteresis_gap < 5.0:
        print(f"  {Colors.WARNING}⚠️  Small hysteresis gap ({hysteresis_gap:.2f}%){Colors.ENDC}")
        print(f"     Consider increasing k_on or decreasing k_off")
    else:
        print(f"  {Colors.OKGREEN}✓{Colors.ENDC} Hysteresis gap: {hysteresis_gap:.2f}% (good)")

    print()


def save_to_csv(snapshots: List[SensorSnapshot], filename: str, mu: float, sigma: float):
    """Save collected data to CSV file."""

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'energy_%', 'z_score', 'presence_state',
                     'state_reason', 'k_on', 'k_off', 'on_threshold_%', 'off_threshold_%',
                     'on_debounce_ms', 'off_debounce_ms', 'abs_clear_delay_ms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for s in snapshots:
            writer.writerow({
                'timestamp': s.timestamp,
                'energy_%': f"{s.energy:.2f}",
                'z_score': f"{s.z_score:.2f}",
                'presence_state': 'PRESENT' if s.presence_state else 'VACANT',
                'state_reason': s.state_reason,
                'k_on': f"{s.k_on:.1f}",
                'k_off': f"{s.k_off:.1f}",
                'on_threshold_%': f"{mu + (s.k_on * sigma):.2f}",
                'off_threshold_%': f"{mu + (s.k_off * sigma):.2f}",
                'on_debounce_ms': s.on_debounce_ms,
                'off_debounce_ms': s.off_debounce_ms,
                'abs_clear_delay_ms': s.abs_clear_delay_ms
            })

    print(f"{Colors.OKGREEN}💾 Data saved to: {filename}{Colors.ENDC}")


def main():
    parser = argparse.ArgumentParser(description='Phase 2 Integration Testing & Monitoring')
    parser.add_argument('--duration', type=int, default=60,
                       help='Total monitoring duration in seconds (default: 60)')
    parser.add_argument('--samples', type=int, default=30,
                       help='Number of samples to collect (default: 30)')
    parser.add_argument('--csv', type=str, default=None,
                       help='Save results to CSV file')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed state information')

    args = parser.parse_args()

    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 80)
    print("  PHASE 2 INTEGRATION TESTING & MONITORING")
    print("=" * 80)
    print(f"{Colors.ENDC}")

    # Get configuration
    ha_url, ha_token = get_ha_config()
    print(f"🔗 Connected to: {Colors.OKCYAN}{ha_url}{Colors.ENDC}")

    # Get baseline values from firmware
    mu, sigma = get_baseline_from_firmware()
    print(f"📊 Baseline: μ={Colors.OKCYAN}{mu:.2f}%{Colors.ENDC}, "
          f"σ={Colors.OKCYAN}{sigma:.2f}%{Colors.ENDC}")

    # Pre-flight check
    print(f"\n{Colors.OKBLUE}🔍 Performing pre-flight check...{Colors.ENDC}")
    try:
        initial = collect_snapshot(ha_url, ha_token, mu, sigma)
        print(f"{Colors.OKGREEN}✅ All sensors accessible{Colors.ENDC}")
        print(f"   Current state: {'PRESENT' if initial.presence_state else 'VACANT'}")
        print(f"   Current energy: {initial.energy:.2f}%")
        print(f"   Current z-score: {initial.z_score:+.2f}σ")
    except Exception as e:
        print(f"{Colors.FAIL}❌ Pre-flight check failed: {e}{Colors.ENDC}")
        sys.exit(1)

    # Start monitoring
    print(f"\n{Colors.OKBLUE}📊 Collecting {args.samples} samples over {args.duration} seconds...{Colors.ENDC}\n")

    snapshots = []
    interval = args.duration / args.samples

    try:
        for i in range(args.samples):
            snapshot = collect_snapshot(ha_url, ha_token, mu, sigma)
            snapshots.append(snapshot)

            prev_snapshot = snapshots[-2] if len(snapshots) > 1 else None
            display_snapshot(snapshot, mu, sigma, args.verbose, prev_snapshot)

            # Sleep until next sample (except after last sample)
            if i < args.samples - 1:
                time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️  Monitoring interrupted by user{Colors.ENDC}\n")

    # Analyze results
    if snapshots:
        analyze_session(snapshots, mu, sigma)

        # Save to CSV if requested
        if args.csv:
            save_to_csv(snapshots, args.csv, mu, sigma)

    print(f"{Colors.OKGREEN}✅ Monitoring complete!{Colors.ENDC}\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
