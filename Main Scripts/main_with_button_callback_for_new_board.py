# Created on: 16 May 2021
# Author: Steven Wong
# © Copyright 2022 Steven Wong. All Rights Reserved.

import machine, time, webrepl
from machine import SoftI2C
from machine import Timer
from lib.utils import connect_wifi
from lib.requests import MicroWebCli as requests
import ujson as json

"""
GPIO_0: VBATT_MON
GPIO_1: IMU INT
GPIO_2: Button A
GPIO_3: Internal ADC (not connected in default BOM)
GPIO_4: LED B
GPIO_5: Button B
GPIO_6: I2C SCL (not connected in default BOM)
GPIO_7: I2C SDA (not connected in default BOM)
GPIO_8: I2C SDA (default BOM connection)
GPIO_9: BOOT0 and I2C SCL (default BOM connection)
GPIO_10: Test point
GPIO_18: IMU CS
GPIO_19: LED A

I2C address: 0x48 (External ADC ADS1000(-Q1)), 0x2C (DigiPot MCP4532-104), 0x6B (IMU LSM6DSO32)
"""

def read_adc_config():
    i = i2c.readfrom(0x48,3)
    return hex(i[2])

def read_adc_data():
    i = i2c.readfrom(0x48,2)
    # convert byte array (2's complement data with sign extension) to int
    return (i[1] + ((i[0] & 0x7) << 8)) - ((i[0] & 0x8) << 8)

# ADC PGA gain setting, 0 -> x1, 1 -> x2, 2 -> x4, 3 -> x8
def set_adc_gain(value):
    if value < 4:
        i2c.writeto(0x48,bytearray([value]))
        print('Set ADC PGA register to ',value)

def set_gain(value):
    if value < 129:
        i2c.writeto_mem(0x2c,0,bytearray([value]))
        print('Set second stage gain to ',1+(((100000*value/128)+75)/2000))

# increase gain by ~0.39
def increase_gain():
    return i2c.writeto(0x2c,bytearray([4]))

# decrease gain by ~0.39
def decrease_gain():
    return i2c.writeto(0x2c,bytearray([8]))

def read_gain():
    if i2c.writeto(0x2c,bytearray([0xc]),False):
        i = i2c.readfrom(0x2c,2)
        print('Second stage gain is ',i[1],' = ',1+(((100000*i[1]/128)+75)/2000))

# initialise ADC variables abd ADC buffer size of 256 for double buffering
adc_buf = [0] * 256
adc_idx = 0
old_idx = 0
running = False

# Timer(0) call backfunction to read ADC data
def adc_callback(*args, **kwargs):
    global adc_buf, adc_idx
    # if buffer size is changed, change 0xff to buffer size - 1
    adc_buf[adc_idx & 0xff] = read_adc_data()
    adc_idx += 1

# Function that continuously upload data
def start():
    global old_idx
    # last_sent = 0
    if running:
        # transfer_tim.deinit()
        print('Started uploading data')
    else:
        return
    while running:
        time.sleep_ms(100)
        # if (((adc_idx & 128) != old_idx) and running):
        if (adc_idx & 128) != old_idx:
            # 128 new samples filled the adc_buf
            old_idx = adc_idx & 128
            if (old_idx):
                # first 128 samples in adc_buf is new
                # print(adc_buf[0:128])
                toSend = {"raw_data":adc_buf[0:128]}
                requests.JSONRequest("http://192.168.0.22:5001/", toSend)
            else:
                # second 128 samples in adc_buf is new
                # print(adc_buf[128:256])
                toSend = {"raw_data":adc_buf[128:256]}
                requests.JSONRequest("http://192.168.0.22:5001/", toSend)
            # now = time.ticks_ms()
            # print('Sent period = ',now-last_sent,' ms')
            # last_sent = time.ticks_ms()

