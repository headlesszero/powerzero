
# Getting Things Working

1. sudo sudo sudo

Most operations **require root privileges**, so run all commands with sudo.

2. chmod +x

As of this writing, hz_bootstrap doesn't properly propogate executable (+x) permissions on files.  So you need to do the following:

```bash
sudo chmod +x ./scripts/*.sh
```

3. You MUST Setup the virtual environment.

This project **requires a virtual environment**. Since some libraries are system-level, setup may take a while:

```bash
sudo scripts/setup_venv.sh
```

4. You MUST START the virtual environment

Before running any Python scripts, you must **activate the virtual environment**:

```bash
sudo scripts/start_venv.sh
```

5. Executing the .py samples:  You MUST specify the venv python

**sudo resets environment variables**, so you must explicitly specify the venv **Python interpreter** when executing scripts.

```bash
sudo ./venv/bin/python ./max_sound.py
```


