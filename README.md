# FV_mltk
Model Checking Toolkit in Python

![GitHub](https://img.shields.io/badge/License-AGPLv3-green)


## Overview
`mctk` is a Python library for Explicit-State Model Checking (will also support Symbolic Model Checking and Bounded Model Checking in the future) on general Kripke Structures supporting the CTL(Computation Tree Logic) operators: EX, EU, and EG.

Users can create checker instances to formally verify if a Kripke Structure (can be created during runtime or input in a JSON file) satisfies certain CTL properties. The checker instance will return "SAT" if satisfied and an Error Trace if unsatisfed.
