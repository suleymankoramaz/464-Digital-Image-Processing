from PIL import Image
import math
import numpy as np


def interpolation(x, y, image_array):
    x1 = math.floor(x)
    x2 = x1 + 1 if x1 < image_array.shape[1] - 1 else x1
    y1 = math.floor(y)
    y2 = y1 + 1 if y1 < image_array.shape[0] - 1 else y1

    p11 = image_array[y1, x1]
    p12 = image_array[y1, x2]
    p21 = image_array[y2, x1]
    p22 = image_array[y2, x2]

    if x1 < 0 or y1 < 0 or x2 >= image_array.shape[1] or y2 >= image_array.shape[0]:
        raise ValueError("Interpolation indices out of bounds")

    pixel_value = (1 - (x - x1)) * (1 - (y - y1)) * p11 + \
                  (x - x1) * (1 - (y - y1)) * p12 + \
                  (1 - (x - x1)) * (y - y1) * p21 + \
                  (x - x1) * (y - y1) * p22

    return pixel_value

def scale(image, rate):
    width, height = image.size
    image_array = np.array(image)

    new_height = int(rate * height)
    new_width = int(rate * width)

    scaled_array = np.empty((new_height, new_width, 3), dtype=np.uint8)

    for out_x in range(new_width):
        for out_y in range(new_height):
            in_x = out_x / rate
            in_y = out_y / rate

            x_floor, y_floor = math.floor(in_x), math.floor(in_y)

            if 0 <= x_floor < width - 1 and 0 <= y_floor < height - 1:
                scaled_array[out_y, out_x] = interpolation(in_x, in_y, image_array)

    scaled_image = Image.fromarray(scaled_array)
    scaled_image.save('scaled_reduce_backward_mapping_bilinear.jpg')
    
def rotate(image, angle):
    angle = math.radians(angle)

    width, height = image.size
    image_array = np.array(image)

    new_width = int(abs(width * math.cos(angle)) + abs(height * math.sin(angle)))
    new_height = int(abs(width * math.sin(angle)) + abs(height * math.cos(angle)))

    new_center_x = new_width // 2
    new_center_y = new_height // 2

    rotated_array = np.empty((new_height, new_width, 3), dtype=np.uint8)

    for out_x in range(new_width):
        for out_y in range(new_height):
            in_x = int((out_x - new_center_x) * math.cos(angle) + (out_y - new_center_y) * math.sin(angle) + width/2)
            in_y = int((out_y - new_center_y) * math.cos(angle) - (out_x - new_center_x) * math.sin(angle) + height/2)

            x_floor, y_floor = math.floor(in_x), math.floor(in_y)

            if 0 <= x_floor < width - 1 and 0 <= y_floor < height - 1:
                rotated_array[out_y, out_x] = interpolation(in_x, in_y, image_array)

    rotated_image = Image.fromarray(rotated_array)
    rotated_image.save('rotated_backward_mapping_bilinear.jpg')

def shear_vertical(image, rate):
    width, height = image.size
    image_array = np.array(image)
    new_width = int(width + height*rate)

    sheared_array = np.empty((height, new_width, 3), dtype=np.uint8)

    for out_x in range(new_width):
        for out_y in range(height):
            in_y = out_y
            in_x = out_x - rate * out_y

            x_floor, y_floor = math.floor(in_x), math.floor(in_y)
            
            if 0 <= x_floor < width - 1 and 0 <= y_floor < height - 1:
                sheared_array[out_y, out_x] = interpolation(in_x, in_y, image_array)

    sheared_image = Image.fromarray(sheared_array)
    sheared_image.save('vertical_sheared_backward_mapping_bilinear.jpg')

def shear_horizontal(image, rate):
    width, height = image.size
    image_array = np.array(image)
    new_height = int(height + width*rate)

    sheared_array = np.empty((new_height, width, 3), dtype=np.uint8)

    for out_x in range(width):
        for out_y in range(new_height):
            in_y = out_y - rate * out_x
            in_x = out_x

            x_floor, y_floor = math.floor(in_x), math.floor(in_y)
            
            if 0 <= x_floor < width - 1 and 0 <= y_floor < height - 1:
                sheared_array[out_y, out_x] = interpolation(in_x, in_y, image_array)

    sheared_image = Image.fromarray(sheared_array)
    sheared_image.save('horizontal_sheared_backward_mapping_bilinear.jpg')

def zoom(image, zoom_factor):
    width, height = image.size

    image_array = np.array(image)
    zoomed_array = np.empty((height, width, 3), dtype=np.uint8)

    for x in range(width):
        for y in range(height):
            in_x = x / zoom_factor
            in_y = y / zoom_factor

            x_floor, y_floor = math.floor(in_x), math.floor(in_y)

            if 0 <= x_floor < width - 1 and 0 <= y_floor < height - 1:
                zoomed_array[y, x] = interpolation(in_x, in_y, image_array)

    zoomed_image = Image.fromarray(zoomed_array)
    zoomed_image.save('zoomed_backward_mapping_bilinear.jpg')

image = Image.open('istanbul.jpg')
scale(image, 0.6)
rotate(image, 30)
shear_vertical(image, 0.3)
shear_horizontal(image, 0.3)
zoom(image, 1.6)