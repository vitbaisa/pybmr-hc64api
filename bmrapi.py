#!/usr/bin/python

import sys
import requests
import datetime

class BMRAPI():
    "BMR RT64 regulation API as observed from BMR client web app"

    def __init__(self, settings):
        self.protocol = settings.get('protocol', 'http://')
        self.host = settings.get('host', 'localhost')
        self.channels = settings.get('channels', [])
        self.rooms = len(self.channels)
        self.username = settings.get('username', 'user')
        self.password = settings.get('password', '1234')
        self.session = requests.Session()
        self.version = '0.9'
        # login
        #self.login()

    def obfuscate(self, s):
        # algorithm taken from BMR client
        b = ''
        c = datetime.datetime.now().day
        d = 0
        while d < len(s):
            e = ord(s[d])
            e = e^c<<2
            b = b + ('0%x' % e)[-2:].upper()
            d += 1
        return b

    def login(self):
        data = {
            'loginName': self.obfuscate(self.username),
            'passwd': self.obfuscate(self.password),
        }
        resp = self.session.post(self.protocol + '://' + self.host + '/menu.html', data=data)
        print resp.text
        if 'res_error_title' in resp.text:
            raise Exception('Unable to login')
        return True

    def hdo_is_low(self):
        resp = self.session.post(self.protocol + '://' + self.host + '/loadHDO', data={'param': ''})
        return bool(int(resp.text))

    def parse_raw_data(self, s):
        try:
            return {
                'name': s[1:14].strip(),
                'current': float(s[14:19]),
                'required': float(s[20:22]),
                'required_all': float(s[22:27]),
                'offset': float(s[27:32]),
                'max_offset': float(s[33:36]),
                'heating': int(s[36]),
                'inhibited': int(s[42]),
                'summer': int(s[43]),
            }
        except ValueError, KeyError:
            return {}

    def get_raw_channel_data(self, channel=0):
        return self.session.post(self.protocol + '://' + self.host + '/wholeRoom', data={'param': channel}).text

    def get_channel_data(self, channel=0):
        return self.parse_raw_data(self.get_raw_channel_data(channel))

if __name__ == '__main__':
    from settings import settings
    api = BMRAPI(settings)
    for channel, _ in enumerate(api.channels):
        print api.get_channel_data(channel)
