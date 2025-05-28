import time
from machine import Pin
from sx127x import SX127x
import bme280_float as bme280



tx_indicator = Pin(38, Pin.OUT)
tx_indicator.value(0)

for cycles in range(5): # stop after 10 cycles
    print("Cycle", cycles)

    tx_indicator.value(1)
    time.sleep(0.1)
    tx_indicator.value(0)

    time.sleep(1)