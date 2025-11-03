ha-bed-presence/
├── .devcontainer/
│   └── devcontainer.json       # Config for Codespaces (e.g., install ESPHome, Python)
├── .github/
│   └── workflows/
│       ├── compile_firmware.yml # CI Action to compile ESPHome code on push
│       └── lint_yaml.yml        # CI Action to check all YAML for errors
├── docs/
│   ├── assets/
│   │   ├── demo.gif
│   │   └── wiring_diagram.png
│   ├── calibration.md
│   ├── faq.md
│   ├── quickstart.md
│   └── troubleshooting.md
├── esphome/
│   ├── custom_components/
│   │   └── bed_presence_engine/
│   │       ├── __init__.py      # ESPHome component schema
│   │       ├── bed_presence.cpp # C++ implementation of the presence engine
│   │       └── bed_presence.h   # C++ header for the presence engine
│   ├── packages/
│   │   ├── diagnostics.yaml
│   │   ├── hardware_m5stack_ld2410.yaml
│   │   ├── presence_engine.yaml
│   │   └── services_calibration.yaml
│   ├── test/
│   │   └── test_presence_engine.cpp # Unit tests for the C++ component
│   ├── bed-presence-detector.yaml   # The main device entry-point file
│   ├── platformio.ini               # PlatformIO config for C++ unit testing
│   └── secrets.yaml.example         # Example secrets file for Wi-Fi, etc.
├── hardware/
│   └── mounts/
│       └── m5stack_side_mount.stl   # 3D printable mount file
├── homeassistant/
│   ├── blueprints/
│   │   └── automation/
│   │       └── bed_presence_automation.yaml
│   ├── dashboards/
│   │   └── bed_presence_dashboard.yaml
│   └── configuration_helpers.yaml.example # Example helpers to be added to HA
└── tests/
    └── e2e/
        ├── test_calibration_flow.py # E2E test script using HA's API
        └── requirements.txt         # Python dependencies for E2E tests
├── .gitignore
├── LICENSE
└── README.md