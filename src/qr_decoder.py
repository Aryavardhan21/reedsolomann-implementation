from pyzbar.pyzbar import decode
from PIL import Image

def decode_qr(image_path):
    try:
        image = Image.open(image_path)
        decoded_objects = decode(image)
        
        if not decoded_objects:
            return None, "No QR code found in the image"

        results = []
        for obj in decoded_objects:
            results.append({
                'type': obj.type,
                'data': obj.data.decode('utf-8'),
                'rect': obj.rect,
                'polygon': obj.polygon
            })

        return results, None
    except Exception as e:
        return None, f"Error decoding QR code: {str(e)}"

# Example usage
if __name__ == "__main__":
    image_path = "example_qr.png"
    results, error = decode_qr(image_path)
    
    if error:
        print(f"Error: {error}")
    else:
        for result in results:
            print(f"Decoded {result['type']}: {result['data']}")
            print(f"Position: {result['rect']}")
