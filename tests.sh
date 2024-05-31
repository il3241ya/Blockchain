#!/bin/bash
set -e

HASH_TESTS_DIR="src/hashing/tests"
TREE_HASH_DIR="src/merkle_tree/tests"


echo "Running hash tests..."
echo "---------------------"
python $HASH_TESTS_DIR/hash_test.py
echo "---------------------"


echo "Running tree tests..."
echo "---------------------"
python $TREE_HASH_DIR/tree_test.py
echo "---------------------"
