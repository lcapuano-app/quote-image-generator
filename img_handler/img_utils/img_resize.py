from PIL import Image

def resize_by_percentage( img: Image, percentage: float )-> Image:
  width, height = img.size
  resized_dimensions = (int(width * percentage), int(height * percentage))
  resized = img.resize(resized_dimensions)
  return resized

def resize_by_height( origin: Image, dest: Image, proportion: float = 1/5 )-> Image:
  origin_w, origin_h = origin.size
  dest_w, dest_h = dest.size
  img_h = int(dest_h * proportion)
  ratio = 1

  if origin_h > img_h:
    ratio =  1 + ( (origin_h - img_h) / img_h )
  else:
    ratio =  1 + ((img_h - origin_h) / origin_h)

  return resize_by_percentage( origin, ratio )


