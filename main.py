import requests
import sys
import yaml
from pushbullet import PushBullet
import datetime
from enum import Enum


class SiteState(Enum):
    error = 1
    down = 2
    up = 3


def site_status(url):
    """
    Determines why the site cannot be accessed
    """
    try:
        r = requests.get(url, timeout=5)
    except requests.ConnectionError:
        return {"state": SiteStatus.error,
                "status": -1,
                "reason": "Webserver is offline"}
    except requests.Timeout:
        return {"state": SiteStatus.error,
                "status": -1,
                "reason":  "Server is offline"}
    except Exception as e:
        return {"state": SiteStatus.error,
                "status": -1,
                "reason": str(e)}

    if r.status_code == "200":
        return {"state": SiteStatus.up,
                "status": r.status_code,
                "reason": r.reason}
    else:
        return {"state": SiteStatus.up,
                "status": r.status_code,
                "reason": r.reason}


def read_config():
    """
    Reads the YAML config file
    """
    with open("config.yaml", "r") as f:
        conf = yaml.load(f)
    return conf


def main(pb, conf):
    status = site_status(conf["site"])
    dt_time = datetime.datetime.now().strftime("%I:%M%p %d/%m/%y")
    devices = conf["devices"]

    if status["state"] == SiteStatus.down:
        pb.push_note("Website Unavailable",
                     "%s as of %s" % (status["reason"], dt_time),
                     devices)
    elif status["state"] == SiteStatus.error:
        pb.push_note("Website Offline",
                     "%s as of %s" % (status["reason"], dt_time),
                     devices)


conf = read_config()
pb = PushBullet(conf["access_token"])

if "--list" in sys.argv:
    for device in pb.get_devices():
        print("%s: %s" % device)
else:
    main(pb, conf)
