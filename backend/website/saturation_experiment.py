# greg mockler
# additional code for saturation experiment 

from PIL import Image
import PIL
import sys
import numpy as np


'''
THIS CODE IS UNUSED AS THE SAME CAN BE DONE SIMPLY IN CSS 
'''

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

    ''' 
    NAIVE APPROACH, VERY SLOW
    '''

    # # Create new Image and a pixel map
    # new = Image.new("HSV", (width, height))
    # pixels = new.load()

    # # modify saturation
    # for i in range(width):
    #     for j in range(height):
    #         pixel = get_pixel(image, i, j)
    #         print(i, j)
    #         pixels[i, j] = (pixel[0], int(pixel[1]*percent), pixel[2])

    # # Return new image
    # return new
    
    '''
    NUMPY APPROACH, MUCH FASTER
    '''

    # convert original to a numpy array
    img2arr = np.array(image)

    # create delta array to multiply original by
    darr = np.ones((height, width, 3))
    
    # set saturation deltas for each pixel
    darr[:,:,1] = percent

    # multiply original array by delta array
    img2arr = np.multiply(img2arr, darr)

    # set any values above 255 back to 255
    img2arr = np.where(img2arr > 255, 255, img2arr)

    # convert back to PIL Image
    arr2im = Image.fromarray(img2arr.astype(np.uint8), mode="HSV")

    return arr2im

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        path = sys.argv[1]
        if(len(sys.argv) > 2):
            percent = float(sys.argv[2])
        else: percent = 1.5
        bump_saturation(Image.open(path), percent).convert("RGB").save("output.jpg", "JPEG")
    else: print("usage py filename.py imagepath sat_percent")
     