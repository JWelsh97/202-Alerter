#!/usr/bin/python

import requests
import sys
import config
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
        return {'state': SiteState.error, 'status': -1, 'reason': 'Server is offline'}
    except requests.ConnectionError:
        return {'state': SiteState.error, 'status': -1, 'reason': 'Webserver is offline'}
    except Exception as e:
        return {'state': SiteState.error, 'status': -1, 'reason': str(e)}

    if r.status_code == '200':
        return {'state': SiteState.up, 'status': r.status_code, 'reason': r.reason}
    else:
        return {'state': SiteState.up, 'status': r.status_code, 'reason': r.reason}


def add_device(pb, conf, dev_num):
    """
    Adds a device identity to config
    using --add-device or -a command
    """
    dev_lst = pb.get_devices()
    try:
        dev_name, dev_id = dev_lst[dev_num]
    except:
        print('Invalid device')
        return

    if 'devices' not in conf:
        conf['devices'] = []

    if not isinstance(conf['devices'], list):
        conf['devices'] = []

    if dev_id in conf['devices']:
        print('%s is already listed' % dev_name)
    else:
        conf['devices'].append(dev_id)
        config.write_config(conf)
        print('Added %s' % dev_name)


def remove_device(pb, conf, dev_num):
    """
    Removes a device identity
    from the config using
    --remove-device or -r
    """
    dev_lst = pb.get_devices()
    try:
        dev_name, dev_id = dev_lst[dev_num]
    except:
        print('Invalid device')
        return

    if 'devices' in conf:
        try:
            conf['devices'].pop(conf['devices'].index(dev_id))
        except:
            print('That device is not in your config')
            return
        config.write_config(conf)
        print('Removed %s' % dev_name)


def main(pb, site, conf):
    """
    Determines which message is used
    pushes selected message out to devices
    """
    status = site_status(site)
    dt_time = datetime.datetime.now().strftime('%I:%M%p %d/%m/%y')
    devices = conf['devices']

    if status['state'] == SiteState.down:
        pb.push_note('Website ({0}) Unavailable'.format(site),
                     '%s as of %s' % (status['reason'], dt_time),
                     devices)

    elif status['state'] == SiteState.error:
        pb.push_note('Website ({0}) Offline'.format(site),
                     '%s as of %s' % (status['reason'], dt_time),
                     devices)


conf = config.read_config()
pb = PushBullet(conf['access_token'])

if '-l' in sys.argv or '--list-devices' in sys.argv:
    for idx, device in enumerate(pb.get_devices()):
        print('[{0}] {1}: {2}'.format(idx, *device))

elif '-a' in sys.argv or '--add-device' in sys.argv:
    try:
        dev_num = int(sys.argv[2])
    except:
        print('Incorrect usage')
        print('Example: -a/--add-device NUMBER')
        sys.exit()
    add_device(pb, conf, dev_num)

elif '-r' in sys.argv or '--remove-device' in sys.argv:
    try:
        dev_num = int(sys.argv[2])
    except:
        print('Incorrect usage')
        print('Example: -r/--remove-device NUMBER')
        sys.exit()
    remove_device(pb, conf, dev_num)

else:
    if site_status('https://google.com')['state'] == SiteState.up:
        for site in conf['sites']:
            main(pb, site, conf)

