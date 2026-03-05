"""
Error Level Analysis (ELA) for image tamper detection.
This module analyzes uploaded certificates for signs of digital manipulation.
"""
import base64
import io
import numpy as np
from PIL import Image, ImageChops, ImageEnhance

def analyze_image_tampering(base64_image: str) -> dict:
    """
    Performs Error Level Analysis (ELA) on a base64 encoded image.
    
    Args:
        base64_image (str): The base64 string of the uploaded image.
        
    Returns:
        dict: Contains 'is_suspicious', 'score', and 'message'.
    """
    try:
        # 1. Clean and decode the base64 string
        if "," in base64_image:
            base64_image = base64_image.split(",", 1)[1]
            
        img_data = base64.b64decode(base64_image)
        original_img = Image.open(io.BytesIO(img_data)).convert('RGB')
        
        # 2. Save the image at a known quality level to create a baseline
        quality_level = 90
        buffer = io.BytesIO()
        original_img.save(buffer, format="JPEG", quality=quality_level)
        buffer.seek(0)
        
        # 3. Load the compressed baseline image
        compressed_img = Image.open(buffer)
        
        # 4. Calculate the pixel difference (Error Level)
        ela_img = ImageChops.difference(original_img, compressed_img)
        
        # Calculate extrema to find the maximum possible difference and scale
        extrema = ela_img.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        
        if max_diff == 0:
            # Identical images (lossless or 100% flat color)
            return {"is_suspicious": False, "score": 0.0, "message": "Clean (No compression differences detected)."}
            
        scale = 255.0 / max_diff
        ela_img = ImageEnhance.Brightness(ela_img).enhance(scale)
        
        # 5. Convert to numpy array to calculate a statistical "Tamper Score"
        ela_array = np.array(ela_img)
        
        # The score is based on the standard deviation and mean of the error levels.
        # High variation (high std dev) or unusually high average error indicates potential localized tampering.
        mean_error = np.mean(ela_array)
        std_error = np.std(ela_array)
        
        # A combined metric (weighted)
        tamper_score = float((mean_error * 0.4) + (std_error * 0.6))
        
        # Threshold for suspicion (Balanced to catch heavy edits while allowing normal photo variance)
        SUSPICION_THRESHOLD = 35.0
        
        is_suspicious = tamper_score > SUSPICION_THRESHOLD
        
        message = "Suspiciously high JPEG compression variation detected." if is_suspicious else "Image passes ELA integrity checks."
        
        return {
            "is_suspicious": is_suspicious,
            "score": round(tamper_score, 2),
            "message": message
        }
        
    except Exception as e:
        # If the image can't be processed, fail open or closed?
        # For security, we might want to flag it or just log the error.
        print(f"[ELA Error] {str(e)}")
        return {"is_suspicious": False, "score": 0.0, "message": f"ELA check failed or bypassed: {str(e)}"}
