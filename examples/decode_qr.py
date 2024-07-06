import sys
sys.path.append('..')  # Add parent directory to Python path

from src.qr_decoder import decode_qr
from src.reed_solomon import ReedSolomon

def string_to_ints(s):
    return [ord(c) for c in s]

def ints_to_string(ints):
    return ''.join(chr(i) for i in ints)

def main():
    image_path = input("Enter the path to the QR code image: ")
    results, error = decode_qr(image_path)

    if error:
        print(f"Error: {error}")
    else:
        print(f"Successfully decoded {len(results)} QR code(s):")
        for i, result in enumerate(results, 1):
            print(f"\nQR Code {i}:")
            print(f"Type: {result['type']}")
            
            # Convert decoded data to integers
            encoded_data = string_to_ints(result['data'])
            
            # Initialize Reed-Solomon decoder
            rs_n, rs_k = 255, 223
            rs = ReedSolomon(rs_n, rs_k)
            
            # Decode data with Reed-Solomon error correction
            decoded_blocks = []
            for j in range(0, len(encoded_data), rs_n):
                block = encoded_data[j:j+rs_n]
                try:
                    decoded_block = rs.decode(block)
                    decoded_blocks.extend(decoded_block)
                except ValueError as e:
                    print(f"Error in block {j//rs_n}: {str(e)}")
            
            # Convert decoded data back to string and remove padding
            decoded_data = ints_to_string(decoded_blocks).rstrip('\x00')
            
            print(f"Decoded data: {decoded_data}")
            print(f"Position: {result['rect']}")

if __name__ == "__main__":
    main()
