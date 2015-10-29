import requests
import sys
import yaml
from pushbullet import PushBullet
import datetime


def sitestatus(url):
    """
    Determines why the site
    cannot be accessed, places
    data in tuple
    """
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        return ("Error!", "Webserver is offline")
    except requests.Timeout:
        return ("Error!", "Server is offline")
    except Exception as e:
        return ("Error!", str(e))
    else:
        return ("Up!", "Site is up!")



def read_config():
    """
    Reads the YAML config file
    """
    f = open("config.yaml", "r")
    conf = f.read()
    f.close()    
    return yaml.load(conf)


if sitestatus("https://google.com")[0] == "Up!":
    dateandtime = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%y")
    conf = read_config()
    sitestatus = sitestatus(conf["site"])
    pb = PushBullet(conf["access_token"])
    get_devices = pb.get_devices()
    index = -1
    if sys.argv > 1:
        for arg in sys.argv:
            if arg == "--list":
                arg = True
                for device in get_devices:
                    index += 1
                    print "%s: %s" % (get_devices[index][0], get_devices[index][1])
            else:
                arg = False
    if arg == False and sitestatus[0] == "Error!":
        pb.push_note(sitestatus[0], "%s as of %s" % (sitestatus[1], dateandtime), conf["devices"])
