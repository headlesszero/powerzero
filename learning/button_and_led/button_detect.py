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


If you haven't done LED BLINK yet, please do that or
read the instructions. I'm assuming you've done that to
be less repetitive in this file.

For this project, we're going to get a button working. The electronics kit
came with a "push button" or "tactile button." It's about 3mm x 3mm.

The button has four pins:

1  ~  3
|     |
|  B  | <-- button body. 1-4 are the pins.
|     |
2  ~  4

- Pins 1 and 2 are internally connected.
- Pins 3 and 4 are internally connected.
- When you press the button (B), all four pins are connected.
  - this means all pins effectively cross-connect

Note: 
- The pin pairs (1/2) and (3/4) don't matter for operation.
- The pin pairs (1 & 3) and (2 & 4) hook inwards towards the button.


When the button is not pressed, the circuit is not complete. When you press
the button and hold it down, the circuit is completed.

We can detect this change by connecting one side of the button (e.g., pins 1&2) to
power (3.3V) and the other side (pins 3&4) to a GPIO pin. 

The GPIO pin always needs to read either LOW (0V) or HIGH (3.3V):
- When the button is pressed, the circuit is completed, and the GPIO pin 
  reads 3.3V (HIGH).
- When the button is not pressed, we need the GPIO pin to read 
  0V (LOW). This is done by connecting it to GND.

Now, here’s the important part: 
- When you press the button, it connects the power (3.3V) to both 
  the GPIO pin and GND. This will create a short circuit as the current 
  flows freely to GND.
- To prevent this short circuit, we add a large resistor (e.g., 10,000Ω (10kΩ) 
  between the negative side of the button and GND.
  - NOTE:  It's important you use a huge resistor here.  I used a 10Ω (1/1000th!!)
    and it started to smell.  So I pulled it out and it melted into my thumb. :-(


It took about five minutes to put the board together, and about two hours
for me to get the resistor thing at least partially lodged into my brain.  
So hopefully that's correct.  With that in mind, I'm going to re-explain 
my understanding more succinctly:

- When the button is NOT pressed, the resistor connects the GPIO pin to GND, 
  allowing it to read 0V (LOW).
- When the button IS pressed, the button connects both side of the button pins,
  and the the resistor limits the current flowing to GND, preventing a
  short circuit, while the GPIO pin reads 3.3V (HIGH)

In the LED project we used GPIO4, so in this one we're going to use 17.
This should make it less confusing in the next project when we put them
together.

Also, because this one is starting to add a few wires, I'm going to start
to colour code them so that it's easier for me to trace what's going on.

Steps to build the circuit:
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


Something that drove me crazy for a while is that I found that if I
pressed the button multiple times quickly, the output didn't seem to match
what I was doing.

It turns out that this is a known issue calle "bounce".  You can debounce by
adding a slight delay (E.g. 1/10th of a second) after a change is detected
within which you don't check for a change.  So if press the button, 
we wait 1/10th or 1/20th of a second before we check again.

As it turns out there is a parameter in the button class for this: bounce_time


"""

from gpiozero import Button
from time     import sleep

DEBOUNCE = True


# Set up the button on GPIO17

if DEBOUNCE:
   button = Button(17, pull_up = False, bounce_time=0.1)

else:
   button = Button(17, pull_up = False)

previous_state = button.is_pressed
counter        = 0

print(f"Ready to start pressing!")

while True:
   current_state = button.is_pressed

   if current_state != previous_state:
      previous_state = current_state
      counter       += 1

      if button.is_pressed:
         print(f"Button pressed!  {counter}")

      else:
         print(f"Button released! {counter}")



