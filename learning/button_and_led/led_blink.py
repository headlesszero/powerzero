"""
LEARNING: BUTTON AND LED
PROJECT1: Blinking an LED

Raspberry Pi Pinout:
| 3V3           |  1   |   2  | 5V            |
| GPIO2  (SDA1) |  3   |   4  | 5V            |
| GPIO3  (SCL1) |  5   |   6  | GND           |
| GPIO4         |  7   |   8  | GPIO14  (TX)  |
| GND           |  9   |  10  | GPIO15  (RX)  |
| GPIO17        |  11  |  12  | GPIO18        |
| GPIO27        |  13  |  14  | GND           |
| GPIO22        |  15  |  16  | GPIO23        |
| 3V3           |  17  |  18  | GPIO24        |
| GPIO10 (MOSI) |  19  |  20  | GND           |
| GPIO9  (MISO) |  21  |  22  | GPIO25        |
| GPIO11 (SCLK) |  23  |  24  | GPIO8  (CE0)  |
| GND           |  25  |  26  | GPIO7  (CE1)  |
| GPIO0  (ID_SD)|  27  |  28  | GPIO1  (ID_SC)|
| GPIO5         |  29  |  30  | GND           |
| GPIO6         |  31  |  32  | GPIO12        |
| GPIO13        |  33  |  34  | GND           |
| GPIO19        |  35  |  36  | GPIO16        |
| GPIO26        |  37  |  38  | GPIO20        |
| GND           |  39  |  40  | GPIO21        |


For this project we're going to create a circuit that loops
from the ground wire (GND) which is the -, thorough to a GPIO
pin which is +.

The idea is to create a circuit that will go from the power
through a resistor and then through an LED and then to the GND.

To confirm it's working:
1. Turn Pi Off (Don't know if it matters, can't hurt)
2. Plug a wire from the first GPIO pin #1 -> 3.3V
3. Plug that into the breadboard (+ column)
4. Plug a resistor from the + column into some row next to it.  Say row 20?
5. Plug the LED with the long end into the same row (20) and connect
   short end into the negative (-) column.
6. Plug a wire from a GND pin (I used pin 6) and into the negative (-) column.
7. Turn Pi on and the LED should turn on

-----------------

LED Leg lengths:  I was worried about plugging the LED in wrong, like how do I know
which way it goes?  Well, one leg is shorter (-) and one leg is longer (+).  So
plug the long (+) leg into the positive, and the shorter into the negative (-).

What type of resistor?  I don't know for sure, from YouTube videos some
people have said as low as 50Ω-100Ω, and others have said as high as 500Ω.  And as
far as I can tell, you can plug a resistor in either way.

I asked ChatGPT and it said 330Ω is a good starting point.  The danger zone 
is with lower / less resistance.  Too much resistance means a dimmer or off LED.
- orange, orange, black, brown, gold

Now to move from a straight power circuit to something we can control
I moved the wire from Pin 1 (3.3V) to Pin 7 (GPIO4)

The code below will simply turn the LED on, sleep for X seconds,
turn the LED off, and sleeping for Y seconds.

When you call ON, it will send 3.3V over that pin.  When you call
OFF it will send 0V.

"""

import gpiozero
import time

led = gpiozero.LED(4)

while True:
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(1)



