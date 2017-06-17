## BMR HC 64 API, modbus TCP

See [pyModbusTCP](http://pythonhosted.org/pyModbusTCP/) documentation.

BMC HC 64 modbus TCP answers on port 502. Register values are read using function no. 3
'Read Holding Register'. One register has 2 bytes. Temperatures are stored as 2
byte integers.

A block of register addresses for room information starts

Room no. | Address |
---------|---------|
1        | 2033    |
2        | 2039    |
3        | 2045    |
4        | 2051    |
5        | 2057    |
6        | 2063    |
7        | 2069    |
8        | 2075    |
...

There are 32 rooms.
