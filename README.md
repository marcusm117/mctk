# Model Checking Toolkit (MCTK)

[![PyPI](https://img.shields.io/pypi/v/mctk-py?color=blue&label=PyPI)](https://pypi.org/project/mctk-py/) [![CI](https://github.com/marcusm117/mctk/workflows/CI/badge.svg?branch=dev)](https://github.com/marcusm117/mctk/actions?query=workflow%3A%22Build+Status%22) [![codecov](https://codecov.io/gh/marcusm117/mctk/branch/dev/graph/badge.svg)](https://codecov.io/gh/marcusm117/mctk) [![Docs](https://github.com/marcusm117/mctk/workflows/Docs/badge.svg?branch=dev)](https://marcusm117.github.io/mctk/) [![License](https://img.shields.io/badge/License-Apache_2.0-green)](https://github.com/marcusm117/mctk/blob/dev/LICENSE) [![Issues](https://img.shields.io/github/issues/marcusm117/FV_mctk?color=red&label=Issues)](https://github.com/marcusm117/mctk/issues)

[Model Checking Toolkit for Python.](https://marcusm117.github.io/mctk/)

## Overview

`mctk` is a Python library for Explicit-State Model Checking (will also support Symbolic Model Checking and Bounded Model Checking in the future) on Kripke Structures (will also support other Transition Systems) supporting the CTL(Computation Tree Logic) operators: **EX, EU, EG, EF, AX, AU, AG, AF**, and the Propositional Logic operators: **NOT, AND, OR, IMPLIES, IFF**.

Users can use functions that implements CTL operators to formally verify if a Kripke Structure (can be created during runtime or input in a JSON file) satisfies certain CTL properties. All checking functions will return a set of states that satisfy the CTL property, which means that if any start state of the Kripke Structure is in the returned set, then the Kripke Structure satisfies the CTL property.

## Getting Started

### Installation

Get the latest version of `mctk` from PyPI. Note that the registered name is `mctk-py` on PyPI due to the strict typo-squatting prevention mechanism of the registry. However, when using the library, you should import it as `mctk`.

   ``` bash
   pip3 install mctk-py
   ```

If you are having trouble with `pip3`, you can also install from the source code, see [Developing](#developing).

### Developing

Clone this Repository to your Local Environment.

   ``` bash
   git clone https://github.com/marcusm117/mctk.git
   ```

Go into the Repository Directory.

   ``` bash
   cd mctk
   ```

Install the Library with all Dependencies.

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

### Create a Kripke Structure from Scratch

``` python
from mctk import *

# create a Kripke Structure from scratch
ks = KripkeStruct()

# set 2 Atomic Propositions in this Kripke Structure
ks.set_atoms(["p", "q"])

# add 2 states to the Kripke Structure
# a State Name is represented by a string, it must be unique
# a State Label is represented by a binary number, it must be unique
# for example, 0b10 means the state has the Atoms "p" but not "q"
ks.add_state("s0", 0b10)
ks.add_state("s1", 0b01)

# set the Start States of the Kripke Structure
# there can be multiple Start States
ks.set_starts(["s0"])

# add 2 Transitions to the Kripke Structure
# a Transition is represented by a key-value pair
# where key the Source State Name and value is a list of Destination State Names
ks.add_trans({"s0": ["s1"], "s1": ["s0"]})
```

### Checking Simple CTL Formula on the Kripke Structure

``` python
# check if the Kripke Structure satisfies the CTL formula: EX p
# SAT_atom(ks, "p") returns a set of states that satisfy the Atomic Proposition p
# EX returns a set of states that satisfy the CTL formula EX p
sat_states = EX(ks, SAT_atom(ks, "p"))

# the result should be {"s1"}
# since the start state "s0" is not in sat_states, ks doesn't satisfy the CTL formula
assert sat_states == {"s1"}

# check if the Kripke Structure satisfies the CTL formula: E p U q
# SAT_atom(ks, "p") returns a set of states that satisfy the Atomic Proposition p
# SAT_atom(ks, "q") returns a set of states that satisfy the Atomic Proposition q
# EU returns a set of states that satisfy the CTL formula E p U q
sat_states = EU(ks, SAT_atom(ks, "p"), SAT_atom(ks, "q"))

# the result should be {"s0", "s1"}
# since the start state "s0" is in sat_states, ks satisfies the CTL formula
assert sat_states == {"s0", "s1"}
```

### Checking Composite CTL Formula on the Kripke Structure

``` python
# check if the Kripke Structure satisfies the CTL formula: EX (p AND EX q)
sat_states = EX(ks, AND(SAT_atom(ks, "p"), EX(ks, SAT_atom(ks, "q"))))

# the result should be {"s1"}
# since the start state "s0" is not in sat_states, ks doesn't satisfy the CTL formula
assert sat_states == {"s1"}

# check if the Kripke Structure satisfies the CTL formula: EG (A p U (NOT q))
sat_states = EG(ks, AU(ks, SAT_atom(ks, "p"), NOT(ks, SAT_atom(ks, "q"))))

# the result should be set(), empty set
# since the start state "s0" is not in sat_states, ks doesn't satisfy the CTL formula
assert sat_states == set()
```

### Checking CTL formula on a Complex Kripke Structure

``` python
ks_json = {
   "Atoms": ["a", "b", "c", "d"],
   "States": {
      "s1": 0b1000,  # s1 has labels "a"
      "s2": 0b1100,  # s2 has labels "a", "b"
      "s3": 0b0110,  # s3 has labels "b", "c"
      "s4": 0b0111,  # s4 has labels "b", "c", "d"
      "s5": 0b0100,  # s5 has label "b"
      "s6": 0b0010,  # s6 has label "c"
      "s7": 0b0001,  # s7 has label "d"
      },
      "Starts": ["s1"],
      "Trans": {
         's1': ['s2'],
         's2': ['s3', 's4'],
         's3': ['s4'],
         's4': ['s7'],
         's5': ['s6'],
         's6': ['s7', 's5'],
         's7': ['s5'],
         },
}
ks = KripkeStruct(ks_json)

# check if the Kripke Structure satisfies the CTL formula: EX a
sat_states = EX(ks, SAT_atom(ks, "a"))

# the result should be {"s2"}
# since the start state "s1" is not in sat_states, ks doesn't satisfy the CTL formula
assert sat_states == {"s2"}

# check if the Kripke Structure satisfies the CTL formula: E a U b
sat_states = EU(ks, SAT_atom(ks, "a"), SAT_atom(ks, "b"))

# the result should be {'s1', 's2', 's3', 's4', 's5'}
# since the start state "s1" is in sat_states, ks satisfies the CTL formula
assert sat_states == {'s1', 's2', 's3', 's4', 's5'}

# check if the Kripke Structure satisfies the CTL formula: EG a
sat_states = EG(tmp_ks, SAT_atom(tmp_ks, "a"))

# the result should be set()
# since the start state "s1" is not in sat_states, ks doesn't satisfy the CTL formula
assert sat_states == set()
```

## Contributing

All contrbutions are welcome!

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.
