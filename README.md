# Micropython OneWire DS2423
### Description

Lightweight driver for the 1wire counter ds2423 from Maxim Integrated
Designed to work with the micropython driver for onewire.

### Hardware

* [DS2423](https://www.maximintegrated.com/en/products/ibutton-one-wire/memory-products/DS2423.html) or ready made [device](https://en.m.nu/measuring-instruments/counters-for-connection-to-1wire-network-version-21)
* Tested on ESP8266
* Pull-up resistor is required on data bus, 1kohm to 3.3v is a good starting point

### Example Usage

```

import ds2423
import onewire

ow = onewire.OneWire(Pin(0))

counter = ds2423.DS2423(ow)
counter.begin(bytearray(b'\x1dl\xec\x0c\x00\x00\x00\x94'))
print(counter.get_count("DS2423_COUNTER_A"))

```