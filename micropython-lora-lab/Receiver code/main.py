from machine import Pin, SPI
from sx127x import SX127x
import ustruct as struct
from machine import SDCard
import time
import os, vfs

### setup lora
lora_default = {
    'frequency': 868000000,
    'signal_bandwidth': 125e3,
    'spreading_factor': 9,
    'coding_rate': 5,
    'preamble_length': 8,
    'implicitHeader': False,
    'sync_word': 0x12,
    'enable_CRC': True,
    'invert_IQ': False,
    'debug': False,
    'frequency_offset':0,
    'tx_power_level': 14,
}


lora_pins = {
    'dio_0':46,
    'ss':48,
    'reset':45,
    'sck':14,
    'miso':21,
    'mosi':47,
}

lora_spi = SPI(
    baudrate=10000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
    sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
    miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP),
)


lora = SX127x(lora_spi, pins=lora_pins, parameters=lora_default)


### payload encoding format
STRUCT_FORMAT = "!BHfL"


### indicator leds
rx_loop_indicator = Pin(2, Pin.OUT)
rx_indicator = Pin(38, Pin.OUT)

rx_loop_indicator.value(0)
rx_indicator.value(0)

#### blink LED to indicate start
for i in range(10):
    rx_loop_indicator.value(1)
    rx_indicator.value(0)
    time.sleep(0.1)
    rx_loop_indicator.value(0)
    rx_indicator.value(1)
    time.sleep(0.1)
rx_indicator.value(0)
print("START")

### initialise Sd card
sd = SDCard(slot=2, sck=Pin(12), miso=Pin(13), mosi=Pin(11), cs=Pin(10))
vfs.mount(sd, '/sd') # mount
print('Files present on SDCard:')
print(os.listdir('/sd')) # list files

# File path on SD card
file_name = 'lora_data_0'

new_name = False
i=0
while not new_name:
    i += 1
    # Check if the file already exists
    if file_name in os.listdir('/sd'):
        file_name = file_name[:-1] + str(i)
    else:
        new_name = True

file_path = '/sd/' + file_name

data_buffer = []
BUFFER_SIZE = 1  # Adjust buffer size as 

i = 0
file_size = 0
while True:

#     i+=1
#     payload = lora.listen(time=5000)

#     if payload:
#         payload = struct.unpack(STRUCT_FORMAT, payload)
#         # payload = lora.readPayload().decode()
#         rssi = lora.packetRssi()
#         print("RX: {} | RSSI: {}".format(payload, rssi))
#         print('ack_payload', payload[0], payload[1])
#         ack_payload = struct.pack('!BH', payload[0], payload[1])
#         lora.println(ack_payload)
#         lora.receive()
#         rx_loop_indicator.value(1)
#         time.sleep(0.1)
#         rx_loop_indicator.value(0)
#     else:
#         print("No payload received")
    if lora.receivedPacket():
        i+=1
        print('receiver')
        payload = lora.readPayload()
        try:
            payload = payload.decode()
            print(payload)
            payload = payload.split(',')
            if len(payload) != 4:
                print('payload format incorrect')
                continue
            try:
                payload[0] = int(payload[0])
            except:
                print('group id invalid or incorrect type')
                continue
            if payload[0] > 20:
                print('payload contains invalid group id')
                continue
            try:
                payload[1] = int(payload[1])
            except:
                print('group id invalid or incorrect type')
                continue
            # if payload[1] > 30:
            #     print('payload contains invalid packet id')
            #     continue
            payload[2] = float(payload[2])
            payload[3] = int(payload[3])
            ack_payload = '{}, {}'.format(payload[0], payload[1])
        except:
            try:
                print('payload encoded using ustruct')
                payload = struct.unpack(STRUCT_FORMAT, payload)
                print(payload)
            except:
                print('payload corrupted')
            if len(payload) != 4:
                print('payload contains insufficient values')
                continue
            if payload[0] > 20 or not isinstance(payload[0], int):
                print('group id invalid or incorrect type')
                continue
            # if payload[1] > 30 or not isinstance(payload[1], int):
            if not isinstance(payload[1], int):
                print('packet id invalid or incorrect type')
                continue

            ack_payload = struct.pack('!BH', payload[0], payload[1])
        rssi = lora.packetRssi()
        print("RX: {} | RSSI: {}".format(payload, rssi))
        # print('ack_payload', payload[0], payload[1])
        print('ack_payload', ack_payload)

        ### write to sd card
        wrtie_start_time = time.ticks_ms()
        data_buffer.append(payload)
        if len(data_buffer) >= BUFFER_SIZE:
            file_size += BUFFER_SIZE
            with open(file_path, 'a') as f:
                for data in data_buffer:
                    f.write(','.join(map(str, data)) + '\n')
                f.flush()
            data_buffer = []
            print('File Saved:', file_path)

        if file_size >= 100:
            file_num = file_path.split('_')[-1]
            file_num = int(file_num)
            file_num += 1
            file_path = '/sd/lora_data_' + str(file_num)
            print('storing to new file:', file_path)
            file_size = 0 
        print('write time:', time.ticks_diff(time.ticks_ms(), wrtie_start_time))

        lora.println(ack_payload)
        rx_loop_indicator.value(1)
        time.sleep(0.1)
        rx_loop_indicator.value(0)
        
