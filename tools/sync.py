#!/usr/bin/env python3

#
# Dynamically load the Python environment for our VENV
#

import os
import sys
import argparse

# Dynamically resolve the project root and virtual environment path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VENV_PYTHON = os.path.join(PROJECT_ROOT, ".venv", "bin", "python")

# Check if the script is using the correct Python interpreter
if sys.executable != VENV_PYTHON:
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

# Determine the absolute path to the 'git' directory and add it to Pythons sys.path
git_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(git_directory_path)


from hz_bootstrap           import SyncManager, ConfigAccessor
from tools.helpers.config   import PZConfig

def execute_hz_sync(args):
    PZConfig.print_config_selection(args, 'powerzero/sync')

    config  = PZConfig.load_config_accessor(args)
    section = PZConfig.get_configuration(args)


    host = SyncManager.HostDefinition(
                    account   = config.get(section, 'remote_username'),
                    host_name = config.get(section, 'remote_host'),
                    password  = config.get(section, 'remote_password'))

    #
    # TODO: Change watch folders based on mode
    #

    sync = SyncManager(target_host = host,
                       watch_folders = ["learning"], 
                       target_folder = "/projects/powerzero",
                       default_types = [SyncManager.DefaultTypes.ALL])

    sync.start(full_sync = True)


#
# Setup the ARGPARSE
#

if __name__ == "__main__":
    # Argument parser setup
    parser   = argparse.ArgumentParser(description="Synchronize host with Pi")
    PZConfig.add_arguments(parser)
    args     = parser.parse_args()

    # Run the main function with deploy type and environment in the args
    execute_hz_sync(args)

