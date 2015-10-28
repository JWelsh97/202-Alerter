import requests


def sitestatus(url):
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        return ("Error", "Webserver is offline.")
    except requests.Timeout:
        return ("Error", "Server is offline.")
    except Exception as e:
        return ("Failure", str(e))