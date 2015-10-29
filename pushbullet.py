import requests
import json

class Pushbullet(object):
    def __init__(self):
        self.__s = requests.session()
        self.__s.headers = {"Access Token": access_token}
    

    def get_devices(access_token):
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

    def pushable(devices):
        """
        Takes pushbullet directory and
        checks if they are pushable
        """
        
        

    def push_note(device_iden, title, body):
