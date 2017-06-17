#!/usr/bin/python3

from pyModbusTCP.client import ModbusClient

# http://pythonhosted.org/pyModbusTCP/

class BMRModbusAPI():
    "BMR RT64 regulation client API using pyModbusTCP"

    def __init__(self, settings):
        self.settings = settings
        self.version = '0.9'
        self.client = ModbusClient(host=self.settings['host'],
                port=self.settings['port'])
        #self.client.debug(True)

    def read_registers(self, address=0):
        if not self.client.is_open():
            if not self.client.open():
                Exception("unable to connect to " + self.settings['host'] +\
                        ":" + str(self.settings['port']))
        if self.client.is_open():
            return self.client.read_holding_registers(address, 1)

    def get_current_temperature(self, address=None):
        return self.read_registers(address)[0] / 10.

    def get_hdo(self):
        return self.client.read_registers(1000)


if __name__ == '__main__':
    from settings import settings
    api = BMRModbusAPI(settings)
    # for channel in api.settings['channels']:
    for ch in api.settings['channels']:
        print(ch['address'], ch['name'], api.get_current_temperature(ch['address']))
