import math
import numpy as np

def get_image_dimensions(img):
  dims = ()
  if hasattr(img, 'shape'):
    dims = img.shape
  else:
    raise Exception('Object is not an numpy ndarray. Image object must be represented as numpy ndarray')

  if len(dims) < 2:
    raise Exception('Invalid object passed. Object has incorrect dimensions for image.')
  
  return len(dims), dims
def get_padded_image(img, no_of_padding, padding_value=0):
  if no_of_padding < 0:
    raise Exception('WARNING: padding cannot be less than 0.')
  if no_of_padding == 0:
    return img
  
  x, y, z = 1, 1, 1
  n, dims = get_image_dimensions(img)
  if n == 2:
    x, y = dims[0], dims[1]
  elif n == 3:
    x, y, z = dims[0], dims[1], dims[2]

  limg = img.tolist()

  if n == 2:
    vertical_pad = [padding_value for i in range(y + no_of_padding*2)]

    for p in range(no_of_padding):
      for i in range(x):
        limg[i].insert(0, padding_value)
        limg[i].append(padding_value)
    
    for p in range(no_of_padding):
      limg.insert(0, vertical_pad)
      limg.append(vertical_pad)
  
  elif n == 3:
    vertical_pad = [[padding_value for i in range(z)] for i in range(y + no_of_padding*2)]

    for p in range(no_of_padding):
      for i in range(x):
        limg[i].insert(0, [padding_value for i in range(z)])
        limg[i].append([padding_value for i in range(z)])
    
    for p in range(no_of_padding):
      limg.insert(0, vertical_pad)
      limg.append(vertical_pad)

  return np.array(limg)


def convolve_2D(img, filter, padding=0, stride=1):
  if stride < 1:
    raise Exception('WARNING: stride value must be minimum 1.')  


  fn, fdims = get_image_dimensions(filter)
  if fn > 2:
    raise Exception('WARNING: convolve_2D() function only convolves 2D images with 2D filters.')
  
  fx, fy = fdims[0], fdims[1]


  n, dims = get_image_dimensions(img)
  
  if n == 3:
    raise Exception('WARNING: convolve_2D() function only convolves 2D images with 2D filters.')
  elif n > 3:
    raise Exception('WARNING: unsupported dimensions. convolve() can only convolve 2D or 3D images')
  
  x, y = dims[0], dims[1]


  padded_img = get_padded_image(img, no_of_padding=padding, padding_value=0)
  pn, pdims = get_image_dimensions(padded_img)
  px, py = pdims[0], pdims[1]

  
  convolved_img = []
  cx = math.floor((x + 2*padding - fx)/stride) + 1
  cy = math.floor((y + 2*padding - fy)/stride) + 1

  # for i in range(cx):
  #   convolved_img.append([])
  #   for j in range(cy):
  #     convolved_img[i].append(0)

  conv_values = []
  f_cells = fx * fy

  for pi in range(0, (px - fx + 1), 2):
    for pj in range(0, (py - fy + 1), 2):
      sum = 0

      for fi in range(fx):
        for fj in range(fy):
          sum += padded_img[pi+fi][pj+fj] * filter[fi][fj]
      
      conv_values.append(round_to_int(sum / f_cells))

  if len(conv_values) != cx * cy:
    raise Exception('WARNING: dimensional problems occurred!')

  for i in range(cx):
    convolved_img.append([])
    for j in range(cy):
      convolved_img[i].append(conv_values[i+j])


  print('Stride size: \t', stride)
  print('Padding size: \t', padding)
  print('Filter dims: \t', fx, 'x', fy)
  print('Image dims: \t', x, 'x', y)
  print('ConvImg dims: \t', cx, 'x', cy)
  print()
  return np.array(convolved_img)