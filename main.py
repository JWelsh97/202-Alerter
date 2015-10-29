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
        return ("Error", "Webserver is offline")
    except requests.Timeout:
        return ("Error", "Server is offline")
    except Exception as e:
        return ("Error", str(e))
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


conf = read_config()
if sitestatus("https://google.com")[0] == "Up!":
    sitestatus = sitestatus(conf["site"])
    pb = PushBullet(conf["access_token"])
    get_devices = pb.get_devices()
    if sys.argv > 1:
        for arg in sys.argv:
            if arg == "--list":    
                print "%s: %s\n" % (get_devices[0][0], get_devices[0][1])
    if sys.argv < 1:
        if sitestatus[0] == "Error":
            push = pb.push_note(sitestatus[0], "%s as of %s" % (sitestatus[1], datetime.datetime.now), conf["devices"])
