from finalavltree import AVLTree
from finalredblacktree import RedBlackTree
import time
import os
#import pandas as pd
import csv



def read_int_from_file(filename):
    numbers = []
    file_path = os.path.join(directory, filename)  # Join the directory and filename

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line_numbers = line.strip().split()
                for num_str in line_numbers:
                    try:
                        num = int(num_str)
                        numbers.append(num)
                    except ValueError:
                        print(f"Skipping non-integer value: {num_str}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return 0

    print(f"Step 1 Complete for {filename}")
    return numbers


def test_tree_operations(tree_type:str, data):
    if tree_type == "RedBlackTree":
        tree= RedBlackTree
        print("Red-Black tree recognized")
    if tree_type== "AVLTree":
        tree = AVLTree
        print("AVL tree recognized")
    start_time = time.time()
    
    print(f"Insertion Timer Started for {tree_type}")
    for item in data:
        tree.insert(item)
        print(f"Inserting {item}")
    insertion_time = time.time() - start_time
    print(f"Insertion Test Complete for {tree_type}")
   
    start_time = time.time()
    print(f"Search Timer Started for {tree_type}")
    for item in data:
        tree.search(item)
        print(f"Searching For {item}")
    search_time = time.time() - start_time
    print(f"Search Test Complete for {tree_type}")
    
    start_time = time.time()
    print(f"Delete Timer Started for {tree_type}")
    for item in data:
        tree.delete(item)
        print(f"Deleting {item}")
    deletion_time = time.time() - start_time
    print(f"Delete Test Complete for {tree_type}")

    return insertion_time, search_time, deletion_time

# results = []

# for filename in files:
#     start_time = time.time() 
#     numbers = read_int_from_file(filename)
#     count = tree.insert(numbers)
#     end_time = time.time()
#     time_taken = end_time - start_time
#     results.append((len(numbers), time_taken))
#     print(f"Processed {filename}: {count} inserted into Red-Black Tree in {time_taken:.4f} seconds.")

# print(results)
if __name__ == "__main__":

    files = [
    '10_ordered_numbers.txt', '10_random_numbers.txt'#'5000_ordered_numbers.txt', '5000_random_numbers.txt',
    # '10000_ordered_numbers.txt', '10000_random_numbers.txt'
    ]

    directory = 'testingdata'

    for file in files:
        data = read_int_from_file(file)  

        if data: 
            red_black_tree_times = test_tree_operations("RedBlackTree", data)
            avl_tree_times = test_tree_operations("AVLTree", data)

            print(f"\nResults for {file}:")
            print(f"Red-Black Tree: Insertion: {red_black_tree_times[0]}s, Search: {red_black_tree_times[1]}s, Deletion: {red_black_tree_times[2]}s")
            print(f"AVL Tree: Insertion: {avl_tree_times[0]}s, Search: {avl_tree_times[1]}s, Deletion: {avl_tree_times[2]}s")
        else:
            print(f"Skipping {file} due to missing or invalid data.")