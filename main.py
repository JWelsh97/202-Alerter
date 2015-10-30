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
    except requests.Timeout:
        return {"state": SiteState.error, "status": -1, "reason":  "Server is offline"}
    except requests.ConnectionError:
        return {"state": SiteState.error, "status": -1, "reason": "Webserver is offline"}
    except Exception as e:
        return {"state": SiteState.error, "status": -1, "reason": str(e)}

    if r.status_code == "200":
        return {"state": SiteState.up, "status": r.status_code, "reason": r.reason}
    else:
        return {"state": SiteState.up, "status": r.status_code, "reason": r.reason}


def read_config():
    """
    Reads the YAML config file
    """
    with open("config.yaml", "r") as f:
        conf = yaml.load(f)
    return conf


def add_device(pb, dev_num):
    conf = read_config()
    dev_lst = pb.get_devices()
    try:
        dev_name, dev_id = dev_lst[dev_num]
    except:
        print('Invalid device')
        return

    if not 'devices' in conf:
        conf['devices'] = []

    if not isinstance(conf['devices'], list):
        conf['devices'] = []

    if dev_id in conf['devices']:
        print('%s is already listed' % dev_name)
    else:
        conf['devices'].append(dev_id)
        with open('config.yaml', 'w') as f:
            f.write(yaml.dump(conf))
        print('Added %s' % dev_name)



def main(pb, conf):
    """
    Determines which message is used
    pushes selected message out to devices
    """
    status = site_status(conf["site"])
    dt_time = datetime.datetime.now().strftime("%I:%M%p %d/%m/%y")
    devices = conf["devices"]

    if status["state"] == SiteState.down:
        pb.push_note("Website Unavailable",
                     "%s as of %s" % (status["reason"], dt_time),
                     devices)
    elif status["state"] == SiteState.error:
        pb.push_note("Website Offline",
                     "%s as of %s" % (status["reason"], dt_time),
                     devices)


conf = read_config()
pb = PushBullet(conf["access_token"])

if "--list" in sys.argv:
    for idx, device in enumerate(pb.get_devices()):
        print('[{0}] {1}: {2}'.format(idx, *device))
elif "--add" in sys.argv:
    idx = sys.argv.index('--add')
    try:
        dev_num = int(sys.argv[idx + 1])
    except:
        print('Incorrect usage')
        print('Example: --add NUMBER')
        sys.exit()
    add_device(pb, dev_num)
    
else:
    if site_status("https://google.com")["state"] == SiteState.up:
        main(pb, conf)

