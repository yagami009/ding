import gc
from micropython import alloc_emergency_exception_buf

# allocate exception buffer for ISRs
alloc_emergency_exception_buf(100)

# enable and configure garbage collection
gc.enable()
gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

from machine import Pin
import time

p26 = Pin(26, Pin.OUT)
p13 = Pin(13, Pin.OUT) 
p26.on()
p13.on()

counter = 0
while counter !=10:
    if (counter % 2 == 0):
        p26.on()
        p13.off()
    else:
        p13.on()
        p26.off()
    time.sleep(1)
    counter+=1

from lib.utils import connect_wifi, load_env_vars

env_vars = load_env_vars("lib/.env")
# connect WiFI
ssid = env_vars.get("WIFI_SSID")
password = env_vars.get("WIFI_PASSWORD")
connect_wifi(ssid, password)

import webrepl
webrepl.start()

p26.on()
p13.on()