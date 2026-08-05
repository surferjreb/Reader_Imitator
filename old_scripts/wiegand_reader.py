"""Reads in Wiegand cards and outputs them to system.  Activating a Door
   contact after card is read.
   @author: James R. Brown
"""

from machine import Pin
import utime


dz = Pin(14, Pin.OUT, Pin.PULL_UP)
d1 = Pin(15, Pin.OUT, Pin.PULL_UP)
card_read = Pin(25, Pin.OUT, Pin.PULL_DOWN)
door_pin = Pin(10, Pin.OUT, Pin.PULL_UP)
valid_read = Pin(9, Pin.IN, Pin.PULL_UP)


def run_card(card):
    print(card)
    print_card(card)
    card_read.on()
    for bit in card:
        if bit == '0':
            dz.off()
            utime.sleep_us(40)
            dz.on()
        if bit == '1':
            d1.off()
            utime.sleep_us(40)
            d1.on()
        utime.sleep_ms(2)
    card_read.off()
        
def read_cards():
    with open('cards.txt', 'r') as file:
        for line in file:
            card = line.strip('\n')
            print(f"Before: {valid_read.value()}")
            run_card(card)
            utime.sleep(2)
            valid_card()
            utime.sleep(8)
            
def open_door():
    door_pin.on()
    utime.sleep(2)
    door_pin.off()

def valid_card():
    print(valid_read.value())
    if valid_read.value() == 0:
        open_door()

def print_card(card):
    if card:
        card_num = card[-9: 25]
        card_num = int(card_num, 2)
        print(card_num)

def main():
    while True:
        read_cards()
        utime.sleep(30)


if __name__ == '__main__':
    main()
    
        
            


        