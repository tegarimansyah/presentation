# =====================
# Default boot.py file
# =====================

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
gc.collect()

# =====================
# Our custom boot.py file
# =====================

import network

# Turn on STA mode to connect a wifi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# Make sure AP mode (access point, make it a hotspot) off
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

ssid = 'YOUR_WIFI_SSID'
password = 'YOUR_WIFI_PASSWORD'

sta_if.connect(ssid, password)
while not sta_if.isconnected():
    # print('Connecting to %s' % (ssid))
    pass

print('Connect to {} successfully'.format(ssid))
