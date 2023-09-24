#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:./lib"
coverage run --source=ansibledocgen -m unittest discover test/units/
