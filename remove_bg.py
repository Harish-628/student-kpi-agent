import sys
from PIL import Image

def remove_white_background(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    newData = []
    # threshold for considering a pixel "white"
    threshold = 240
    
    for item in datas:
        if item[0] >= threshold and item[1] >= threshold and item[2] >= threshold:
            # changing the alpha value to 0 for white pixels
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        remove_white_background(sys.argv[1], sys.argv[2])
