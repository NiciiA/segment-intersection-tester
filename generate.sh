#!/bin/bash

pushd generation

  pushd "generator"
    python ./generation/generator.py # standard test generator
  popd

  pushd "locations"
    python ./generation/generate_locations.py # location test generator
  popd

popd # /generation
