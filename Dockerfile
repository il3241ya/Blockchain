FROM python:3.11-alpine AS builder

WORKDIR /Blockchain

COPY requirements.txt .
COPY blocks/*.proto ./blocks/
COPY main.py .

RUN apk update && \
    apk add --no-cache protobuf && \
    pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p /Blockchain/blocks/protobuf_gen && \
    protoc --proto_path=/Blockchain/blocks --python_out=/Blockchain/blocks/protobuf_gen /Blockchain/blocks/network_structure.proto

FROM python:3.11-alpine

ENV PYTHONPATH {$PYTHONPATH}:/Blockchain/src

WORKDIR /Blockchain
COPY --from=builder /Blockchain/requirements.txt .
COPY --from=builder /Blockchain/blocks/protobuf_gen /Blockchain/blocks/protobuf_gen
COPY --from=builder /Blockchain/main.py .

RUN apk update && \
    apk add --no-cache protobuf && \
    pip3 install --no-cache-dir -r requirements.txt

RUN rm requirements.txt ./blocks/network_structure.proto
CMD ["sh"]
