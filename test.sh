
pushd testing

  pushd "tests"
    python ./tester.py run-tests ./data/segment-intersection-data/tests/*
  popd

  pushd "loctests"
    python ./tester.py run-tests ./data/segment-intersection-data/tests_location/*
  popd

  pushd "collecter"
    python ./tester.py collect ./out results.csv
  popd

popd # /testing