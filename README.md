# DocFlow
A Discord Bot written by Members of the [Programming Server](https://discord.gg/010z0Kw1A9ql5c1Qe) 
to evaluate code and search documentation for various languages.

## Setup
This Project requires a [Python 3.6 Interpreter](https://www.python.org/downloads/) as well
as a bunch of dependencies which you can install by using the following command:
```bash
pip3 install -r requirements.txt
```

## Usage
*Note: To get started as fast as possible, simply run `make firstrun`*.

You need to set a `DISCORD_TOKEN` environment variable for the Bot to connect to Discord. 
To start the bot, simply use the following command, from the root directory:

```bash
python3 -m docflow
```

Additionally, if you wish to enable the documentation search functionality found in
`src/bot/doc.py`, you need to run `make scrape` in order to scrape the required 
reference files from various documentation pages.

## Contributing
The master branch should always be functional, so adding new features, fixing bugs,
refactoring code or other changes must be worked on within branches. 
For discussion and getting your branch merged, please use Pull Requests. 
Also, please make sure to use *descriptive commit messages* so other collaborators
can understand your changes easier. Each commit should represent *one idea*. 
Please view [this](https://guides.github.com/introduction/flow/) for a more 
detailed description of the GitHub Flow.
