#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:./lib"
coverage run --source=ansibledocgen $(which nosetests) -w test/units/
