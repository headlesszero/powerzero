import os
import time
import threading

import RPi.GPIO    as GPIO
import simpleaudio as sa

from enum  import Enum
from pydub import AudioSegment


class PAMSound:
    class Clip(Enum):
        STARTUP     = 'tada.mp3'
        BEEP        = 'tone_short.mp3'
        LONG_BEEP   = 'tone_long.mp3'
        HELLO       = 'hello_there.mp3'

    SD_PIN          = 23                        # GPIO for enabling the amplifier
    SAMPLE_RATE     = 48000


    def __init__(self, display):
        # Setup the Amplifier
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SD_PIN, GPIO.OUT)
        GPIO.output(self.SD_PIN, GPIO.HIGH)
        time.sleep(0.250)

        self.display = display

        self.wav_filenames = {}

        for mp3 in PAMSound.Clip:
            self.wav_filenames[mp3.value] = self._convert_mp3(f"sounds/{mp3.value}", 0)

    def __del__(self):
        """ Properly shut down and clean up. """
        GPIO.output(self.SD_PIN, GPIO.LOW)  # Power down amp
        GPIO.cleanup()


    def _convert_mp3(self, mp3_path: str, volume_change: int = 0) -> str:
        """ Converts MP3 to WAV, ensuring mono and consistent sample rate. """
        
        NUM_CHANNELS = 2

        self.display.print(f"Load: {mp3_path.rsplit('/', 1)[-1]}")
        wav_path = os.path.splitext(mp3_path)[0] + f"_m{abs(volume_change):03}_{NUM_CHANNELS}.wav"

        if os.path.exists(wav_path):
            return wav_path  # Use existing converted file


        sound = AudioSegment.from_mp3(mp3_path)
        sound = sound.set_channels(NUM_CHANNELS) 
        sound = sound.set_frame_rate(self.SAMPLE_RATE)

        if volume_change != 0:
            sound = sound + volume_change

        # Apply small fade-in and fade-out to prevent pops
        #sound = sound.fade_in(10).fade_out(10)  # 10ms fade-in/out

        sound.export(wav_path, format="wav", parameters=["-acodec", "pcm_s16le"])
        return wav_path


    def play(self, clip: Clip, wait: bool = False):
        """ Plays a sound file, ensuring no overlap and avoiding 'device busy' errors. """

        wav_path = self.wav_filenames.get(clip.value)
        if not wav_path or not os.path.exists(wav_path):
            print(f"Error: Sound file {wav_path} not found.")
            return

        # Use a threading lock to prevent multiple plays at once
        if hasattr(self, "_play_lock") and self._play_lock.locked():
            return  # Ignore new requests while a sound is playing

        self._play_lock = threading.Lock()

        def _play_sound():
            with self._play_lock:
                wave_obj = sa.WaveObject.from_wave_file(wav_path)
                play_obj = wave_obj.play()
                play_obj.wait_done()        # Block until sound finishes

        # Start a background thread for playback
        play_thread = threading.Thread(target=_play_sound, daemon=True)
        play_thread.start()

        if wait:
            play_thread.join()  # Block until playback completes

