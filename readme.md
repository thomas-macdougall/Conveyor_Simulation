# Conveyor Belt Assembly Simulation

## Overview

This script simulates a conveyor belt assembly line.

I have added the ability to have many different components, however, I have restricted it to 2 for the purpose of this simulation.

## Usage

Run the script with the following command, including any optional arguments:

'''
python conveyor_simulation.py [--iterations N] [--components C1 C2] [--chance X Y] [--stations N] [--workers N] [--time N] [--debug]
'''

## Arguments

| Argument | Description |

| `--iterations N` | The number of iterations to run the simulation for. Defaults to 100. |
| `--components C1 C2` | The components to use in the simulation. Needs to only be 2. |
| `--chance X Y` | The chance of a component being placed on the conveyor belt. Defaults to 1/3. |
| `--stations N` | The number of stations on the conveyor belt. Defaults to 3. |
| `--workers N` | The number of workers at each station. Defaults to 2. |
| `--time N` | The number of steps to assemble components to make a finished product. Defaults to 4. |
| `--debug` | Enables debug mode. |