# Buttons callback functions
def btnA_callback(pin):
    global old_idx, adc_idx, running
    if running:
        return
    adc_idx = 0
    old_idx = 0
    # Start reading ADC data and transfer
    ledB.on() # Blue LED as indication
    # ADC used has a fixed sampling rate of 128 SPS
    adc_tim.init(freq = 128, callback = adc_callback)
    print('Started continuously reading ADC output buffer to adc')
    running = True
    # start uploading data 1 second later
    # transfer_tim.init(mode=Timer.ONE_SHOT, period = 1000, callback = start)

def btnB_callback(pin):
    # Stop reading ADC data and transfer
    global running
    if not running:
        return
    running = False
    adc_tim.deinit()
    ledB.off() # Blue LED as indication
    print('Stopped continuously reading ADC output buffer to adc')

def transfer_data(*args, **kwargs):
    global old_idx
    if ((adc_idx & 128) != old_idx):
        # 128 new samples filled the adc_buf
        old_idx = adc_idx & 128
        if (old_idx):
            # first 128 samples in adc_buf is new
            # print(adc_buf[0:128])
            toSend = {"raw_data":adc_buf[0:128]}
            requests.JSONRequest("http://192.168.0.22:5001/", toSend)
            print('Data sent')
        else:
            # second 128 samples in adc_buf is new
            # print(adc_buf[128:256])
            toSend = {"raw_data":adc_buf[128:256]}
            requests.JSONRequest("http://192.168.0.22:5001/", toSend)
            print('Data sent')

# define ADC pin and init
# because ADC2 is not supported on microPython, a wire is added between GPIO13 and GPIO33
batt_mon = machine.Pin(0, machine.Pin.IN)   # set GPIO 0 as high impedance pin for battery voltage monitoring
adc = machine.ADC(machine.Pin(3)) # create ADC object on GPIO 3
adc.atten(machine.ADC.ATTN_11DB)
# adc.width(machine.ADC.WIDTH_12BIT)
adc.width(3)
print('Internal ADC initialised')

# initialise timers
adc_tim = Timer(0)
transfer_tim = Timer(2) # no Timer(1) with ESP32-C3
# transfer_tim.init(mode=Timer.ONE_SHOT, period = 1000, callback = start)
print('Timers initalised')

# initialise buttons and LEDs
btnA = machine.Pin(2, machine.Pin.IN)
btnB = machine.Pin(5, machine.Pin.IN)
ledA = machine.Pin(19, machine.Pin.OUT)
ledB = machine.Pin(4, machine.Pin.OUT)
# set buttons interrupts
btnA.irq(trigger = machine.Pin.IRQ_FALLING, handler = btnA_callback)
btnB.irq(trigger = machine.Pin.IRQ_FALLING, handler = btnB_callback)
print('LEDs and buttons initialised')

# initialise IMU GPIOs
imu_cs = machine.Pin(18, machine.Pin.IN)
imu_int = machine.Pin(1, machine.Pin.IN)

# initialise I2C
i2c = SoftI2C(scl = machine.Pin(9), sda = machine.Pin(8), freq = 100000)
print('SoftI2C initialised with SDA = GPIO_8 and SCL = GPIO_9')

# set second stage gain to minimum
set_gain(0)

# connect WiFI, enter password before executing
ssid = ''
password = ''
connect_wifi(ssid, password)

webrepl.start(password='eeg')

"""
Perquisite:
Flash ESP32-C3 with MicroPython
Upload lib folder to ESP32-C3
Change the WiFi ssid and password of this main.py and upload to ESP32-C3

Instructions:
1. Start JSON server on PC
2. Turn on device
3. After successfully connected to WiFi and webrepl
4. Press button A to start reading ADC into adc_buf, blue LED indicate in operation
5. Run start() function through command interface through USB-to-UART or webrepl
6. Press button B to end data recording and uploading to server
Repeat from step 4

Appendix:
webrepl: http://micropython.org/webrepl/
"""