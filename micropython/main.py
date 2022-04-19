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
adcread = adc.read()

##################################################################################

DEFAULT_SPI_PARAMS = {
    "spi_num": 2,
    "sck": 18,
    "mosi": 23,
    "miso": 19,
    "output_amp_gain": 50,  # value between 0-255 controlling gain of output amplifier
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

# data = bytearray([17, DEFAULT_SPI_PARAMS['output_amp_gain']])
data = bytearray(DEFAULT_SPI_PARAMS['output_amp_gain'])
# data = bytearray(100)
spi.write(data)

ssid = 'TP-Link_AP_4C04'
password = '63525465'
connect_wifi(ssid, password)

###############################################################################

adc_sample = []
pot_size = 512

def sample_callback(*args, **kwargs):
    global adc_sample
    if len(adc_sample) > pot_size:
        del adc_sample[0]
        adc_sample.append(adc.read())
    else:
        adc_sample.append(adc.read())

sample_timer = Timer(0)
sample_timer.init(freq=pot_size, callback=sample_callback)

for i in range(30):
    time.sleep(1)
    print(gc.mem_free())
    data = adc_sample
    toSend = {"raw_data":data}
    print(toSend)
    requests.JSONRequest("http://192.168.0.37:5001/collect", toSend)

requests.GETRequest("http://192.168.0.37:5001/save")