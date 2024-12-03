from PIL import Image

def convert(filepath, format):
    img_png = Image.open(filepath)
    img_png.save("./export."+str(format))