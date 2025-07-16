#!/bin/bash

source .venv/bin/activate

pushd generation

  python ./generator.py # standard test generator
  python ./generate_locations.py # location test generator

  pushd leda
    ./gen_leda.sh
  popd

popd # /generation
