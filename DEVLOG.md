
CURRENT STATE
- Need to verify all requirements
- Was confusion on the sound card and stuff.. I thought i had a sound card.  Id on't.



# What we need to install

sudo apt-get update


## PIP
sudo apt-get install python3-pip -y

## FFMPEG
sudo apt-get install ffmpeg -y

## LIBSOUND
sudo apt-get install libasound2-dev


PI REQUIREMENTS:
pydub # audio


## Configuraiton for Audio Output

/boot/config.txt


Note: It's OK to have more than one DT Overlay....  need to adjust config stuff

dtparam=audio=on
audio_pwm_mode=2
hdmi_ignore_edid_audio=1
dtoverlay=vc4-kms-v3d,noaudio

## New AUdio Config Component:

Realistic Audio Output Options for Raspberry Pi
    1.  HDMI:
    •   Outputs audio through the HDMI connection.
    •   Best for setups where the Pi is connected to a monitor or TV with speakers.
    2.  PWM (3.5mm Jack / GPIO):
    •   Uses the onboard PWM system to generate analog audio.
    •   Can be output to the 3.5mm jack or GPIO pins (e.g., for a PAM8302A amplifier).
    •   Suitable for small speakers, buzzer-like devices, or custom audio setups.
    3.  USB Audio:
    •   For external USB sound cards or USB headphones/speakers.
    •   Ideal for higher-quality audio requirements or for adding an external DAC.
    4.  I2S (External DAC/Amplifier):
    •   For advanced users using external I2S audio DACs or amplifiers.
    •   Examples: HiFiBerry, IQAudio DACs.
    •   Offers higher fidelity than PWM.
    5.  Bluetooth Audio (if enabled):
    •   For Bluetooth speakers or headphones.
    •   Requires additional setup but can be used wirelessly.

# Audio Settings
audio_mode = pwm
audio_volume = 50

# Optional: PWM-Specific Config
audio_pwm_gpio = 18

# Optional: Fallback
audio_fallback = hdmi

