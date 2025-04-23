#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tinytuya
import sys
import json

DPS_LABELS = {
    "1":  "Switch ON/OFF",
    "18": "Current [A]",
    "19": "Power [W]",
    "20": "Voltage [V]",
    "22": "Voltage Coefficient",
    "23": "Electric Coefficient",
    "24": "Power Coefficient",
    "25": "Electricity Coefficient",
    "38": "Relay Status",
    "39": "Overcharge Switch",
    "40": "Light Mode",
    "41": "Child Lock"
}

DPS_SCALE = {
    "18": lambda v: round(v / 1000.0, 3),
    "19": lambda v: round(v / 10.0, 1),
    "20": lambda v: round(v / 10.0, 1),
}

def get_scaled_value(key, value):
    return DPS_SCALE[key](value) if key in DPS_SCALE else value

def main(args):
    if len(args) < 4:
        print("Usage: tuya_status.py <ip> <device_id> <local_key> <version> [param|--pretty]")
        sys.exit(1)

    ip, device_id, local_key, version = args[:4]
    extra = args[4] if len(args) > 4 else None

    device = tinytuya.OutletDevice(device_id, ip, local_key)
    device.set_version(float(version))

    try:
        data = device.status()
        dps = data.get("dps", {})
        if not dps:
            print(json.dumps({"error": "No DPS data returned"}))
            sys.exit(1)

        if extra and extra.lower() == "--pretty":
            print("Device status (pretty):")
            for key, value in dps.items():
                label = DPS_LABELS.get(key, f"DPS {key}")
                print(f"{label}: {get_scaled_value(key, value)}")
        elif extra:
            # Only one parameter requested (voltage/power/current/switch)
            param_map = {
                "voltage": "20",
                "power": "19",
                "current": "18",
                "switch": "1"
            }
            dps_key = param_map.get(extra.lower())
            if not dps_key or dps_key not in dps:
                print(json.dumps({"error": f"Unknown or missing parameter: {extra}"}))
                sys.exit(1)
            print(get_scaled_value(dps_key, dps[dps_key]))
        else:
            # Default = full JSON dump (ideal for Zabbix)
            print(json.dumps(data))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
