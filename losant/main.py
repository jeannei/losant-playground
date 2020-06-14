import time
import random
from losantmqtt import Device


# event_type values: int, bool, none
devices = {
    "5edd12818dead300075fc61d": {
        "name": "Fire detector",
        "device": Device(
            "5edd12818dead300075fc61d",
            "bc216521-185e-461e-94e5-c7bd7807e679",
            "0c76b4b7378d52e2487ac222b53d6df7e98a35d8988227969ce146921945c630"
        ),
        "sensor_attribute_key": "firedetector",
        "event_type": "int",
        "command_handler": lambda name, device, event_name, event_value:
            print("Got command", name, event_name, event_value),
    },
    "5edd109a8dead300075fc61b": {
        "name": "Temperature",
        "device": Device(
            "5edd109a8dead300075fc61b",
            "3d6d2c20-68a5-4698-a694-e53a757d23e5",
            "b881bc40e681c12f96d0a036c3ccbacc12908d1431af07bf7ad11ca175787b70"
        ),
        "sensor_attribute_key": "temperature",
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
