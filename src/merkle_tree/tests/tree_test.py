import unittest
from src.hashing.hash import HashingFactory 
from src.merkle_tree.merkle_tree import MerkleNode, MerkleTree


class TestMerkleTree(unittest.TestCase):
    def setUp(self):
        self.hash_function = HashingFactory()

    def test_node(self):
        node = MerkleNode(hash_value=self.hash_function.hash("lol kek"))
        self.assertEqual(node.hash_value, self.hash_function.hash('lol kek').hex())
    
    def test_single_transaction(self):
        transactions = ["tx1"]
        tree = MerkleTree(transactions, self.hash_function)
        root = tree.get_root()
        self.assertEqual(root.hash_value, self.hash_function.hash(self.hash_function.hash("tx1").hex() + self.hash_function.hash("tx1").hex()).hex())

    def test_even_number_of_transactions(self):
        transactions = ["tx1", "tx2", "tx3", "tx4"]
        tree = MerkleTree(transactions, self.hash_function)
        root = tree.get_root()
        expected_root_hash = self.hash_function.hash(
            self.hash_function.hash(self.hash_function.hash("tx1").hex() + self.hash_function.hash("tx2").hex()).hex() +
            self.hash_function.hash(self.hash_function.hash("tx3").hex() + self.hash_function.hash("tx4").hex()).hex()
        ).hex()
        self.assertEqual(root.hash_value, expected_root_hash)

    def test_odd_number_of_transactions(self):
        transactions = ["tx1", "tx2", "tx3"]
        tree = MerkleTree(transactions, self.hash_function)
        root = tree.get_root()
        expected_root_hash = self.hash_function.hash(
            self.hash_function.hash(self.hash_function.hash("tx1").hex().encode('utf-8') + self.hash_function.hash("tx2").hex().encode('utf-8')).hex() +
            self.hash_function.hash(self.hash_function.hash("tx3").hex().encode('utf-8') + self.hash_function.hash("tx3").hex().encode('utf-8')).hex()
        ).hex()
        self.assertEqual(root.hash_value, expected_root_hash)

    def test_merkle_tree_structure(self):
        transactions = ["tx1", "tx2", "tx3", "tx4"]
        tree = MerkleTree(transactions, self.hash_function)
        levels = tree.tree_structure
        self.assertEqual(len(levels), 3)  
        self.assertEqual(len(levels[0]), 4)  
        self.assertEqual(len(levels[1]), 2)  
        self.assertEqual(len(levels[2]), 1) 

if __name__ == "__main__":
    unittest.main()