#!/bin/bash
echo "------------Checking Root folder------------"
pep8 *.py
echo
echo "------------Checking into API folder------------"
pep8 api/*.py api/v1/*.py api/v1/views/*.py
echo
echo "------------Checking into MODELS folder------------"
pep8 models/*.py models/engine/*.py
echo
echo "------------Checking into TESTS folder------------"
pep8 tests/*.py tests/test_models/*.py tests/test_models/test_engine/*.py
echo
echo "------------Checking into WEB_FLASK folder------------"
pep8 web_flask/*.py
echo
