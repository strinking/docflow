# DocFlow
A Discord Bot written by Members of the [Programming Server](https://discord.gg/010z0Kw1A9ql5c1Qe) to evaluate code and browse documentation.

### Setup
This Project requires a [Python 3.6 Interpreter](https://www.python.org/downloads/) as well as the following packages:
- discord.py rewrite

Usage of a virtual environment is highly recommended.  
You can setup these using the following commands:
```bash
# Create a virtual environment, activate it
python3 -m venv venv
source venv/bin/activate

# Install discord.py from GitHub
python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite
```

### Usage
You need to set a `DISCORD_TOKEN` environment variable for the Bot to connect to Discord. An easy way to do this by using a Virtual Environment is shown [here](TODO: create wiki page). To start the bot, simply use the following commands:

```bash
# If the virtual environment is not activated yet:
source venv/bin/activate

# Run application
python3 run.py

# When you're done with using it, use `deactivate` to leave the venv
deactivate
```
