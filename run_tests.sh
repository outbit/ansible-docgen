#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:./lib"
coverage run --source=ansibledocgen $(which pytest) -w test/units/
