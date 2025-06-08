#!/bin/bash

set -e
set -x

path="${1:-source}"

isort $path
black $path