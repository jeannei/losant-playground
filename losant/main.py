import time
import random
from losantmqtt import Device


# event_type values: int, bool, none
devices = {
    "5ee4ecc26cdf8d000610bd05": {
        "name": "Temp Sensor",
        "device": Device(
            "5ee4ecc26cdf8d000610bd05",
            "cf8bdf2b-8843-4710-95df-66793d7238d9",
            "b178891f59a5d77a643cc0f4a541bb6136d9845b3512fab537025353864ffb3b"
        ),
        "sensor_attribute_key": "temp",
        "event_type": "int",
        "command_handler": lambda name, device, event_name, event_value:
        print("Got command", name, event_name, event_value),
    },
    "5ee4ed79f0e1080007ca6ab8": {
        "name": "AC",
        "device": Device(
            "5ee4ed79f0e1080007ca6ab8",
            "09379aee-d26a-497b-996d-fa85dfb44c73",
            "2e9c09fde5581e41f65a95898f28bd1f14dc8fdd5e45b51ca659bedcfaa84ec1"
        ),
        "sensor_attribute_key": "ACSwitch",
        "event_type": "none",
        "command_handler": lambda name, device, event_name, event_value:
            print("Got command", name, event_name, event_value),
    },
    "5ee4ecfb62971c00072eb473": {
        "name": "Air Quality Sensor",
        "device": Device(
            "5ee4ecfb62971c00072eb473",
            "ee5dac9d-181a-4529-a22d-da661cba5ea2",
            "dd64699aeceae44d5f8d5b8a50149743630d081910690244a9ad72f87198e8a4"
        ),
        "sensor_attribute_key": "AQI",
        "event_type": "int",
        "command_handler": lambda name, device, event_name, event_value:
        print("Got command", name, event_name, event_value),
    },
    "5ee4edbb95039800064810f0": {
        "name": "Air Purifier",
        "device": Device(
            "5ee4edbb95039800064810f0",
            "1608fc2e-c44b-469b-af51-b3aedf36ef95",
            "79d6b4feacea687300479808b536db5f0c3c34aee32fd67ab4551112fb09107f"
        ),
        "sensor_attribute_key": "purifierSwitch",
        "event_type": "none",
        "command_handler": lambda name, device, event_name, event_value:
            print("Got command", name, event_name, event_value),
    },
    "5ee4ed476cdf8d000610bd07": {
        "name": "Noise Sensor",
        "device": Device(
            "5ee4ed476cdf8d000610bd07",
            "6553c479-4dbd-47f3-a5e1-23ffdf05458b",
            "43849337d8bc4a648b8a20f7cddb4493aa8533343f2bc60044f2a61bbe020949"
        ),
        "sensor_attribute_key": "noise",
        "event_type": "bool",
        "command_handler": lambda name, device, event_name, event_value:
            print("Got command", name, event_name, event_value),
    },
    "5ee507d7f0e1080007ca6acd": {
        "name": "Speaker",
        "device": Device(
            "5ee507d7f0e1080007ca6acd",
            "0ce90904-bff0-4d82-9f34-120a0a1831e9",
            "d8e78db99423262942448d95db558b9affaad9e9a35afd1c81fd449a0d60a6da"
        ),
        "sensor_attribute_key": "voice",
        "event_type": "none",
        "command_handler": lambda name, device, event_name, event_value:
            print("Got command", name, event_name, event_value),
    }
}


def on_command(incoming_device, command):
    device = devices[incoming_device._device_id]
    command_handler = device["command_handler"]
    command_handler(device["name"], incoming_device, command["name"], command["payload"])


# possible event names are connect, reconnect, close, and command
def attach_listeners_and_connect():
    for k, v in devices.items():
        device = v.get("device")
        device.add_event_observer("command", on_command)
        device.connect(blocking=False)


if __name__ == '__main__':
    attach_listeners_and_connect()
    while True:
        for key, value in devices.items():
            device = value.get("device")
            device.loop()
            if device.is_connected():
                sensor_attribute = value["sensor_attribute_key"]
                if value["event_type"] == "int":
                    state_val = random.random() * 100
                    device.send_state({sensor_attribute: state_val})
                elif value["event_type"] == "bool":
                    state_val = True if random.random() * 100 > 60 else False
                    device.send_state({sensor_attribute: state_val})
        time.sleep(4)
