
import re

import time
import busio
import board

from   luma.core.interface.serial   import i2c
from   luma.oled.device             import ssd1306
from   PIL                          import Image, ImageDraw, ImageFont


class OLED:

    def __init__(self):
        self.serial      = i2c(port=1, address=0x3C)
        self.oled        = ssd1306(self.serial, width=128, height=64)
        self.font        = ImageFont.load_default()

        # Calculate max lines based on display height and font height
        self.line_height = self.font.getbbox("A")[1] + self.font.getbbox("A")[3]
        self.max_lines   = self.oled.height // self.line_height
        self.clear()

    def clear(self):
        self.lines = []
        self._draw_text()



    def print(self, string: str):

        #
        # Split the lines and add them
        #
        lines    = re.split(r'(\n|\r)', string+'\n')
        pop_prev = False

        for i in range(0, len(lines) - 1, 2):  # Process pairs (line, separator)
            line      = lines[i]
            separator = lines[i + 1]

            # If we have a line
            if line:
                # If line feed, replace previous line
                if '\r' in separator or pop_prev:
                    pop_prev = False
                    if self.lines:
                        self.lines[-1] = line  # Replace last line
                    else:
                        self.lines.append(line)

                else:
                    self.lines.append(line)

            # No line?  Are we a LF?  Meaning go up a line?
            else:
                pop_prev = True
    
        # Trim our lines
        self.lines = self.lines[-self.max_lines:]
        self._draw_text()


    def _draw_text(self):
        # Caculate where to draw, if not at top
        ypos   = 0
        height = (len(self.lines)+1) * self.line_height

        if height > self.oled.height:
            ypos = self.oled.height - height

        image = Image.new("1", (self.oled.width, self.oled.height))
        draw  = ImageDraw.Draw(image)

        draw.text((0, ypos), '\n'.join(self.lines), font=self.font, fill=255)

        self.oled.display(image)
