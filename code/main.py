from machine import Pin as pin
from neopixel import NeoPixel as neopixel
import time
from umqtt.simple import MQTTClient

username = 'YOUR_ADAFRUIT_USERNAME'
password = 'YOUR_ADAFRUIT_KEY'

table_topic = username + '/feeds/bedroom.table-lamp'
room_topic = username + '/feeds/bedroom.room-lamp'

lamp = pin(0, pin.OUT)

# 16 Bit LED in pin 2
np_pin = pin(2, pin.OUT)
np = neopixel(np_pin, 16)

def change_same_color(color, delay=0, led=[x for x in range(0,16)]):
    for i in led:
        np[i] = color
        time.sleep(delay/1000)
        np.write()  

def table_lamp(hex_color):
    # split color msg to r,g,b
    r,g,b = [hex_color[i:i+2] for i in range(0, len(hex_color), 2)]
    # hex to decimal
    r,g,b = int(r,16), int(g,16), int(b,16)
    # change all color of neopixel
    change_same_color((r,g,b))

def room_lamp(msg):
    if msg.lower() == 'on':
        lamp.off()
    else:
        lamp.on()

def sub_cb(topic, msg):
    print(topic, msg)
    topic = topic.decode('UTF-8')
    msg = msg.decode('UTF-8')
    if topic == table_topic:
        table_lamp(msg.strip('#'))
    else:
        room_lamp(msg)

def main():
    print('Connecting to Server')
    c = MQTTClient("ESP_light", server='io.adafruit.com', port=1883, user=username, password=password)
    c.set_callback(sub_cb)
    c.connect()

    c.subscribe(table_topic.encode('UTF-8'))
    c.subscribe(room_topic.encode('UTF-8'))

    while True:
        c.wait_msg()
        
    c.disconnect()
  
if __name__ == "__main__":
    change_same_color((0,0,0))
    main()
