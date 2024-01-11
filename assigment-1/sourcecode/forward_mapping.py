from PIL import Image
import math
import numpy as np


def scale(image, rate):
  width, height = image.size
  image_array = np.array(image)

  new_height = int(rate*height)
  new_width = int(rate*width)

  scaled_array = np.empty((new_height, new_width, 3), dtype=np.uint8)

  for x in range(width):
    for y in range(height):
      
      new_x = int(x*rate)
      new_y = int(y*rate)

      if 0 <= new_x < new_width and 0 <= new_y < new_height:
        scaled_array[new_y, new_x] = image_array[y, x]

  scaled_image = Image.fromarray(scaled_array)
  scaled_image.save('scaled_reduce_forward_mapping.jpg')

def rotate(image, angle):
  angle = math.radians(angle)

  width, height = image.size
  image_array = np.array(image)

  center_x = width // 2
  center_y = height // 2

  new_width = int(abs(width * math.cos(angle)) + abs(height * math.sin(angle)))
  new_height = int(abs(width * math.sin(angle)) + abs(height * math.cos(angle)))
  
  rotated_array = np.empty((new_height, new_width, 3), dtype=np.uint8)

  for x in range(width):
    for y in range(height):
        pixel = image_array[y, x]

        new_x = int((x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + new_width / 2)
        new_y = int((x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + new_height / 2)

        if 0 <= new_x < new_width and 0 <= new_y < new_height:
            rotated_array[new_y, new_x] = pixel

  rotated_image = Image.fromarray(rotated_array)
  rotated_image.save('rotated_forward_mapping.jpg')

def shear_vertical(image, rate):
  width, height = image.size
  image_array = np.array(image)
  new_width = int(width + height*rate)

  sheared_array = np.empty((height, new_width, 3), dtype=np.uint8)

  for x in range(width):
    for y in range(height):
      pixel = image_array[y, x]

      new_x = int(x + rate*y)
      new_y = y

      if 0 <= new_x < new_width and 0 <= new_y < height:
        sheared_array[new_y, new_x] = pixel
  
  sheared_image = Image.fromarray(sheared_array)
  sheared_image.save('vertical_sheared_forward_mapping.jpg')

def shear_horizontal(image, rate):
  width, height = image.size
  image_array = np.array(image)
  new_height = int(height + width*rate)

  sheared_array = np.empty((new_height, width, 3), dtype=np.uint8)

  for x in range(width):
    for y in range(height):
      pixel = image_array[y, x]

      new_x = x
      new_y = int(y + rate*x)

      if 0 <= new_x < width and 0 <= new_y < new_height:
        sheared_array[new_y, new_x] = pixel
  
  sheared_image = Image.fromarray(sheared_array)
  sheared_image.save('horizontal_sheared_forward_mapping.jpg')

def zoom(image, zoom_factor):
  width, height = image.size

  image_array = np.array(image)
  zoomed_array = np.empty((height, width, 3), dtype=np.uint8)

  for x in range(width):
    for y in range(height):
      new_x = x / zoom_factor
      new_y = y / zoom_factor

      if 0 <= new_x < width and 0 <= new_y < height:
        pixel = image_array[int(new_y), int(new_x)]
        zoomed_array[y, x] = pixel

  zoomed_image = Image.fromarray(zoomed_array)
  zoomed_image.save('zoomed_forward_mapping.jpg')

image = Image.open('istanbul.jpg')
scale(image, 0.6)
rotate(image, 30)
shear_vertical(image, 0.3)
shear_horizontal(image, 0.3)
zoom(image, 1.6)