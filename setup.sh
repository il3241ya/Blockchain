#/bin/sh

python3 -m venv ./venv
source venv/bin/activate

PYTHONPATH=$PYTHONPATH:$PWD/src/
