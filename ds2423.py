# DS12423x dual counter driver for MicroPython.
# MIT license; Copyright (c) 2021 Christofer "Buff" Andersson

from micropython import const

_DS2423_READ_MEMORY_COMMAND = const(0xa5)
_DS2423_COUNTER_A = const(0xc0)
_DS2423_COUNTER_B = const(0xe0)


class DS2423(object):

    def __init__(self, onewire):
        self.ow = onewire

    def scan(self):
        return [rom for rom in self.ow.scan() if rom[0] == 29]

    def begin(self, adress):
        '''
        - Takes device adress, use .scan()
        - ie.  'counter.begin(bytearray(b'\x1d\x6c\xec\x0c\x00\x00\x00\x94'))'
        or counter.begin(rom[0]) from scan function
        '''
        self.rom = adress

    def isbusy(self):
        return not self.ow.readbit()

    def _crc16(self, data, length):
    # Calculate CRC16 for DS2423 data validation
        crc = 0
        for i in range(length):
            crc ^= data[i]
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc

    def get_count(self, counter):
        buf = [None] * 42
        self.ow.select_rom(self.rom)
        self.ow.writebyte(_DS2423_READ_MEMORY_COMMAND)
        self.ow.writebyte(_DS2423_COUNTER_A if counter ==
                        "DS2423_COUNTER_A" else _DS2423_COUNTER_B)
        self.ow.writebyte(0x01)
        self.ow.readinto(buf)
        self.ow.reset()
        
        # CRC16 validation - invert received CRC as per datasheet  
        calculated_crc = self._crc16(buf, 40)
        received_crc = buf[40] | (buf[41] << 8)
        # Invert the received CRC (datasheet says it's complemented)
        received_crc = ~received_crc & 0xFFFF
        if calculated_crc != received_crc:
            raise ValueError("CRC16 validation failed - data may be corrupted")
        
        count = int(buf[35])
        for i in range(34, 31, -1):
            count = (count << 8) + buf[i]
        return count