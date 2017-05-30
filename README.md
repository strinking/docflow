# DocFlow
A Discord Bot written by Members of the [Programming Server](https://discord.gg/010z0Kw1A9ql5c1Qe) to evaluate code and browse documentation.

## To Be Done
- [ ] Basic Bot framework, using the commands extension of discord.py
- [ ] Code Evaluation using [Coliru](http://coliru.stacked-crooked.com)
- [ ] Documentation search for various languages

## Setup
This Project requires a [Python 3.6 Interpreter](https://www.python.org/downloads/) as well as the following packages:
- discord.py rewrite ([*Documentation*](http://discordpy.readthedocs.io/en/rewrite/))

Usage of a virtual environment is highly recommended.  
You can setup these using the following commands:
```bash
# Create a virtual environment, activate it
python3 -m venv venv
source venv/bin/activate

# Install discord.py from GitHub
python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite
```

## Usage
You need to set a `DISCORD_TOKEN` environment variable for the Bot to connect to Discord. An easy way to do this by using a Virtual Environment is shown [here](TODO: create wiki page). To start the bot, simply use the following commands:

```bash
# If the virtual environment is not activated yet:
source venv/bin/activate

# Run application
python3 run.py

# When you're done with using it, use `deactivate` to leave the venv
deactivate
```

## Contributing
The master branch **must always be working without any bugs**, so adding new features, fixing bugs, refactoring code or other changes must be worked on within branches. For discussion and getting your branch merged, please use Pull Requests. Also, please make sure to use *descriptive commit messages* so other collaborators can understand your changes easier. Each commit should represent *one idea*. Please view [this](https://guides.github.com/introduction/flow/) for a more detailed description of the GitHub Flow.

Pull Requests are validated through the tests in `test` using **Travis**.
