
import socket
import machine
import time
import ustruct as struct
from machine import Pin,SoftSPI, SPI
from sx127x import SX127x
import bme280_float as bme280

### TX = 1 -> ustruct encoding
### TX = 0 -> string encoding
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



STUDENT_GROUP_ID = 19
PKT_ID = 0



# initialise LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
#lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# create a raw LoRa socket
#s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

#s.setblocking(False)

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

temp, press, humidity = bme.values
print('temp, press', temp, press)

temp = float(temp[:-1])
print('temp', temp)
press = int(float(press[:-3])*100)
print('press', press)

print('temp, press', temp, press)




#lora.send(data)
start_time = time.ticks_ms()
i = 0
while i<110:
    if time.ticks_diff(time.ticks_ms(), start_time) > 3000:
        start_time = time.ticks_ms()
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

        lora.println(data)
        print('data sent', time.ticks_ms())
        payload = lora.listen(time=3000)
        print(lora.receivedPacket())
        print('listened for:', time.ticks_ms())
        print('payload:', payload)
        time.sleep(0.1)

        print('data:', data)
        print('struct_len:', struct_len)
        print('data_len:', data_len)
        
        if payload != None:
            if TX == 1:
                payload = struct.unpack('!BH', payload)
            else:
                payload = payload.decode()

            rssi = lora.packetRssi()
            print("RX: {} | RSSI: {}".format(payload, rssi))
        else:
            print('No ACK')
        
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
        
        tx_indicator.value(1)
        time.sleep(0.1)
        tx_indicator.value(0)
                
        # time.sleep(3)
        
        