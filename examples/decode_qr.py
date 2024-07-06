import sys
sys.path.append('..')  # Add parent directory to Python path

from src.qr_decoder import decode_qr

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
            print(f"Data: {result['data']}")
            print(f"Position: {result['rect']}")

if __name__ == "__main__":
    main()
