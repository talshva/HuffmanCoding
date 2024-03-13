import sys
coded_letters_dict = dict()
id_counter = 0

class Nodes:
    def __init__(self, frequency, symbol, left=None, right=None, num_id=''):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right
        self.id = num_id
        self.code = ''

    def _str_helper(self, level=0, prefix=""):
        # Prefix the node representation with the given prefix (which could be empty, '0', or '1')
        ret = "|\t"*level + prefix + "(" +repr(f"id={self.id} : letters={self.symbol} : freq={self.frequency}") + ")" + "\n"
        # For the left child, add '0' prefix; for the right child, add '1' prefix
        if self.left:
            ret += self.left._str_helper(level+1, "0 - ")
        if self.right:
            ret += self.right._str_helper(level+1, "1 - ")
        return ret

    def __str__(self):
        # Start the tree representation without any prefix
        return self._str_helper()

    def __repr__(self):
        return '<HuffmanNode>'


def CalculateFrequency(text_file_data):
    the_symbols = dict()
    for item in text_file_data:
        if the_symbols.get(item) == None:
            the_symbols[item] = 1
        else:
            the_symbols[item] += 1
    return the_symbols


def CalculateLetterCodes(node, value=''):
    newValue = value + str(node.code)
    if(node.left):
        CalculateLetterCodes(node.left, newValue)
    if(node.right):
        CalculateLetterCodes(node.right, newValue)
    if(not node.left and not node.right):
        coded_letters_dict[node.symbol] = newValue


def EncodeTextFile(text_file_data, coding):
    encodingOutput = [coding[element] for element in text_file_data]
    the_string = ''.join(encodingOutput)

    print(f"Number of chars before huffman coding (size of input file): {len(text_file_data)}")
    print(f"Number of chars after huffman coding (before writing to file): {int(len(the_string)/8)}")

    return binary_to_chars(the_string)


def binary_to_chars(binary_sequence):
    padding_length = (8 - len(binary_sequence) % 8) % 8
    binary_sequence += '0' * padding_length
    escape_character = chr(1)  # Using '\x01' as an escape character

    # First element indicates the padding amount
    encoded_string = str(padding_length)

    for i in range(0, len(binary_sequence), 8):
        byte = binary_sequence[i:i+8]
        char_code = int(byte, 2)
        if char_code < 32:  # Check if it's a control character
            # Encode as an escaped character
            encoded_string += escape_character + chr(char_code + 32)
        elif char_code == 127:  # DEL
            encoded_string += escape_character + chr(126)
        elif char_code == ord(escape_character):  # Escape character itself
            encoded_string += escape_character + escape_character
        else:
            # Directly convert to character
            encoded_string += chr(char_code)

    return encoded_string


def sequence_to_bits(traversal_sequence):
    bits_string = ""
    for element in traversal_sequence:
        if len(element) == 1:  # Single character
            # Convert character to 8-bit binary
            bits_string += format(ord(element), '08b')
        else:  # Element length > 1, assumed to be a number in string format
            # Convert string number to int, add 127, and convert to 8-bit binary
            number = int(element) + 127
            bits_string += format(number, '08b')

    return bits_string



def Set_IDs(node):
    global id_counter
    if node:
        if len(node.symbol) != 1:
            node.id = str(id_counter)
            id_counter += 1
        Set_IDs(node.left)
        Set_IDs(node.right)


def inorderTraversal(node, result=[]):
    if node:
        inorderTraversal(node.left, result)
        if len(node.symbol) == 1:
            result.append(node.symbol)
        else:
            result.append(node.id)
        inorderTraversal(node.right, result)
    return result


def preorderTraversal(node, result=[]):
    if node:
        if len(node.symbol) == 1:
            result.append(node.symbol)
        else:
            result.append(node.id)
        preorderTraversal(node.left, result)
        preorderTraversal(node.right, result)
    return result


def get_max_depth(node):
    if node is None:
        return 0
    left_depth = get_max_depth(node.left)
    right_depth = get_max_depth(node.right)
    return max(left_depth, right_depth) + 1


def HuffmanEncoding(text_file_data):
    symbolWithFreqs = CalculateFrequency(text_file_data)
    # Sort the dictionary by its values in descending order for printing
    sorted_symbolWithFreqs = dict(sorted(symbolWithFreqs.items(), key=lambda item: item[1], reverse=True))
    print(f"Freq Dictionary: \n {sorted_symbolWithFreqs}\n")
    
    nodes = []
    for symbol in symbolWithFreqs:
        nodes.append(Nodes(symbolWithFreqs[symbol], symbol))
    #it = 0
    while len(nodes) > 1:
        #it += 1
        nodes = sorted(nodes, key=lambda x: x.frequency)
        #print(f"iteration: {it}")
        #for node in nodes:
        #    print(node.frequency, node.symbol)
        left = nodes[0]
        right = nodes[1]
        left.code = 0
        right.code = 1
        newNode = Nodes(left.frequency + right.frequency, left.symbol + "," + right.symbol, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
        
    Set_IDs(nodes[0])
        # Print the Huffman Tree
    print("Huffman Tree:")
    print(nodes[0])
    
    CalculateLetterCodes(nodes[0])
    #print(f"Letter encodings: \n {coded_letters_dict}")
    encodedDataOutput = EncodeTextFile(text_file_data, coded_letters_dict)
    #print(f"\nData after converting to chars: \n {encodedDataOutput}")
    inorder = inorderTraversal(nodes[0], [])
    #print(f"\nInorder sequence for tree:  \n{inorder}")
    inorder_converted = binary_to_chars(sequence_to_bits(inorder))
    #print(f"\nConverted Inorder sequence for tree:  \n{inorder_converted}")
    preorder = preorderTraversal(nodes[0], [])
    #print(f"\nPreorder sequence for tree:  \n{preorder}")
    preorder_converted = binary_to_chars(sequence_to_bits(preorder))
    #print(f"\nConverted Preorder sequence for tree:  \n{preorder_converted}")
    return encodedDataOutput, ''.join(inorder_converted), ''.join(preorder_converted)


def main(input_file_name):
    try:
        with open(input_file_name, 'r') as file:
            text_file_data = file.read()

        encoded_data, inorder, preorder = HuffmanEncoding(text_file_data)

        encoded_file_name = "compressed.txt"
        with open(encoded_file_name, 'w', encoding='utf-8') as file:
            write_data = f"{encoded_data}\n{inorder}\n{preorder}"
            file.write(write_data)

        print(f"Number of chars after writing to file (using char encoding): {len(write_data)}")
        print(f"Saving ratio: {int(len(write_data)/len(text_file_data) * 100)} %")

    except FileNotFoundError:
        print(f"File {input_file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Run the program using this command: 'python compression.py <path_to_text_file>'")
        print("For example: python compression.py Alice_in_wonderlands.txt")
    else:
        main(sys.argv[1])
   #main("Alice_in_wonderlands.txt") 