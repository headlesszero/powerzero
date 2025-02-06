"""
Wiring for SPI OLED Display (7-pin)

Black  → GND  (OLED)  → GND  (Pin 6, Pi)
Red    → VCC  (OLED)  → 3.3V (Pin 1, Pi)
Yellow → SCK  (OLED)  → SCK  (Pin 23, GPIO 11, Pi)  # Corrected from SCL
Green  → MOSI (OLED)  → MOSI (Pin 19, GPIO 10, Pi)
White  → RES  (OLED)  → GPIO 4  (Pin 7, Pi)
Blue   → DC   (OLED)  → GPIO 6  (Pin 31, Pi)

IF using more than one SPI device:
Orange → CS   (OLED)  → GPIO 5  (Pin 29, Pi)

ELSE (if OLED is the only SPI device):
Orange → CS   (OLED)  → GND (Pin 6, Pi)  # CS is grounded

# Also need to enable SPI in config.txt
dtparam=spi=on

"""


# Disable GPIO warnings that popped up as I was first getting it working
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from luma.core.interface.serial import spi
from luma.oled.device           import sh1106


# Set CS pin based on wiring choice
USE_GPIO_CS = False  # We're using ground for test setup

if USE_GPIO_CS:
    serial = spi(device=0, port=0, gpio_DC=6, gpio_RST=4, gpio_CS=5)  # CS as GPIO 5
else:
    serial = spi(device=0, port=0, gpio_DC=6, gpio_RST=4, gpio_CS=None)  # CS grounded

# Initialize OLED display
oled = sh1106(serial, width=128, height=64, rotate=0)

from bounce import bounce
bounce(oled)

