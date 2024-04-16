from PIL import Image
import heapq
from collections import Counter, defaultdict

class Node:
    def __init__(self, pixel, freq):
        self.pixel = pixel
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequency):
    priority_queue = [Node(pixel, freq) for pixel, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def assign_codes(node, prefix="", codebook={}):
    if node.pixel is not None:
        codebook[node.pixel] = prefix
    if node.left:
        assign_codes(node.left, prefix + '0', codebook)
    if node.right:
        assign_codes(node.right, prefix + '1', codebook)
    return codebook

def encode_image(image, codebook):
    width, height = image.size
    encoded_output = ''
    pixels = list(image.getdata())
    for pixel in pixels:
        encoded_output += codebook[pixel]
    return encoded_output, width, height

def decode_image(encoded_data, codebook, dimensions):
    reverse_codebook = {v: k for k, v in codebook.items()}
    pixels = []
    current_code = ''
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codebook:
            pixels.append(reverse_codebook[current_code])
            current_code = ''
    return pixels, dimensions

def main():
    image_path = 'tiger-jpg.jpg'
    img = Image.open(image_path).convert('L') # Convert to grayscale
    frequency = Counter(img.getdata())
    root = build_huffman_tree(frequency)
    codebook = assign_codes(root)
    
    encoded_data, width, height = encode_image(img, codebook)
    pixels, dimensions = decode_image(encoded_data, codebook, (width, height))
    
    # Create a new image from the decoded data
    new_img = Image.new('L', dimensions)
    new_img.putdata(pixels)
    new_img.show()

if __name__ == "__main__":
    main()
