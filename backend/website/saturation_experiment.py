# greg mockler
# additional code for saturation experiment 

from pillow import Image

# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
      return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel

# modify the Saturation value of an image
def bump_saturation(image, percent):
    image = image.convert("HSV")

    # Get size
    width, height = image.size

    # Create new Image and a pixel map
    new = Image.new("HSV", (width, height))
    pixels = new.load()

    # modify saturation
    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            pixels[i, j] = (pixel[0], pixel[1]*percent, pixel[2])

    # Return new image
    return pixels