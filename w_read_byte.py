
from machine import Pin
import utime


dz = Pin(14, Pin.OUT, Pin.PULL_UP)
d1 = Pin(15, Pin.OUT, Pin.PULL_UP)
card_read = Pin(25, Pin.OUT, Pin.PULL_DOWN)
door_pin = Pin(10, Pin.OUT, Pin.PULL_UP)
# valid_read = Pin(9, Pin.IN, Pin.PULL_UP)
BUFFER_SIZE = 40
buf = bytearray(BUFFER_SIZE)

def send_card(card):
    """Send card in binary by using pin outputs"""
    # print_card(card)
    print("card sent")
    card_read.on()
    for i in range(card):
        bit = line_view[i]
        if bit == 48:
            dz.off()
            utime.sleep_us(40)
            dz.on()
        if bit == 49:
            d1.off()
            utime.sleep_us(40)
            d1.on()
        utime.sleep_ms(2)
    card_read.off()
        
def badge_cards():
    """Read binary card number, run card read, then open door."""
    with open('cards.txt', 'rb') as file:
        while True:
            bytes_read = file.readinto(buf)
            
            if bytes_read == 0:
                break
            
            line_view = memoryview(buf)[:bytes_read]
            
            actual_len = bytes_read
            while (actual_len > 0 and
                   lineview[actual_len - 1] in (10, 13, 32)):
                   actual_len -= 1
            
            if actual_len == 0:
                   continue
                   
            send_card(actual_len)
            utime.sleep(1)
            open_door()
            utime.sleep(8)

def open_door():
    door_pin.value(1)
    # print('door open')
    utime.sleep(5)
    door_pin.value(0)

def valid_card():
    print(valid_read.value())
    if valid_read.value() == 0:
        print('valid')
        open_door()

def check_valid():
    current_value = valid_read.value()
    print(current_value)

def print_card(card):
    try:
        card_num = card[-9: 25]
        card_num = int(card_num, 2)
        print(card_num)
    except Exception as err:
        print(f"Error printing card: {err} ")

def main():
    while True:
        badge_cards()
        utime.sleep(30)


if __name__ == '__main__':
    main()