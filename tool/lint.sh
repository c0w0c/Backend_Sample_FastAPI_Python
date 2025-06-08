#!/bin/bash

set -e
set -x

isort .
black .
pylint source/.
