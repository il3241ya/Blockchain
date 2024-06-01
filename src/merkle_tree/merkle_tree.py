from src.hashing.hash import HashingFactory


class MerkleNode:
    def __init__(self, hash_value, left_node=None, right_node=None):
        self.left_node = left_node
        self.right_node = right_node
        self.hash_value = hash_value.hex()

    def __str__(self):
        return self.hash_value

    
class MerkleTree:
    def __init__(self, transactions, hash_function):
        self.transactions = transactions
        self.hash_function = hash_function
        self._build_tree()

    def _build_tree(self):
        if len(self.transactions) % 2 != 0:
            self.transactions.append(self.transactions[-1])

        tree_depth = len(self.transactions) // 2

        nodes = [MerkleNode(hash_value=self.hash_function.hash(transaction)) for transaction in self.transactions]

        self.tree_structure = []
        self.tree_structure.append(nodes)

        for _ in range(tree_depth):
            self.tree_structure.append(
                [
                    MerkleNode(
                        self.hash_function.hash(self.tree_structure[-1][j].hash_value + self.tree_structure[-1][j + 1].hash_value),
                        left_node=self.tree_structure[-1][j],
                        right_node=self.tree_structure[-1][j + 1]
                    )
                    for j in range(0, len(self.tree_structure[-1]) - 1, 2)
                ]
            )

    def get_root(self):
        return self.tree_structure[-1][0]
