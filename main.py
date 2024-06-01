from src.hashing.hash import HashingFactory
from src.merkle_tree.merkle_tree import MerkleNode, MerkleTree
import blocks.protobuf_gen.network_structure_pb2 as NNetwork
import time


def create_transactions_4_226(transactions_name):
    for transaction_name in transactions_name:
        with open(f'transactions/{transaction_name}', 'wb') as f:
            f.write(b'\1' * 226)


def read_transactions(transactions_name):
    trx = []
    for transaction in transactions_name:
        with open(f'transactions/{transaction}', 'rb') as f:
            trx.append(f.read())
    return trx


def calculate_block_hash(block_header, hash_function):
    block_header_bytes = block_header.SerializeToString()
    return hash_function.hash(block_header_bytes).hex()


def mine_block(block, hash_function):
    nonce = 0
    while True:
        block.BlockHeader.Nonce = nonce
        block_header_hash = calculate_block_hash(block.BlockHeader, hash_function)
        if block_header_hash.startswith("0000"):
            return nonce, block_header_hash
        nonce += 1


if __name__ == "__main__":

    transactions = [
        'tx1.txt',
        'tx2.txt',
        'tx3.txt',
        'tx4.txt'
    ]

    create_transactions_4_226(transactions)

    sha256 = HashingFactory()
    merkle_tree = MerkleTree(
        transactions=read_transactions(transactions), 
        hash_function=sha256
    )

    with open('blocks/network/prevblock_header.hash', 'rb') as f:
        prev_hash = f.read()


    block = NNetwork.TBlock()
    block.BlockHeader.PrevBlockHeaderHash = prev_hash
    block.BlockHeader.Timestamp = time.time()

    for txn in read_transactions(transactions): 
        block.BlockData.Transaction.append(txn)

    block.BlockHeader.MerkleTreeHash = bytes.fromhex(merkle_tree.get_root().hash_value)

    block.BlockHeader.BlockSize = len(block.SerializeToString())
    block.BlockHeader.Nonce = 0


    # Подберем необходимое значение nonce
    nonce, block_header_hash = mine_block(block, sha256)
    block.BlockHeader.Nonce = nonce

    print(f"Block mined with nonce: {nonce}")
    print(f"Block header hash: {block_header_hash}")

    serialized_block = block.SerializeToString()
    with open('blocks/network/mined_block.bin', 'wb') as f:
        f.write(serialized_block)
