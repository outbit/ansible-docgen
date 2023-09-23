#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:./lib"
coverage run --source=ansibledocgen $(which python3) -m unittest discover test/units/
