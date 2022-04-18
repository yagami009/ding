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
    "output_amp_gain": 255,  # value between 0-255 controlling gain of output amplifier
}

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