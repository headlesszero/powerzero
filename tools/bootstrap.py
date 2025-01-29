#!/usr/bin/env python3
"""
BOOTSTRAP:
----------
The intent is to go through the different stages of getting a device from freshly
installed to ready to use.

We handle this with two parameters.  The Deploy Stage, and the Configuration.

Think of the configuration as the purpose.
- dev  -> I'm setting this thing up to work on it
- prod -> I'm setting this thing up to give it to someone

In my opinion, these things are exclusive.  Using HZ_BOOTSTRAP we can take
our project and transition it from a fresh flash of Raspberry OS to something ready to go.


DEPLOY STAGES:
--------------
Within the concept of 'dev' and 'prod' You may want to do different things.  In all
cases you would start with initialize.

INTIALIZE:
- This is the basic setup.  It installs software, updates the system. etc.  You would
  typically do this once.

DEVELOP:
- Optional setting to adjust any configuration values during development.  Like maybe
  you want to enable or disable WiFi.  Tweak the config values based on your needs.

  Develop would typically NOT be used for prod configs.

VALIDATE:
- You want to do some sort of testing, and may require a different configuration
  than what you ultimately ship with.  For example, if you're registering a component
  then putting registration steps into validate would make sense.

FINALIZE:
- You're done and you need to apply final configuration before you "ship".  As an example
  you might not want to have your WiFi embedded in your product before you give it to
  someone.  Or you might not want the logs generated during init/validate to stay on the
  device.  Finalize would contain configuration to adjust those settings or remove the logs.


HOW TO USE:
-----------

- DEV: You would typically just use INITIALIZE every time you flash a disk to get it into
       an expected state for development.  Slower operations that you only want to run
       once you would put into INITIALIZE (like updating all the software).

       And then DEVELOP to fine tune ay configuration.

- PROD: You would typically use INITIALIZE to set everything up, update the system,
        install all the software, etc.  It may add configuration to make it easy to 
        validate (e.g. SSH, WiFi settings).

        You would use VALIDATE to perform any sort of testing or confirmation that
        everything is working as expected and ready to go.

        You would use FINALIZE to cleanup anything required in VALIDATE but that
        you don't want in your final product.  E.g. Your WiFi settings.

- LEARN: Setup specifically for the learning projects, and not for the final
         powerzero project.

"""
import os
import sys
import argparse

#
# Dynamically load the Python environment for our VENV
#

# Dynamically resolve the project root and virtual environment path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VENV_PYTHON = os.path.join(PROJECT_ROOT, ".venv", "bin", "python")

# Check if the script is using the correct Python interpreter
if sys.executable != VENV_PYTHON:
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

from hz_bootstrap import LogColor

#
# Installer function
#

deploy_stages  = ["initialize", "develop", "validate", "finalize"]
configurations = ["dev", "prod", "learn"]

def execute_hz_bootstrap(stage: str, config: str):
    stage  = stage.lower().strip()
    config = config.lower().strip()

    global deploy_stages
    global configurations

    if stage not in deploy_stages:
        print(f"Error: Unknown environment '{stage}'.  Available stages: ({', '.join(deploy_stages)}).")
        sys.exit(1)

    if config not in configurations:
        print(f"Error: Unknown environment '{stage}'.  Available stages: ({', '.join(configurations)}).")
        sys.exit(1)


    stage_list = f"{LogColor.DARK_GRAY.value}[{'] ['.join(deploy_stages)}]{LogColor.RESET.value}"
    stage_list = stage_list.replace(f"[{stage}]", f"{LogColor.BOLD.value}{LogColor.MAGENTA.value}[{stage.upper()}]{LogColor.RESET.value}{LogColor.DARK_GRAY.value}")

    config_list = f"{LogColor.DARK_GRAY.value}[{'] ['.join(configurations)}]{LogColor.RESET.value}"
    config_list = config_list.replace(f"[{config}]", f"{LogColor.BOLD.value}{LogColor.MAGENTA.value}[{config.upper()}]{LogColor.RESET.value}{LogColor.DARK_GRAY.value}")


    # Use 'cls' for Windows and 'clear' for Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{LogColor.UNDERLINE.value}{LogColor.YELLOW.value}Bootstrap:{LogColor.RESET.value}")
    print(f"{LogColor.BLUE.value}Deploy Stage:  {stage_list}")
    print(f"{LogColor.BLUE.value}Configuration: {config_list}")
    print("")

    # Join the current location with the offset
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../config/bootstrap_{stage}.ini")

    # Use hz_bootstrap to deploy the config to the device
    import hz_bootstrap
    try:
        hz_bootstrap.install_config(config_path, config)


    except Exception as e:
        logger = hz_bootstrap.get_logger('example_install')
        logger.exception(str(e))



#
# Read the environment
#

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Install script for initializing the Pi environment.")

    parser.add_argument(
        "-s", "--stage",
        choices=deploy_stages,
        required=True,
        help="Stage of deployment (i.e. start with initialize, end with finalize)"
    )

    parser.add_argument(
        "-c", "--configuration",
        choices=configurations,
        required=True,
        help="Environment configuration (i.e. what's configured and enabled)"
    )

    args = parser.parse_args()

    # Run the main function with deploy type and environment
    execute_hz_bootstrap(args.stage, args.configuration)

