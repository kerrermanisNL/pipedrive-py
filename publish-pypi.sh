#! /bin/bash
python setup.py sdist && python setup.py bdist_wheel 
python setup.py sdist upload -r prod && python setup.py bdist_wheel upload -r prod
