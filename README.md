# mctk

[![Build Status](https://github.com/marcusm117/mctk/workflows/Build%20Status/badge.svg?branch=dev)](https://github.com/marcusm117/mctk/actions?query=workflow%3A%22Build+Status%22) [![codecov](https://codecov.io/gh/marcusm117/mctk/branch/dev/graph/badge.svg)](https://codecov.io/gh/marcusm117/mctk) ![License](https://img.shields.io/badge/License-AGPLv3-green) ![Issues](https://img.shields.io/github/issues/marcusm117/FV_mctk?color=red&label=Issues)

Model Checking Toolkit in Python.


## Overview

`mctk` is a Python library for Explicit-State Model Checking (will also support Symbolic Model Checking and Bounded Model Checking in the future) on general Kripke Structures supporting the CTL(Computation Tree Logic) operators: EX, EU, and EG.

Users can create checker instances to formally verify if a Kripke Structure (can be created during runtime or input in a JSON file) satisfies certain CTL properties. The checker instance will return "SAT" if satisfied and an Error Trace if unsatisfied.


## Getting Started
### Installation
1. Clone this Repository to your Local Environment
   ``` bash
   git clone https://github.com/[YOUR USERNAME]/mctk.git
   ```
2. Install the Library with all Dependencies
   ``` bash
   make develop
   ```


### Linting & Testing
- `make lint`: perform static analysis of this library with `black`, `flake8` and `pylint`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information


## Contributing

1. **[Optional]** Open a New Issue
2. Fork this Repository to your Github
3. Clone your Fork to your Local Environment
   ```bash
   git clone https://github.com/[YOUR USERNAME]/mctk.git
   ```
4. Create a New Branch for an Open Issue
   ```bash
   git checkout -b MCTK-[NUMBER]
   ```
5. Commit your Changes
   ```bash
   git commit -m "meaningful commit message"
   ```
6. Push to the Branch to your Fork
   ```bash
   git push origin MCTK-[NUMBER]
   ```
7. Open a Pull Request against this Repository
