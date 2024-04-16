import heapq
from collections import Counter, defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Build the Huffman tree
def build_huffman_tree(text):
    frequency = Counter(text) # Frequency of each character in the text
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]# Priority queue from the frequency table
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)# Combine the two nodes with the lowest frequency
        right = heapq.heappop(priority_queue)

        merged = Node(None, left.freq + right.freq)  # Create a new node with these two nodes as children and the combined frequency
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    return priority_queue[0]  # Return the root node of the Huffman tree


# Assign Huffman codes to each character
def assign_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        assign_codes(node.left, prefix + "0", codebook)
        assign_codes(node.right, prefix + "1", codebook)
    return codebook


# Encode the text using the Huffman codes
def huffman_encoding(text):
    root = build_huffman_tree(text)
    codebook = assign_codes(root)
    encoded_text = ''.join(codebook[char] for char in text)
    return encoded_text, codebook


# Decode the encoded text using the Huffman codes
def huffman_decoding(encoded_text, codebook):
    reverse_codebook = {code: char for char, code in codebook.items()}
    current_code = ""
    decoded_text = ""
    
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_text += reverse_codebook[current_code]
            current_code = ""

    return decoded_text


if __name__ == "__main__":
    # input_text = "The quick brown fox jumps over the lazy dog"
    input_text = input("Enter the text to be encoded: ")
    encoded_text, codebook = huffman_encoding(input_text)
    print("Encoded text:", encoded_text)
    print("Huffman Codes:", codebook)
    decoded_text = huffman_decoding(encoded_text, codebook)
    print("Decoded text:", decoded_text)
