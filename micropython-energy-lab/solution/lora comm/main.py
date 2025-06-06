import socket
import network
import machine
import time
import gc
import ustruct as struct
from machine import Pin,SoftSPI, SPI
from sx127x import SX127x
import bme280_float as bme280

machine.freq(160000000)  ### set CPU frequency to 160MHz
gc.collect()  ### garbage collection
### TX = 1 -> ustruct encoding
### TX = 0 -> string encoding

wlan = network.WLAN(network.WLAN.IF_STA)
wlan.active(False)

TX = 0 

lora_default = {
    'frequency': 868000000,
    'frequency_offset':0,
    'tx_power_level': 14,
    'signal_bandwidth': 125e3,
    'spreading_factor': 9,
    'coding_rate': 5,
    'preamble_length': 8,
    'implicitHeader': False,
    'sync_word': 0x12,
    'enable_CRC': True,
    'invert_IQ': False,
    'debug': False,
}

lora_pins = {
    'dio_0':46,
    'ss':48,
    'reset':45,
    'sck':14,
    'miso':21,
    'mosi':47,
}

lora_spi = SoftSPI(
    baudrate=10000000, polarity=0, phase=0,
    bits=8, firstbit=SPI.MSB,
    sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
    miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP),
)

lora = SX127x(lora_spi, pins=lora_pins, parameters=lora_default)


STRUCT_FORMAT = "!BHfL"



STUDENT_GROUP_ID = 12
PKT_ID = 0

PERIOD = 60000  ### 60s
ACTIVE_TIME = 30000  ### seconds
SLEEP_TIME = 30000  ### seconds


tx_indicator = Pin(38, Pin.OUT)
tx_indicator.value(0)
tx_loop_indicator = Pin(2, Pin.OUT)
tx_loop_indicator.value(0)
#### blink LED to indicate start
for i in range(10):
    tx_loop_indicator.value(1)
    tx_indicator.value(1)
    time.sleep(0.1)
    tx_loop_indicator.value(0)
    tx_indicator.value(0)
    time.sleep(0.1)
tx_indicator.value(0)

print("START")


i2c = machine.I2C(0, sda=machine.Pin(9), scl=machine.Pin(8))
bme = bme280.BME280(i2c=i2c)

i=0
while i<5:
    print('loop', i)
    tx_loop_indicator.value(1)
    time_1 = time.ticks_ms()

    time_read = time.ticks_ms()
    temp, press, humidity = bme.values
    time_read = time.ticks_diff(time.ticks_ms(), time_read)
    print('time_read', time_read)

    print('temp, press', temp, press)

    temp = float(temp[:-1])
    print('temp', temp)
    press = int(float(press[:-3])*100)
    print('press', press)

    print('temp, press', temp, press)

    i += 1
    PKT_ID = i 
    if TX == 1:
        data = struct.pack(STRUCT_FORMAT, STUDENT_GROUP_ID, PKT_ID, temp, press)
    else:
        data_raw = '{}, {}, {}, {}'.format(STUDENT_GROUP_ID, PKT_ID, temp, press)
        # data_raw = '{}, {}, {}'.format(STUDENT_GROUP_ID, temp, press)  ### mistake 1:wrong packet size 
        # data_raw = '{}, {}, {}, {}, {}'.format(STUDENT_GROUP_ID, temp, PKT_ID, press, press)  ### mistake 1:wrong sequence 

        data = data_raw
    struct_len = struct.calcsize(STRUCT_FORMAT)
    data_len = len(data)

    time_tx = time.ticks_ms()
    lora.println(data)
    time_tx = time.ticks_diff(time.ticks_ms(), time_tx)
    print('time_tx', time_tx)

    print('data sent', time.ticks_ms())
    payload = lora.listen(time=3000)
    # print(lora.receivedPacket())
    print('listened for:', time.ticks_ms())
    print('payload:', payload)

    print('data:', data)
    print('struct_len:', struct_len)
    print('data_len:', data_len)
    
    if payload != None:
        try:
            payload = struct.unpack('!BH', payload)
        except:
            payload = payload.decode()

        rssi = lora.packetRssi()
        print("RX: {} | RSSI: {}".format(payload, rssi))
    else:
        print('No ACK')

    tx_indicator.value(1)
    time.sleep(0.1)
    tx_indicator.value(0)
    time.sleep(0.1)
    
    # if lora.receivedPacket():
    #     try:
    #         payload = lora.readPayload()
    #         payload = struct.unpack('!BH', payload)
    #         rssi = lora.packetRssi()
    #         print("RX: {} | RSSI: {}".format(payload, rssi))
    #     except Exception as e:
    #         print(e)
    # else:
    #     print('No ACK')

    time2 = time.ticks_ms()
    
    remaining_time = ACTIVE_TIME - time.ticks_diff(time2, time_1) - 200
    print('remaining_time', remaining_time)
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < remaining_time:
        if lora.receivedPacket():
            # if TX == 1:
            #     payload = struct.unpack('!BH', payload)
            # else:
            #     payload = payload.decode()

            rssi = lora.packetRssi()
            print(" RSSI: {}".format(rssi))

    

    time_active = time.ticks_diff(time.ticks_ms(), time_1)
    print('time_active', time_active/1000)
    time_sleep = PERIOD - time_active
    print('sleeping for', time_sleep/1000)
    lora.sleep()
    # time.sleep(time_sleep/1000)
    machine.lightsleep(time_sleep)
    tx_loop_indicator.value(1)
    gc.collect()

tx_loop_indicator.value(1)
tx_indicator.value(1)
time.sleep(5)
tx_loop_indicator.value(0)
tx_indicator.value(0)
    