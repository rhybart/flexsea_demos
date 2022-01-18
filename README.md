# FlexSEA Demos

This repo contains demo scripts for the open-source [flexSEA library](https://pypi.org/project/flexsea/). The idea is for these demos to serve as both sanity checks for making sure flexSEA is working correctly as well as blueprints for how certain tasks can be accomplished with the library.

## Installation

The demos can be installed by cloning the repo and then running pip. It is strongly recommended to install in a new virtual environment. For that you'll need [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) or [poetry](https://python-poetry.org/).

```bash
git clone https://github.com/jcoughlin11/flexsea_demos
cd flexsea_demos
```

### Pip

To install globally:

```bash
pip install .
```

### Virtual environment

If you want to create a virtual environment using `virtualenv`:

```bash
mkdir ~/.venvs
virtualenv ~/.venvs/flexsea_demos_env
source ~/.venvs/flexsea_demos_env/bin/activate
pip install .
```

### Poetry

First [install poetry](https://python-poetry.org/docs/#installation). Once installed:

```bash
poetry shell
poetry install
```

The first command creates a new virtual environment and the second installs `flexsea_demos` along with all of its dependencies.


## Usage

The basic usage pattern is:

```bash
flexsea_demos <command> <parameter_file>
```

To see a list of the available commands:

```bash
flexsea_demos -h
```

Each demo is fully configurable via a parameter file. Sample parameter files for each demo can be found in the `param_files` directory, and they utilize the [yaml](https://en.wikipedia.org/wiki/YAML) format.

The parameter files are source controlled, so you can feel free to make changes to them directly and then, should you desire to get back to the original version, simply check it out:

```bash
git checkout <parameter_file>
```

Alternatively, you can make a copy of the parameter file you're interested in and make changes to that.

It is **strongly** recommended that you run the demos outside of the `flexsea_demos` directory. One example of where to run them is:

```bash
mkdir -p ~/code/sandbox/python/flexsea_demos
cp param_files/*.yaml ~/code/sandbox/python/flexsea_demos
cd ~/code/sandbox/python/flexsea_demos
```

Then, if you want to run, say, the `read_only` demo, you would do:

```bash
flexsea_demos read_only read_only_params.yaml
```
