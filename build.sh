#!/bin/bash

set -x
set -a

LEDA_VERSION=7.2

git submodule update --init --recursive

python3 -m venv .venv
source .venv/bin/activate
pip install -r generation/requirements.txt
echo "Don't forget to run \`source .venv/bin/activate!\`"

pushd adapters

  curl https://leda.uni-trier.de/leda/download.cgi?LEDA-${LEDA_VERSION}.tgz -o leda.tgz
  tar -xaf leda.tgz
  rm leda.tgz
  mv LEDA-${LEDA_VERSION} deps/leda

  export LEDA_HOME="$(realpath deps/leda)"
  export PATH="${PATH}:${LEDA_HOME}/bin"
  export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${LEDA_HOME}/lib"

  echo "LEDA environment (also stored in venv):"
  echo "export LEDA_HOME=\"$LEDA_HOME\"" | tee -a .venv/bin/activate
  echo 'export PATH="${PATH}:${LEDA_HOME}/bin"' | tee -a .venv/bin/activate
  echo 'export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${LEDA_HOME}/lib"' | tee -a .venv/bin/activate

  pushd deps/leda
    ./lconfig g++ static # https://stackoverflow.com/a/11173897
    ./build.sh # may need to change shebang to bash
  popd

  mkdir -p "deps/ogdf/build-release"
  pushd "deps/ogdf/build-release"
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=TRUE -DCMAKE_POLICY_DEFAULT_CMP0069=NEW -DBUILD_SHARED_LIBS=OFF \
      -DOGDF_MEMORY_MANAGER=POOL_NTS -DOGDF_USE_ASSERT_EXCEPTIONS=OFF
    cmake --build . --target OGDF -j $(nproc)
  popd

  mkdir -p "cpp/build-release"
  pushd "cpp/build-release"
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=TRUE -DCMAKE_POLICY_DEFAULT_CMP0069=NEW -DBUILD_SHARED_LIBS=OFF \
      -DOGDF_DIR=$(realpath "../../deps/ogdf/build-release") -DMPFR_LIBRARIES=/usr/lib64/libmpfr.so
    cmake --build . --target all -j $(nproc)
  popd

popd # /adapters
