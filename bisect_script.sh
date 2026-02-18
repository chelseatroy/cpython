#!/bin/bash

  # Rebuild the project; skip commit if build fails
  make -j4 || exit 125

  # Run the regression test
  ./python -m pytest test_my_bug.py

  if [ $? -eq 0 ]; then
      exit 0    # test passed — good commit
  else
      exit 1    # test failed — bad commit
  fi