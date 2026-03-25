from PIL import Image
import stepic
import io

def encode_data(image_path, data, output_path):
    """
    Embeds binary data into an image using LSB steganography via stepic.
    """
    try:
        img = Image.open(image_path)
        # Convert to RGB if necessary (stepic likes RGB)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        encoded_img = stepic.encode(img, data)
        encoded_img.save(output_path, format='PNG') # PNG is lossless and preserves LSBs
        return True, "Data successfully hidden!"
    except Exception as e:
        return False, str(e)

def decode_data(image_path):
    """
    Extracts binary data from an image.
    """
    try:
        img = Image.open(image_path)
        decoded_bytes = stepic.decode(img)
        
        # Try to decode as text first
        try:
            return True, decoded_bytes.decode('utf-8'), "text"
        except UnicodeDecodeError:
            # If not text, return the raw bytes
            return True, decoded_bytes, "file"
    except Exception as e:
        return False, str(e), None
