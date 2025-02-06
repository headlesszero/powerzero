
#
# Initialize the i2c device
#

from luma.core.interface.serial import i2c
from luma.oled.device           import ssd1306

serial = i2c(port=1, address=0x3C)
oled = ssd1306(serial, width=128, height=64)

#
# Initialize the SPI device
#

import RPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.oled.device           import sh1106

# Disable GPIO warnings
GPIO.setwarnings(False)

serial = spi(device=0, port=0, gpio_DC=6, gpio_RST=4, gpio_CS=None)  # CS grounded
oled2 = sh1106(serial, width=128, height=64, rotate=0)

#
# Bounce!
#
from bounce import bounce
bounce(oled, oled2)
