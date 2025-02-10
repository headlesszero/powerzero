import os
import simpleaudio as sa
import RPi.GPIO as GPIO
from pydub import AudioSegment
import time

# Define the GPIO pin for the SD (Shutdown) control
SD_PIN = 23  # GPIO 23, Pin #16

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SD_PIN, GPIO.OUT)
GPIO.output(SD_PIN, GPIO.LOW)  # Start with amp off

def convert(mp3_path: str, volume_change: int = 0):
    """
    Converts an MP3 file to WAV format if it hasn't already been converted.
    Returns the path to the playable WAV file.

    :param mp3_path: Path to the MP3 file.
    :param volume_change: Volume change in decibels (negative to decrease, positive to increase).
    :return: Path to the playable WAV file.
    """

    if volume_change > 0:
        volume_str = f"_p{volume_change:03}"
    else:
        volume_str = f"_m{abs(volume_change):03}"

    wav_path = os.path.splitext(mp3_path)[0] + volume_str + ".wav"

    if os.path.exists(wav_path):
        print(f"Loading {mp3_path} {volume_change}dB")
        return wav_path  # Return existing WAV file if it already exists

    print(f"Converting {mp3_path} {volume_change}dB")

    # Convert MP3 to WAV and adjust volume
    sound = AudioSegment.from_mp3(mp3_path)
    sound = sound + volume_change  # Increase/decrease volume in dB
    sound.export(wav_path, format="wav")

    return wav_path  # Return the newly converted WAV file


# Convert the MP3 file
wav_path = convert("sounds/hello_there.mp3", volume_change=0)

# Enable the amplifier (fixes the pop issue)
GPIO.output(SD_PIN, GPIO.HIGH)  
time.sleep(0.1)  # Short delay to stabilize amp

# Play the WAV file
wave_obj = sa.WaveObject.from_wave_file(wav_path)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait for playback to finish

# (Optional) Disable the amplifier after playback
GPIO.output(SD_PIN, GPIO.LOW)

# Cleanup GPIO
GPIO.cleanup()


