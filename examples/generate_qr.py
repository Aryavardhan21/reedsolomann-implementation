import sys
import random
sys.path.append('..')  # Add parent directory to Python path

from src.qr_generator import generate_qr
from src.reed_solomon import ReedSolomon

def string_to_ints(s):
    return [ord(c) for c in s]

def ints_to_string(ints):
    return ''.join(chr(i) for i in ints)

def main():
    data = input("Enter the data to encode in QR code: ")
    
    # Convert string to integers for Reed-Solomon encoding
    data_ints = string_to_ints(data)
    
    # Pad data to fit Reed-Solomon block size
    rs_n, rs_k = 255, 223  # RS(255,223) can correct up to 16 errors
    padded_data = data_ints + [0] * (rs_k - len(data_ints) % rs_k)
    
    # Initialize Reed-Solomon encoder
    rs = ReedSolomon(rs_n, rs_k)
    
    # Encode data with Reed-Solomon
    encoded_blocks = []
    for i in range(0, len(padded_data), rs_k):
        block = padded_data[i:i+rs_k]
        encoded_block = rs.encode(block)
        encoded_blocks.extend(encoded_block)
    
    # Convert encoded data back to string
    encoded_data = ints_to_string(encoded_blocks)
    
    # Generate QR code
    qr_image = generate_qr(encoded_data, error_correction=3)  # Using highest error correction level

    output_file = "generated_qr_with_rs.png"
    qr_image.save(output_file)
    print(f"QR code with Reed-Solomon encoding generated and saved as {output_file}")

if __name__ == "__main__":
    main()
