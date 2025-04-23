To use the template you will need to place tuya_status.py in the /usr/lib/zabbix/externalscripts folder on your Zabbix Server machine

To use tuya_status run:

```python3 tuya_status.py <IP> <DEVICE.ID> <LOCAL.KEY> <PROTOCOL.VERSION>```

<PROTOCOL.VERSION> is 3.1, 3.2, 3.3 or 3.4
This will produce a json
For more readible form add --pretty which should give output like:
```

Device status (pretty):
Switch ON/OFF: True
DPS 9: 0
DPS 17: 5
Current [A]: 0.076
Power [W]: 17.1
Voltage [V]: 226.3
DPS 21: 1
Voltage Coefficient: 568
Electric Coefficient: 27135
Power Coefficient: 14837
Electricity Coefficient: 2810
DPS 26: 0
Relay Status: memory
Overcharge Switch: False
Light Mode: relay
Child Lock: False
DPS 42:
DPS 43:
DPS 44:
```

To use tuya_toggle.py run:

python3 tuya_toggle.py <IP> <DEVICE.ID> <LOCAL.KEY> <VAR> <OPTIONAL.TIMEOUT>

<VAR> can be on, of, reset
<OPTIONAL.TIMEOUT> is a timeout for reset telling how long does the device must be off
