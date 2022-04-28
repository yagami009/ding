import machine
from machine import Pin
from machine import ADC, SPI
import time
from machine import Timer
import gc
from machine import freq
from lib.utils import connect_wifi
from lib.requests import MicroWebCli as requests
import ujson as json

freq(240000000)
adc = ADC(Pin(33))
adc.atten(machine.ADC.ATTN_11DB)
adc.width(machine.ADC.WIDTH_12BIT)

##################################################################################

DEFAULT_SPI_PARAMS = {
    "spi_num": 2,
    "sck": 18,
    "mosi": 23,
    "miso": 19,
    "output_amp_gain": 255,  # value between 0-255 controlling gain of output amplifier
}

get_param = lambda key: Pin(DEFAULT_SPI_PARAMS[key])
temp_spi_params = {key: get_param(key) for key in ["sck", "miso", "mosi"]}

spi = SPI(
    2,
    baudrate=10000000,
    polarity=0,
    phase=0,
    sck=Pin(18),
    mosi=Pin(23),
    miso=Pin(19),
)

# setting gain #

data = bytearray([17,DEFAULT_SPI_PARAMS['output_amp_gain']])
cs = machine.Pin(5, machine.Pin.OUT)

# have to turn GPIO 5 off before writing the gain

cs.off() 
spi.write(data)
cs.on() 

# will change lol
ssid = 'TP-Link_AP_4C04'
password = '63525465'
connect_wifi(ssid, password)

###############################################################################

adc_sample = []

# set for frequency the adc should be read and set the size of the array to send every t seconds 
pot_size = 256
sampling_rate = 64

def sample_callback(*args, **kwargs):
    global adc_sample
    if len(adc_sample) >= pot_size:
        # fifo
        del adc_sample[0]
        adc_sample.append(adc.read())
    else:
        adc_sample.append(adc.read())

sample_timer = Timer(0)
sample_timer.init(freq=sampling_rate, callback=sample_callback)

requests.JSONRequest("http://192.168.0.37:5001/message", {"message": "### LOOK AT 7 HZ ###"})
time.sleep(10)

decode_period = 4
#send 7hz data
for i in range(4):
    time.sleep(decode_period)
    data = adc_sample
    toSend = {"7":data}
    requests.JSONRequest("http://192.168.0.37:5001/7hz", toSend)
    
requests.JSONRequest("http://192.168.0.37:5001/message", {"message": "### LOOK AT 10 HZ ###"})
time.sleep(10)

#send 10hz data
for i in range(4):
    time.sleep(decode_period)
    data = adc_sample
    toSend = {"10":data}
    requests.JSONRequest("http://192.168.0.37:5001/10hz", toSend)

requests.JSONRequest("http://192.168.0.37:5001/message", {"message": "### LOOK AT 12 HZ ###"})
time.sleep(5)

#send 12hz data
for i in range(4):
    time.sleep(decode_period)
    data = adc_sample
    toSend = {"12":data}
    requests.JSONRequest("http://192.168.0.37:5001/12hz", toSend)

requests.GETRequest("http://192.168.0.37:5001/isCalibrated")

while True:
    time.sleep(decode_period)
    data = adc_sample
    toSend = {"raw_data":data}
    requests.JSONRequest("http://192.168.0.37:5001/decode", toSend)