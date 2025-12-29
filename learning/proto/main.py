import gpiozero
import time

from modules.sound import PAMSound
from modules.oled  import OLED

GPIO_LED    = 26
GPIO_BUTTON = 4



# Turn on the status led immediately on startup
status_led = gpiozero.LED(GPIO_LED)
status_led.on()

# Get our button ready
button = gpiozero.Button(GPIO_BUTTON, pull_up = True)

# Start the display
oled = OLED()
oled.print("Initializing...\r")

# Load the sound manager
sound = PAMSound(oled)
sound.play(PAMSound.Clip.STARTUP, False)

# Turn the LED off since we're ready
status_led.off()
oled.clear()
oled.print("Proto - 0")


POLL_TIME       = 0.1
LONG_PRESS_TIME = 1.5

was_pressed     = False
was_long_press  = False
press_time      = 0
press_count     = 0

try:
    while True:
        if button.is_pressed:

            # Records a NEW press
            if not was_pressed:
                was_pressed = True
                press_time  = time.monotonic()
                status_led.on()

                sound.play(PAMSound.Clip.BEEP)
                oled.print(f"\rProto - {press_count+1}")
                press_count += 1

            # Existing press?  See how long if not already a long press
            elif not was_long_press:
                seconds = float(time.monotonic() - press_time)
                if seconds >= LONG_PRESS_TIME:
                    # Long press detected, play a sound
                    sound.play(PAMSound.Clip.LONG_BEEP)
                    was_long_press = True

                    # Turn off the LED
                    status_led.off()

                    # Reset the screen
                    press_count = 0
                    oled.clear()
                    oled.print(f"\rProto - {press_count}")


        else:
            was_pressed    = False
            was_long_press = False
            status_led.off()

        time.sleep(POLL_TIME)

except KeyboardInterrupt:
    print("\rExit.\n");

