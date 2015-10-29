import requests


def sitestatus(url):
    '''
    Determines why the site
    cannot be accessed, places
    data in tuple
    '''
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        return ("Error", "Webserver is offline.")
    except requests.Timeout:
        return ("Error", "Server is offline.")
    except Exception as e:
        return ("Failure", str(e))

def read_config():
    '''
    Reads the YAML config file
    '''
    f = open("config.yaml", "r")
    conf = f.read()
    f.close()
    return yaml.load(conf)
