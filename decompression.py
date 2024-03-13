import sys

class Node:
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol
        self.left = left
        self.right = right



def chars_to_binary(encoded_string):
    # Extract the initial padding length
    padding_length = int(encoded_string[0])
    encoded_string = encoded_string[1:]  # Remove padding length indicator

    binary_sequence = ""
    i = 0
    while i < len(encoded_string):
        char = encoded_string[i]
        if char == chr(1):  # Check for escape character
            i += 1  # Move to the escaped character
            escaped_char = encoded_string[i]
            if escaped_char == chr(1):  # Escaped escape character
                binary_sequence += format(ord(escaped_char), '08b')
            elif ord(escaped_char) == 126:  # Special case for DEL
                binary_sequence += format(127, '08b')
            else:  # Control characters
                binary_sequence += format(ord(escaped_char) - 32, '08b')
        else:
            binary_sequence += format(ord(char), '08b')
        i += 1

    # Remove padding added during encoding
    if padding_length > 0:
        binary_sequence = binary_sequence[:-padding_length]

    return binary_sequence


def bits_to_sequence(binary_sequence):
    traversal_sequence = []
    for i in range(0, len(binary_sequence), 8):
        byte = binary_sequence[i:i+8]
        value = int(byte, 2)  # Convert from binary to integer

        if value > 127:  # It was encoded as a number + 127
            number = value - 127
            traversal_sequence.append(str(number))
        else:  # It's an ASCII character
            traversal_sequence.append(chr(value))

    return traversal_sequence



def buildTree(inOrder, preOrder, inStrt, inEnd):
    """Recursive function to construct binary of size len from
    Inorder traversal in[] and Preorder traversal pre[].  
    Initial values of inStrt and inEnd should be 0 and len -1. 
    The function doesn't do any error checking for cases
    where inorder and preorder do not form a tree """   
  
    if (inStrt > inEnd):
        return None
 
    # Pick current node from Preorder traversal using
    # preIndex and increment preIndex
    tNode = Node(preOrder[buildTree.preIndex])
    buildTree.preIndex += 1
 
    # If this node has no children then return
    if inStrt == inEnd :
        return tNode
 
    # Else find the index of this node in Inorder traversal
    inIndex = search(inOrder, inStrt, inEnd, tNode.symbol)
     
    # Using index in Inorder Traversal, construct left 
    # and right subtrees
    tNode.left = buildTree(inOrder, preOrder, inStrt, inIndex-1)
    tNode.right = buildTree(inOrder, preOrder, inIndex + 1, inEnd)
 
    return tNode
 
 
def search(arr, start, end, value):
    # UTILITY FUNCTIONS
    # Function to find index of value in arr[start...end]
    # The function assumes that value is present in inOrder[]
    for i in range(start, end + 1):
        if arr[i] == value:
            return i

def decode_huffman_tree(root, encoded_data):
    decoded_output = ""
    current = root
    for bit in encoded_data:
        if bit == '0':
            current = current.left
        else:
            current = current.right

        if current.left is None and current.right is None:  # Leaf node
            decoded_output += current.symbol
            current = root

    return decoded_output

def decompress(encoded_file_name):

    #  Reading the encoded text to decode it
    try:
        with open(encoded_file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            encoded_data = lines[0].strip()
            inorder_encoded = lines[1].strip()
            preorder_encoded = lines[2].strip()

        # Convert Base64 encoded inorder and preorder sequences to binary
        inorder_binary = chars_to_binary(inorder_encoded)
        preorder_binary = chars_to_binary(preorder_encoded)
        decoded_data = chars_to_binary(encoded_data)

        # Convert binary sequences back to characters/IDs
        inorder_sequence = bits_to_sequence(inorder_binary)
        preorder_sequence = bits_to_sequence(preorder_binary)


        # Reconstruct Huffman Tree
        buildTree.preIndex = 0
        tree_root = buildTree(inorder_sequence, preorder_sequence, 0, len(inorder_sequence)-1)

        # Decode the encoded data
        original_text = decode_huffman_tree(tree_root, decoded_data)


    except FileNotFoundError:
        print(f"File {encoded_file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


    #  Writing the decoded text to an output file
    decoded_file_name = "decompressed.txt"
    try:
        with open(decoded_file_name, 'w') as file:
            write_data = f"{original_text}"
            file.write(write_data)
            print("Decompressed data to file:", decoded_file_name)

    except FileNotFoundError:
        print(f"File {decoded_file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



def main(input_file_name):
    decompress(input_file_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Run the program using this command: 'python decompression.py compressed.txt'")
    else:
        main(sys.argv[1])
    #main("compressed.txt")
    
