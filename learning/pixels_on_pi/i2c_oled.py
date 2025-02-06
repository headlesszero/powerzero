"""

Wiring for I2C OLED Display (4-pin)

Black  → GND  (OLED) → GND  (Pin 6, Pi)
Red    → VCC  (OLED) → 3.3V (Pin 1, Pi)
Yellow → SCL  (OLED) → SCL  (Pin 5, GPIO 3, Pi)
Green  → SDA  (OLED) → SDA  (Pin 3, GPIO 2, Pi)

"""

import busio
import board

USE_LUMA = True

if USE_LUMA:
    # Initialize using LUMA Library
    from luma.core.interface.serial import i2c
    from luma.oled.device           import ssd1306
    serial = i2c(port=1, address=0x3C)
    oled = ssd1306(serial, width=128, height=64)

else:
    # Initialize using AdaFruit Library
    import adafruit_ssd1306
    i2c  = busio.I2C(board.SCL, board.SDA)
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

from bounce import bounce
bounce(oled)



