"""
PAM8302A Wiring with Bridged Grounds:
--------------------------------------
1. GND (Black)       -> Pin 6 (GND on Raspberry Pi)
2. 5V (Red)          -> Pin 2 (5V Power on Raspberry Pi)
3. Shutdown (Yellow) -> Pin 11 (GPIO17) [Optional: Leave unconnected or tie to 3.3V for always-on]
4. Audio In+ (Green) -> Pin 12 (GPIO18, PWM Audio Signal)
5. Audio In- (Blue)  -> Connected to GND (same line as Black wire)

Notes:
- The Blue wire (Audio In-) is bridged to the Black wire (GND) to ensure a shared ground.
- GPIO18 (Pin 12) is the designated hardware PWM pin for audio signals on the Raspberry Pi.
- The amplifier receives power from Pin 2 (5V) and is optionally controlled via Pin 11 (Shutdown).
- Use this setup to play higher-quality audio, such as WAV files, through the amplifier and connected speaker.

-------------------
-- CRITICAL NOTE --
-------------------
Working through this I discovered that this could do beeps and such but would
NOT be able to play the higher fidelity sound I was looking for (audio files / voice).

I have left this file here in case someone has a PAM8032A, but it's not what I decided
to use for the final product.

"""


import RPi.GPIO as GPIO
import time

print("\nStarting to play tones through PAM8302A amplifier.\n")

# Melody with frequencies (Hz) and durations (seconds)
startup_melody = [
    (659, 0.2),  # E5
    (440, 0.2),  # A4
    (494, 0.3),  # B4
]

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)  # GPIO18 for PWM Audio Signal

    # Start PWM with the first frequency in the melody
    pwm = GPIO.PWM(18, startup_melody[0][0])  
    pwm.start(1)  # 50% duty cycle for balanced output

    # Play the melody
    for hz, secs in startup_melody:
        pwm.ChangeFrequency(hz)  # Change frequency for the tone
        time.sleep(secs)  # Play the tone for the specified duration

finally:
    pwm.stop()          # Stop the PWM signal
    GPIO.cleanup(18)    # Clean up GPIO18 resources

print("Tone playback complete.\n")

