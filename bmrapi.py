#!/usr/bin/python

import sys
import requests
import datetime
from settings import settings

rooms = settings['rooms']
protocol = settings['protocol']
ip = settings['ip']
consumption = settings['consumption']
log = settings['logfile']
username = settings['username']
password = settings['password']

def obfuscate(s):
    b = ''
    c = datetime.datetime.now().day
    d = 0
    while d < len(s):
        e = ord(s[d])
        e = e^c<<2
        b = b + ('0%x' % e)[-2:].upper()
        d += 1
    return b

def login():
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'cs,en;q=0.8,en-US;q=0.6',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': protocol + '://' + ip + '/login.html',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'loginName': obfuscate(username),
        'passwd': obfuscate(password),
    }
    print headers
    print data
    resp = requests.post(protocol + '://' + ip + '/menu.html', data=data, headers=headers)
    if 'res_error_title' in resp.text:
        raise Exception('Unable to login')
    return True

def time_now():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def hdo_low():
    resp = requests.post(protocol + '://' + ip + '/loadHDO', data={'param': ''})
    return bool(int(resp.text))

def parse_response(s):
    return {
        'name': s[1:14].strip(),
        'current': float(s[14:19]),
        'required': int(s[20:22]),
        'required_all': float(s[22:27]),
        'offset': float(s[27:32]),
        'max_offset': float(s[33:36]),
        'heating': int(s[36]),
        'low': int(s[42]),
        'summer': int(s[43]),
    }

def get_raw_data():
    try:
        hdo_low()
    except:
        login()
    return (hdo_low() and 'L' or 'H') + '|' +\
        time_now() + '|' +\
        '|'.join([requests.post(protocol + '://' + ip + '/wholeRoom', data={'param': x}).text for x in range(rooms)])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: python bmrdash.py ACTION"
        exit(1)
    if sys.argv[1] == 'get':
        print get_raw_data()
    elif sys.argv[1] == 'store':
        with open(log, 'a') as logf:
            data = get_raw_data()
            logf.write(data + '\n')
            logf.flush()
