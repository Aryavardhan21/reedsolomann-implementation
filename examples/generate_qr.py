import sys
sys.path.append('..')  # Add parent directory to Python path

from src.qr_generator import generate_qr

def main():
    data = input("Enter the data to encode in QR code: ")
    error_correction_levels = {
        'L': 1,
        'M': 0,
        'Q': 3,
        'H': 2
    }
    
    ec_level = input("Enter error correction level (L, M, Q, H) [default: H]: ").upper() or 'H'
    if ec_level not in error_correction_levels:
        print("Invalid error correction level. Using H.")
        ec_level = 'H'

    box_size = int(input("Enter box size (1-50) [default: 10]: ") or 10)
    border = int(input("Enter border size (0-10) [default: 4]: ") or 4)
    
    style = input("Enter style (default or rounded) [default: default]: ").lower() or 'default'
    if style not in ['default', 'rounded']:
        print("Invalid style. Using default.")
        style = 'default'

    fill_color = input("Enter fill color [default: black]: ") or "black"
    back_color = input("Enter background color [default: white]: ") or "white"

    qr_image = generate_qr(
        data, 
        error_correction=error_correction_levels[ec_level],
        box_size=box_size,
        border=border,
        fill_color=fill_color,
        back_color=back_color,
        style=style
    )

    output_file = "generated_qr.png"
    qr_image.save(output_file)
    print(f"QR code generated and saved as {output_file}")

if __name__ == "__main__":
    main()
