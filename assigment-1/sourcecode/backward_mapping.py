from PIL import Image
import math
import numpy as np


def scale(image, rate):
  width, height = image.size
  image_array = np.array(image)

  new_height = int(rate*height)
  new_width = int(rate*width)

  scaled_array = np.empty((new_height, new_width, 3), dtype=np.uint8)

  for out_x in range(new_width):
    for out_y in range(new_height):
      
      in_x = int(out_x/rate)
      in_y = int(out_y/rate)

      if 0 <= in_x < width and 0 <= in_y < height:
        scaled_array[out_y, out_x] = image_array[in_y, in_x]

  scaled_image = Image.fromarray(scaled_array)
  scaled_image.save('scaled_reduce__backward_mapping.jpg')

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

      if 0 <= in_x < width and 0 <= in_y < height:
        rotated_array[out_y, out_x] = image_array[in_y, in_x]

  rotated_image = Image.fromarray(rotated_array)
  rotated_image.save('rotated_backward_mapping.jpg')

def shear_vertical(image, rate):
  width, height = image.size
  image_array = np.array(image)
  new_width = int(width + height*rate)

  sheared_array = np.empty((height, new_width, 3), dtype=np.uint8)

  for out_x in range(new_width):
    for out_y in range(height):

      in_y = out_y
      in_x = int(out_x - rate*out_y)

      if 0 <= in_x < width and 0 <= in_y < height:
        sheared_array[out_y, out_x] = image_array[in_y, in_x]
  
  sheared_image = Image.fromarray(sheared_array)
  sheared_image.save('vertical_sheared_backward_mapping.jpg')

def shear_horizontal(image, rate):
  width, height = image.size
  image_array = np.array(image)
  new_height = int(height + width*rate)

  sheared_array = np.empty((new_height, width, 3), dtype=np.uint8)

  for out_x in range(width):
    for out_y in range(new_height):

      in_y = int(out_y - rate*out_x)
      in_x = out_x

      if 0 <= in_x < width and 0 <= in_y < height:
        sheared_array[out_y, out_x] = image_array[in_y, in_x]
  
  sheared_image = Image.fromarray(sheared_array)
  sheared_image.save('horizontal_sheared_backward_mapping.jpg')

def zoom(image, zoom_factor):
  width, height = image.size

  image_array = np.array(image)
  zoomed_array = np.empty((height, width, 3), dtype=np.uint8)

  for x in range(width):
    for y in range(height):
      in_x = x / zoom_factor
      in_y = y / zoom_factor

      if 0 <= in_x < width and 0 <= in_y < height:
        pixel = image_array[int(in_y), int(in_x)]
        zoomed_array[y, x] = pixel

  zoomed_image = Image.fromarray(zoomed_array)
  zoomed_image.save('zoomed_backward_mapping.jpg')

image = Image.open('istanbul.jpg')
scale(image, 0.6)
rotate(image, 30)
shear_vertical(image, 0.3)
shear_horizontal(image, 0.3)
zoom(image, 1.6)