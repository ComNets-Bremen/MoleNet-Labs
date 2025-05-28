import machine
import time
import ustruct as struct
from machine import Pin,SoftSPI, SPI
from sx127x import SX127x
import bme280_float as bme280


'''
DO NOT SEND THE PKTS FASTER THAN 10 SECONDS
'''

tx_ind = Pin(38, Pin.OUT)
tx_ind.value(0)
rx_ind = Pin(2, Pin.OUT)
rx_ind.value(0)
#### blink LED to indicate start
for i in range(10):
    rx_ind.value(1)
    tx_ind.value(1)
    time.sleep(0.1)
    rx_ind.value(0)
    tx_ind.value(0)
    time.sleep(0.1)
tx_ind.value(0)


'''
Take help of the code snippets in the implementation section of the report
Dont forget to adapt the pins for the MoleNet development board (refer Pin Mapping Table)
'''

### your unique group_id
GROUP_ID = 0

### init sensor
'''Add Code here'''



### init lora
'''Add Code here'''



for i in range(30):
    ### read data and Tx. over lora
    '''Add Code here'''







    tx_ind.value(1)
    time.sleep(0.1)
    tx_ind.value(0)
    time.sleep(10)




