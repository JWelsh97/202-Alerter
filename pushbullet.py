import requests
import json


class PushBullet(object):
    def __init__(self, access_token):
        self.__s = requests.session()
        self.__s.headers = {"Access-Token": access_token}

    def get_devices(self):
        try:
            r = json.loads(self.__s.get("https://api.pushbullet.com/v2/devices").text)
        except:
            result = []
        if "devices" in r:
            devices = r["devices"]
            result = []
            for device in devices:
                if device["active"]:
                    result.append((device["nickname"], device["iden"]))
        return result

    def push_note(self, title, body, devices):
        result = []
        if isinstance(devices, list):
            for iden in devices:
                post = self.__s.post("https://api.pushbullet.com/v2/pushes",
                                     data={"type": "note",
                                           "device_iden": iden,
                                           "title": title,
                                           "body": body})
                result.append(post.text)
        return result