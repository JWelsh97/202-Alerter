import requests
import json

class PushBullet(object):
    def __init__(self):
        self.__s = requests.session()
        self.__s.headers = {"Access-Token": access_token}
    
    def get_devices(self):
        """
        Gathers pushbullet directory
        of all devices
        """
        try:
            r = json.loads(self.__s.get("https://api.pushbullet.com/v2/devices").text)
        except:    
            result = []
        if "devices" in request:
            devices = request["devices"]
            result = []
            for device in devices:
                if device["active"]:
                    result.append(device)
        return result
        
    def push_note(self, device_iden, title, body):
        result = []
        if isinstance(devices, list):
            for device in devices:
                post = self.__s.post("https://api.pushbullet.com/v2/pushes",
                                     data={"type": "note",
                                           "device": device_iden,
                                           "title": title,
                                           "body": body})
                result.append(post.text)
        return result

