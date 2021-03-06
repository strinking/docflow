[![Build Status](https://travis-ci.org/strinking/docflow.svg?branch=master)](https://travis-ci.org/strinking/docflow)
# DocFlow
A Discord Bot written by Members of the [Programming Server](https://discord.gg/010z0Kw1A9ql5c1Qe) 
to evaluate code and search documentation for various languages.

If you are not from the [Programming Discord Server](https://discord.gg/010z0Kw1A9ql5c1Qe),
chances are you have little idea of what this is doing. But worry not! Check out the
[`README.md` file in the `docs` directory](./docs/README.md), it should give you an idea of
what this project is all about - this file is focused around setup instructions.

## Setup
This Project requires a [Python 3.6 Interpreter](https://www.python.org/downloads/) as well
as a bunch of dependencies which you can install by using the following command:
```bash
pip3 install -r requirements.txt
```

## Usage
You need to rename `config-example.json` to `config.json` and put your Discord token into it.
To start the bot, simply use the following command, from the root directory:

```bash
python3 -m docflow
```

If no reference files are found, this will scrape them automatically, which may
take a few minutes. Afterwards, the results are cached in `docflow/.scrapy/httpcache/`,
which will greatly increase the speed at which subsequent scrapes run.

If you wish to manually scrape again, simply run `python3 -m docflow scrape`.

## Contributing
The master branch should always be functional, so adding new features, fixing bugs,
refactoring code or other changes must be worked on within branches. Please push
intermediate commits to the `dev`  branch when they have reached a certain stability.
For discussion and getting your branch merged, please use Pull Requests. 
Also, please make sure to use *descriptive commit messages* so other collaborators
can understand your changes easier. Each commit should represent *one idea*. 
Please view [this](https://guides.github.com/introduction/flow/) for a more 
detailed description of the GitHub Flow.
