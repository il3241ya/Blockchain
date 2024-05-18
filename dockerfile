FROM python:3.11-alpine

WORKDIR /Blockchain
COPY requirements.txt .

ENV PYTHONPATH /Blockchain/src:$PYTHONPATH
RUN apk update && apk add --no-cache \
        protobuf

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN protoc --python_out=/Blockchain/src/blocks/protobuf_gen /Blockchain/src/blocks/network_structure.proto

CMD ["python3"]
