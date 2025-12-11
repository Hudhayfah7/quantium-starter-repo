#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run test suite
pytest -v
TEST_RESULT=$?

# If tests passed, exit 0; else exit 1
if [ $TEST_RESULT -eq 0 ]; then
    echo "All tests passed! 🎉"
    exit 0
else
    echo "Some tests failed. ❌"
    exit 1
fi