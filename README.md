# Model Checking Toolkit (MCTK)

[![PyPI](https://img.shields.io/pypi/v/mctk-py?color=blue&label=PyPI)](https://pypi.org/project/mctk-py/) [![Build Status](https://github.com/marcusm117/mctk/workflows/Build%20Status/badge.svg?branch=dev)](https://github.com/marcusm117/mctk/actions?query=workflow%3A%22Build+Status%22) [![codecov](https://codecov.io/gh/marcusm117/mctk/branch/dev/graph/badge.svg)](https://codecov.io/gh/marcusm117/mctk) [![License](https://img.shields.io/badge/License-Apache_2.0-green)](https://github.com/marcusm117/mctk/blob/dev/LICENSE) [![Issues](https://img.shields.io/github/issues/marcusm117/FV_mctk?color=red&label=Issues)](https://github.com/marcusm117/mctk/issues)

Model Checking Toolkit for Python.

## Overview

`mctk` is a Python library for Explicit-State Model Checking (will also support Symbolic Model Checking and Bounded Model Checking in the future) on Kripke Structures (will also support other Transition Systems) supporting the CTL(Computation Tree Logic) operators: EX, EU, and EG.

Users can create checker instances to formally verify if a Kripke Structure (can be created during runtime or input in a JSON file) satisfies certain CTL properties. The checker instance will return a set of satisfying states and "SAT" if satisfied or an Error Trace if unsatisfied.

## Getting Started

### Installation

Get the latest version of `mctk` from PyPI:

   ``` bash
   pip3 install mctk-py
   ```

If you are having trouble with `pip3`, you can also install from the source code, see [Developing](#developing).

### Developing

Clone this Repository to your Local Environment

   ``` bash
   git clone https://github.com/marcusm117/mctk.git
   ```

Go into the Repository Directory

   ``` bash
   cd mctk
   ```

Install the Library with all Dependencies

   ``` bash
   make develop
   ```

### Linting & Testing

We use a `Makefile` as a command registry:

- `make format`: autoformat  this library with `black`
- `make lint`: perform static analysis of this library with `black`, `flake8` and `pylint`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information

## Usage

``` python
from mctk import KripkeStruct

ks = KripkeStruct()
ks.set_atoms(["p", "q"])
ks.add_state("s0", 0b10)
ks.add_state("s1", 0b01)
ks.set_start(["s0"])
ks.add_trans({"s0": ["s1"], "s1": ["s0"]})
```

## Contributing

All contrbutions are welcome!

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.
