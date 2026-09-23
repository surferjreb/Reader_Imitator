"""Imitates Wiegand Reader output to a Door Controller.
   @author: James R. Brown
"""


from machine import Pin
import utime
import errno


dz = Pin(14, Pin.OUT, Pin.PULL_UP)
d1 = Pin(15, Pin.OUT, Pin.PULL_UP)
card_read = Pin(25, Pin.OUT, Pin.PULL_DOWN)
door_pin = Pin(10, Pin.OUT, Pin.PULL_DOWN)
valid_read = Pin(9, Pin.IN, Pin.PULL_UP)

BUFFER_SIZE = 32
buf = bytearray(BUFFER_SIZE)

def send_card(card):
    """Send card byte by using pin outputs to interface."""

    print(card)
    
    card_read.on()
    for i in range(len(card)):
        bit = card[i]
        if bit == 48:
            dz.off()
            utime.sleep_us(50)
            dz.on()
        if bit == 49:
            d1.off()
            utime.sleep_us(50)
            d1.on()
        utime.sleep_ms(2)
    card_read.off()
    print("card sent")
        
def badge_cards():
    """Read card number into bytearray buf, pass buf to send_card(),
       run valid_card().
    """
    with open('cards.txt', 'rb') as file:
        for line in file:
            buf = line

            if buf == 0:
                break

            send_card(buf)
            utime.sleep(2)
            valid_card()
            utime.sleep(8)

def open_door():
    """Activates a Relay to simulate door contact"""
    door_pin.value(1)
    # print('door open')
    utime.sleep(5)
    door_pin.value(0)

def valid_card():
    """checks the valid_read pin value, activates open_door()
       if card was valid/strike fired.
    """
    # print(valid_read.value())
    if valid_read.value() == 0:
        print('valid card')
        open_door()
    else:
        print("invalid")

def main():
    err_message = ("Error: \"cards.txt\" not found"
                   " or card file is named incorrectly.")

    while True:
        try:
            badge_cards()
            utime.sleep(30)
        except OSError as err:
            if err.args[0] == errno.ENOENT:
                print(err_message)
                break;
            else:
                print(err)


if __name__ == '__main__':
    main()
