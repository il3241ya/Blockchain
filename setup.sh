#/bin/sh

python3 -m venv ./venv
source venv/bin/activate

pip3 install -r requirements.txt

protoc --python_out=src/blocks/protobuf_gen src/blocks/network_structure.proto
