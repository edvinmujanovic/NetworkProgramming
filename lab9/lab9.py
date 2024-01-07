import math
import random
import zlib

# Load text data from the file
file_path = "lab9/exempeltextMac.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()
    print("Length of data:", len(data))

# Convert the text data to a byte array with UTF-8 encoding
byteArr = bytearray(data, 'UTF-8')
print("Length of byteArr:", len(byteArr))


def calculate_histogram(bytearray):
    histogram = [0] * 256
    for char in bytearray:
        histogram[char] += 1
    return histogram


def calculate_probability(histogram):
    total_occurrences = sum(histogram)
    probability_histogram = [0] * len(histogram)
    for index in range(len(histogram)):
        probability_histogram[index] = round(histogram[index] / total_occurrences, 4)
    return probability_histogram

def test_zip_compression():
    t1 = """I hope this lab never ends because
            it is so incredibly thrilling!"""

    t10 = 10 * t1
    print("Length of t1:", len(t1))
    zipped_t1 = zlib.compress(bytearray(t1, 'UTF-8'))
    print("Length of zipped t1:", len(zipped_t1))
    print("Length of t10:", len(t10))
    zipped_t10 = zlib.compress(bytearray(t10, 'UTF-8'))
    print("Length of t10 zipped:", len(zipped_t10))


def calculate_entropy(probability_histogram):
    entropy = 0
    for i in range(len(probability_histogram)):
        if probability_histogram[i] != 0:
            entropy += probability_histogram[i] * math.log2(1 / probability_histogram[i])
    return entropy


def zip_compress_and_analyze(data):
    the_copy = bytearray(data, 'UTF-8')
    random.shuffle(the_copy)

    # Compress the shuffled data using zlib
    compressed_copy = zlib.compress(the_copy)
    compressed_entropy = calculate_entropy(calculate_probability(calculate_histogram(compressed_copy)))
    bits_per_symbol_shuffled = len(compressed_copy) * 8 / len(the_copy)
    print("Bits per symbol (Shuffled): {:.15f}".format(bits_per_symbol_shuffled))

    # Compress the original data using zlib
    compressed_original_bytearr = zlib.compress(byteArr)
    original_bytearr_entropy = calculate_entropy(calculate_probability(calculate_histogram(byteArr)))
    bits_per_symbol_original = len(compressed_original_bytearr) * 8 / len(byteArr)
    print("Entropy of compressed original bytearr: {:.15f} bits/symbol".format(original_bytearr_entropy))
    print("Bits per symbol (Original): {:.15f}".format(bits_per_symbol_original))


print("Checking Histogram")
print()

# Calculate histogram
histogram = calculate_histogram(byteArr)
print("Histogram:")
print(histogram)

# Calculate probability histogram
probability_histogram = calculate_probability(histogram)
print("Probability Histogram:")
print(probability_histogram)

# Calculate and print entropy
entropy = calculate_entropy(probability_histogram)
print()



zip_compress_and_analyze(data)

test_zip_compression()