from typing import Tuple


def sort_freq_dict(freq_dict: dict) -> dict:
    return dict(sorted(freq_dict.items(), key=lambda x:x[1]))


# Makes a dictionary with the symbol as the key and its
# frequency as the value
def make_frequency_dict(data: str) -> dict:
    freq_dict = {}
    for i in range(len(data)):
        if data[i] in freq_dict.keys():
            freq_dict[data[i]] += 1
        else:
            freq_dict[data[i]] = 1
    return sort_freq_dict(freq_dict)


# Creates binary tree with higher frequency data
# higher up in the tree and thus accessible using
# fewer bits
def create_binary_tree(data: str) -> dict:
    freq_dict: dict = make_frequency_dict(data)
    tree_dict: dict = freq_dict.copy()
    for _ in range(len(freq_dict.keys()) - 1):
        small_0: str = list(freq_dict.keys())[0]
        small_1: str = list(freq_dict.keys())[1]
        freq_dict[small_0 + small_1] = freq_dict[small_0] + freq_dict[small_1]
        tree_dict[small_0 + small_1] = {small_0: tree_dict[small_0], small_1: tree_dict[small_1]}
        del freq_dict[small_0], tree_dict[small_0]
        del freq_dict[small_1], tree_dict[small_1]
        freq_dict = sort_freq_dict(freq_dict)
    return tree_dict


# This is seperate from 'create_huffman_dict' to simplify
# the recursion
def get_first_branches(tree) -> Tuple[dict, dict]:
    trunk = list(tree.values())[0]
    branch_0 = list(trunk.values())[0]
    branch_1 = list(trunk.values())[1]
    return branch_0, branch_1
    

# Recursively transverses the binary tree recording the path it took to get there.
# Left is represented by a 0 and right by a 1. This path then becomes the bit
# representation of the symbol.
def create_huffman_dict(branches: dict, huffman_key) -> dict:
    deeper_branches = {}
    for bits, branch in branches.items():
        if type(branch) == dict:
            counter = "0"
            for key, val in branch.items():
                if type(val) == dict:
                    deeper_branches[bits + counter] = val
                elif type(val) == int:
                    huffman_key[key] = bits + counter
                counter = "1"
        else:
            huffman_key[branch] = bits
    
    if len(deeper_branches) != 0:
        return create_huffman_dict(deeper_branches, huffman_key)
    else:
        return huffman_key
    

# Goes through the data respresenting each symbol with its bitwise
# representation in the dict
def compress(data: str, huffman_dict: dict) -> str:
    compressed_bits: str = ""
    for char_i in range(len(data)):
        compressed_bits += huffman_dict[data[char_i]]
    return compressed_bits


# Goes through compressed data and converts back into original symbols
def decompress(compressed_data: str, huffman_dict: dict) -> str:
    reverse_dict: dict = {bits: char for char, bits in huffman_dict.items()}
    shortest_bit_length: int = len(sorted(list(reverse_dict.keys()))[0]) - 1
    data = ""
    i: int = shortest_bit_length
    j: int = 0
    while i <= len(compressed_data):
        if compressed_data[j:i] in reverse_dict.keys():
            data += reverse_dict[compressed_data[j:i]]
            j = i
            i += shortest_bit_length
        else:
            i += 1
    return data


# Gets the unicode representation of each char in the data to be compressed
def get_unicode(data: str) -> str:
    unicode_data: str = ""
    for i in range(len(data)):
        unicode_data += bin(ord(data[i]))[2:]
    return unicode_data


# Turns unicode data into unicode chars
def turn_into_unicode(compressed_data):
    unicode_data: str = ""
    j = 0
    i = 7
    while i <= len(compressed_data):
        unicode_data += chr(int(compressed_data[j: i], 2))
        j = i
        i += 7
    return unicode_data


def read_file(path: str) -> str:
    f = open(path, "r")
    file_str: str = f.read()
    f.close()
    return file_str


def write_file(path: str, data: str) -> None:
    f = open(path, "w")
    f.write(data)
    f.close
    

# Performs full compression
def write_compressed_file(compressed_unicode_data: str, write_path: str) -> None:
    write_file(write_path, compressed_unicode_data)


def write_decompressed_file(compressed_data: str, huffman_dict: dict, path: str) -> None:
    decompressed_data: str = decompress(compressed_data, huffman_dict)
    write_file(path, decompressed_data)


def main():
    # read_path: path of file you want to compress
    read_path: str = ""
    # Likewise, compressed_path and decompressed_path are paths of files
    # where you want your compressed and decompressed data written
    compressed_path: str = ""
    decompressed_path: str = ""
    data: str = read_file(read_path)

    # Trains a Huffman table on read_file's data
    tree: dict = create_binary_tree(data)
    val_0, val_1 = get_first_branches(tree)
    huffman_dict: dict = create_huffman_dict({"0": val_0, "1": val_1}, {})
    
    # Compresses read_file 
    compressed_data: str = compress(data, huffman_dict)

    # Turns compressed data (a str of 1's and 0's) into unicode characters
    # so that we can write it to file and properly compare compressed
    # file size with original
    compressed_unicode_data: str = turn_into_unicode(compressed_data)
    decompressed_data: str = decompress(compressed_data, huffman_dict)

    # Writes to chosen paths
    write_file(compressed_path, compressed_unicode_data)
    write_file(decompressed_path, decompressed_data)

if __name__ == "__main__":
    main()
