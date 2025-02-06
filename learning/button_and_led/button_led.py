"""
LEARNING: BUTTON AND LED
PROJECT1: Detecting a button press

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


If you haven't done LED BLINK or BUTTON DETECT please do that
first as this builds directly on top of those.

In fact, I'm going to assume you already have your board setup
based on the BUTTON DETECT and we're going to add an LED in.

Steps to build the BUTTON circuit:
1. RED: Connect 3.3V power from Pin1 on the Pi to the positive 
   column (+) on the board
2. RED: Connect the column (+) to a row where we'll put the button.  
   -Let's say 15.
3. BUTTON: Connect it so that pins 1 and 2 are on row 15, and pins 3 and 4
   will be on a different row depending on the size of your botton.  
   For me it's row 18.
4. YELLOW: Connect row 18 to something slightly down the board just to give
   yourself more room to work.  I used row 25.
5. YELLOW: Place a yellow cable from row 25 to GPIO17, which is Pin 11 on the Pi
6. RESISTOR: Place a 10,000Ω (10kΩ) resistor from row 25 to the negative (-) column
   - Color code: brown, black, black, orange, gold


We're also going to add teh LED in very similarly to how we did
it in the LED BLINK.  But there are some changes. 

Steps to add on the LED:


1. GREEN: I'm using a green LED, so I'm going to use a green wire to connect
   GPIO4 / Pi pin 7 to the breadboard.  I chose fow 5 to get it above the button.
   This is effectively the (+) as the power will come fro the Pi to here
2. LED: Plug the long end of the LED into row 5, as the power goes from (+) to (-)
        and plug the short end (-) into row 6
3. RESISTOR: Place a 330Ω (enough to get the 3.3V power down enough to not hurt the LED)
   from row 6 into the vertical (-) on the board that is already connected to GND
   - orange, orange, black, brown, gold


Design Concept:
---------------
We have some number of "flash patterns".

A flash pattern is a pattern of on/off commands along with a sleep duration.

Each of those patterns is stored in an array (patterns).

We initialize an index to 0, and we "play" whatever pattern is stored
at the index.  And when we press the button we jump to the next pattern.

Because the sleep period for the pattern could be long (say 5 seconds) and we
want the button to be responsive, we're going to break the sleep into some
number of cycles.  I've chosen 100ms.  This way if you press the button it'll
break out of the pattern and go to the next one within ~100ms.
"""

from gpiozero import Button, LED
from time     import sleep

# Define the GPIO controls
button = Button(17, pull_up = False) # use false to match our circuit design
led    = LED(4)


# Define all our flash patterns
pattern_off    = [('off', 1)]
pattern_slow   = [('on', 1), ('off', 1)]
pattern_fast   = [('on', 0.2), ('off', 0.2)]
pattern_blink  = [('on', 0.1), ('off', 0.1), ('on', 0.1), ('off', 0.1), ('on', 0.1), ('off', 1)]

patterns       = [pattern_off, pattern_blink, pattern_slow, pattern_fast]
pattern_names  = ["off", "blink", "slow", "fast"]

pattern_index  = 0

print(f"\nPress the button to start a pattern.\n")

while True:
   pattern_restart = False
   is_pressed      = False

   # i will be a 0->x-1 based on the pattern length
   for i in range(len(patterns[pattern_index])):

      # If we want to restart the pattern, break out and it'll restart for us
      if pattern_restart:
         break

      action  = patterns[pattern_index][i][0]
      seconds = patterns[pattern_index][i][1]

      if action == 'on':
         led.on()
      else:
         led.off()

      # cycles number of 100ms sleeps
      cycles = max(1, int(float(seconds) / 0.100))
      for _ in range(cycles):
         sleep(0.100)

         if button.is_pressed:
            if not is_pressed:
               # Reset the pattern
               is_pressed      = True
               pattern_restart = True
               pattern_index   = (pattern_index + 1) % len(patterns) # go to the next pattern

               print(f"Blink pattern {pattern_names[pattern_index]}")

         else:
            if is_pressed:
               is_pressed      = False









