#!/bin/bash

source .venv/bin/activate

pushd generation

  python ./generator.py # standard test generator
  python ./generate_locations.py # location test generator

popd # /generation
