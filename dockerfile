FROM python:3.11-alpine

ENV PYTHONPATH /Blockchain/src:$PYTHONPATH

WORKDIR /Blockchain

COPY requirements.txt ./
COPY blocks/*.proto ./blocks/

RUN apk update && \
    apk add --no-cache protobuf && \
    pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p /Blockchain/blocks/protobuf_gen && \
    protoc --proto_path=/Blockchain/blocks --python_out=/Blockchain/blocks/protobuf_gen /Blockchain/blocks/network_structure.proto

CMD ["sh"]