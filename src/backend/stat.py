import json
import os.path
import platform
import threading

import requests

from src.events import events
from src.util import get_version


def get_mac():
    import uuid
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    mac_address = '-'.join([mac_address[i:i + 2] for i in range(0, 11, 2)])
    return mac_address


def check_newest():
    t = threading.Thread(target=do_check_newest)
    t.start()


def get_os_dist():
    if os.path.exists("/etc/lsb-release"):
        with open("/etc/lsb-release") as f:
            for line in f.readlines():
                items = line.split("=")
                if items[0] == "DISTRIB_DESCRIPTION":
                    return items[1]
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            lines = f.readlines()
            for line in lines:
                items = line.split("=")
                if items[0] == "PRETTY_NAME":
                    return items[1]
            for line in lines:
                items = line.split("=")
                if items[0] == "NAME":
                    return items[1]
    return "Unknown Linux"


def do_check_newest():
    data = {
        "app": {
            "name": "my_dict",
            "version": get_version(),
            "md5sum": "",
            "statistics": {}
        },
        "host": {
            "os": platform.platform(),
            "mac": get_mac(),
            "ext": {
                "dist": get_os_dist(),
                "uname": platform.uname(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "architecture": platform.architecture(),
            }
        }
    }

    try:
        response = requests.post("http://home.mydata.top:8681/api/my_dict/check_newest", data=json.dumps(data))
        print(threading.currentThread().getName(), "check_newest: ", response.text)
        res = response.json()
        if res["result"]["code"] != 0 or "new_version" not in res:
            return
        new_version = res["info"]
        events.signal_check_newest.emit(new_version)
    except:
        return
