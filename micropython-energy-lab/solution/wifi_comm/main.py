import network
import socket
import time
import machine
import gc
from machine import Pin,SoftSPI, SPI
from sx127x import SX127x
import bme280_float as bme280

machine.freq(160000000)  ### set CPU frequency to 160MHz
gc.collect()  ### garbage collection

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



STUDENT_GROUP_ID = 19
PKT_ID = 0

PERIOD = 60000  ### 60s
ACTIVE_TIME = 30000  ### seconds
SLEEP_TIME = 30000  ### seconds


ssid = 'CN-Students'
password = 'CnStudentsWiFiAccess123'

#host_ip = '127.0.0.1'
host_ip = '192.168.0.180'
host_port = 9999


i2c = machine.I2C(0, sda=machine.Pin(9), scl=machine.Pin(8))
bme = bme280.BME280(i2c=i2c)


wlan = network.WLAN(network.WLAN.IF_STA)

if wlan.isconnected():
    wlan.disconnect()
    wlan.active(False)
    print('Terminating old connection')
    
wlan.active(True)
print('Status:', wlan.active())
print('Connection:', wlan.isconnected())

if not wlan.isconnected():
    print('Connecting WLAN . . . . ')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        machine.idle()
    ip_addr = wlan.ipconfig('addr4')
    print('ip_addr:', ip_addr)
    

tx_addr = socket.getaddrinfo(host_ip, host_port)[0][-1]
print('tx_addr', tx_addr)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq = 0
while seq<5:
    print('loop', i)
    tx_loop_indicator.value(1)
    time_1 = time.ticks_ms()

    time_read = time.ticks_ms()
    temp, press, humidity = bme.values
    time_read = time.ticks_diff(time.ticks_ms(), time_read)
    print('time_read', time_read)

    temp = float(temp[:-1])
    print('temp', temp)
    press = int(float(press[:-3])*100)
    print('press', press)

    print('temp, press', temp, press)
    
    msg = str(STUDENT_GROUP_ID) + ' ; ' + str(seq) + ' ; ' + str(temp) + ' ; ' + str(press) + ' ; ' + ip_addr[0]
    byt = msg.encode()
    
    time_tx = time.ticks_ms()
    if not wlan.active():
        wlan.active(True)
    if not wlan.isconnected():
        print('Connecting WLAN . . . . ')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            machine.idle()
        ip_addr = wlan.ipconfig('addr4')
        tx_addr = socket.getaddrinfo(host_ip, host_port)[0][-1]
        print('tx_addr', tx_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(byt, tx_addr)
    time_tx = time.ticks_diff(time.ticks_ms(), time_tx)
    print('Transmitted pakcet ', seq, time_tx)
    
    sock.settimeout(0)
    
    
    try:
        payload = sock.recvfrom(80)
        print(payload)
    except OSError as e:
        if e.args[0] == 11:
            print('No ACK')
    
    tx_indicator.value(1)
    time.sleep(0.1)
    tx_indicator.value(0)
    time.sleep(0.1)
    
    time.sleep(5)
    seq = seq + 1
    
    time2 = time.ticks_ms()
    
    remaining_time = ACTIVE_TIME - time.ticks_diff(time2, time_1) - 200
    
    print('remaining_time', remaining_time)
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < remaining_time:
        try:
            payload = sock.recvfrom(80)
            print(payload)
        except OSError as e:
            if e.args[0] == 11:
                pass
                #print('No ACK')
            
    time_active = time.ticks_diff(time.ticks_ms(), time_1)
    print('time_active', time_active/1000)
    time_sleep = PERIOD - time_active
    print('sleeping for', time_sleep/1000)
    sock.close()
    wlan.active(False)
    # time.sleep(time_sleep/1000)
    machine.lightsleep(time_sleep)
    # machine.deepsleep(time_sleep)
    tx_loop_indicator.value(1)
    gc.collect()
    
tx_loop_indicator.value(1)
tx_indicator.value(1)
time.sleep(5)
tx_loop_indicator.value(0)
tx_indicator.value(0)
    
sock.close()
wlan.disconnect()