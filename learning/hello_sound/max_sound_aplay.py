import re
import os
import RPi.GPIO as GPIO
import subprocess

from pydub import AudioSegment
import time

# Define the GPIO pin for the SD (Shutdown) control
SD_PIN  = 23  # GPIO 23, Pin #16

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SD_PIN, GPIO.OUT)
GPIO.output(SD_PIN, GPIO.LOW)  # Start with amp off

def get_i2s_device():
    """Automatically detects the correct I2S hardware device (hw:X,0)."""
    result = subprocess.run(["aplay", "-l"], capture_output=True, text=True)
    match = re.search(r"card (\d+): sndrpihifiberry", result.stdout)
    if match:
        return f"hw:{match.group(1)},0"
    else:
        raise RuntimeError("I2S DAC not found!")

def convert(mp3_path: str, volume_change: int = 0):
    """
    Converts an MP3 file to WAV format if it hasn't already been converted.
    Returns the path to the playable WAV file.

    :param mp3_path: Path to the MP3 file.
    :param volume_change: Volume change in decibels (negative to decrease, positive to increase).
    :return: Path to the playable WAV file.
    """
    NUM_CHANNELS = 2

    if volume_change > 0:
        volume_str = f"_p{volume_change:03}"
    else:
        volume_str = f"_m{abs(volume_change):03}"

    wav_path = os.path.splitext(mp3_path)[0] + f"{volume_str}_{NUM_CHANNELS}.wav"

    if os.path.exists(wav_path):
        print(f"Loading {mp3_path} {volume_change}dB")
        return wav_path  # Return existing WAV file if it already exists

    print(f"Converting {mp3_path} {volume_change}dB")

    # Convert MP3 to WAV and adjust volume
    sound = AudioSegment.from_mp3(mp3_path)
    sound = sound.set_channels(NUM_CHANNELS)
    sound = sound + volume_change  # Increase/decrease volume in dB
    sound.export(wav_path, format="wav")

    return wav_path  # Return the newly converted WAV file


# Detect I2S device
i2s_device = get_i2s_device()

# Convert the MP3 file
wav_path = convert("sounds/hello_there.mp3", volume_change=0)

# Enable the amplifier (fixes the pop issue)
GPIO.output(SD_PIN, GPIO.HIGH)  
time.sleep(0.1)  # Short delay to stabilize amp

# Play the WAV file
subprocess.run(["aplay", "-D", i2s_device, wav_path])


# (Optional) Disable the amplifier after playback
GPIO.output(SD_PIN, GPIO.LOW)

# Cleanup GPIO
GPIO.cleanup()

