from ulab import numpy as np
import utime as time
from lib.runner import Runner
from lib.utils import connect_wifi
from lib.requests import MicroWebCli as requests

decode_period_s = 4 # decode every x seconds
Nc = 1
Ns = 256
Nt = 3
stim_freqs = [7, 10, 12]
decoding_period_s = 4

ssid = 'TP-Link_AP_4C04'
password = '63525465'
connect_wifi(ssid, password)


runner = Runner('CCA', buffer_size=Ns)
runner.setup()
runner.run()

while True:
    time.sleep(decode_period_s)
    toSend = {"decoded":runner.decode()}
    requests.JSONRequest("http://192.168.0.37:5001/decoded", toSend)