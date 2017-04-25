#Python Mosaic Builder
#Alexander Takemori 
#https://takemori.us/projects
#Created: 16 April 2017

"""
Currently only will take images with the same size
"""


import sys
import os
import random

import pickle
import numpy
import PIL
from PIL import Image



PICTURE_DIR = "./media"
TARGET_PIC = "./target.jpg"
MEDIA_HEIGHT = -1
MEDIA_WIDTH = -1

TARGET_WIDTH = "a"
MEDIA_PERSPECTIVE = "c"
NEW_MEDIA_WIDTH = "d"
NEW_MEDIA_HEIGHT = "b"

SCANNED_WIDTH = -1
SCANNED_HEIGHT = -1


X_DENSITY = 50

SCALE = 10 # double x_density is full-scale?





class ImageBox(object):
  """
  "Takes in an image and returns tuples that correspond
  "to the coordinates required for quandrants and edges
  """
  def __init__(self, media_image):
    im = media_image
    self.topLeftX = 0
    self.topLeftY = 0
    self.botRightX = im.width
    self.botRightY = im.height

  def botRightQuad(self):
    return ((self.botRightX / 2, self.botRightY / 2, 
            self.botRightX, self.botRightY))



#may not need to be an object
class ColorDict(object):
  """
  "Builds a dictionary containing the color values
  "and names of the pictures in the PIC_DIR folder.
  """
  def __init__(self):
    self.dict = {}
    global MEDIA_HEIGHT, MEDIA_WIDTH

    try:
      self.dict = pickle.load(open("media_dict.p", "rb"))
    except IOError as e:
      print "Building new media database"
      print "New Images:",

    print "Path Valid: " + str(os.path.isdir(PICTURE_DIR))
    #Count the number of files to do for progress bar as int totNum
    #  Also ends up counting directories as files...
    totNum = len(os.listdir(PICTURE_DIR))

    im = Image.open(PICTURE_DIR + "/" + os.listdir(PICTURE_DIR)[0])
    MEDIA_WIDTH = im.width
    MEDIA_HEIGHT = im.height
    im.close()

    new_files = [x for x in os.listdir(PICTURE_DIR)
                   if x not in self.dict.keys()]
    #Iterate through files to build color data and add to dict
    for filename in new_files:
      im = Image.open(PICTURE_DIR + "/" + filename)
      print "+",
      #However it's done, it needs to end up with 4 colored quadrants
      im = im.resize((2, 2), Image.LANCZOS)
      im2 = im.resize((1, 1), Image.LANCZOS)
      self.dict[filename] = (list(im.getdata()), im2.getpixel((0, 0)))

    if len(new_files) > 0:
      pickle.dump(self.dict, open("media_dict.p", "wb"))
      print "Media Dictionary Updated"


#TODO if final img large, split into quads with another for loop
def display_final_img(final_dict):
  #im = Image.open(PICTURE_DIR + "/" + ******)
  global NEW_MEDIA_HEIGHT, NEW_MEDIA_WIDTH
  NEW_MEDIA_WIDTH *= SCALE
  NEW_MEDIA_HEIGHT *= SCALE

  print "Old:", MEDIA_WIDTH ,MEDIA_HEIGHT
  print "New:", NEW_MEDIA_WIDTH, NEW_MEDIA_HEIGHT

  final_width = (SCANNED_WIDTH * NEW_MEDIA_WIDTH) / 2
  final_height = (SCANNED_HEIGHT * NEW_MEDIA_HEIGHT) / 2

  final_image = Image.new("RGB", (final_width, final_height), (255, 255, 255))

  print "Number of unigue cells: " + str(len(final_dict.keys()))
  print "Assembling Final Picture:"

  for tile, coords_list in final_dict.iteritems():
    im = Image.open(PICTURE_DIR + "/" + tile)
    im = im.resize((NEW_MEDIA_WIDTH, NEW_MEDIA_HEIGHT))
    for xy in coords_list:
      final_image.paste(im, (xy[0] * NEW_MEDIA_WIDTH, xy[1] * NEW_MEDIA_HEIGHT))
    print ".",

  final_image.save("current.jpg")
  final_image.show()


#Eventually do at sizes large enough where perspectives are
##easily divisible so perspectives stay relatively similar
def pixelate_target():
  im = Image.open(TARGET_PIC)
  global TARGET_WIDTH, MEDIA_PERSPECTIVE, NEW_MEDIA_HEIGHT, NEW_MEDIA_WIDTH
  global SCANNED_HEIGHT, SCANNED_WIDTH

  TARGET_WIDTH = im.width / X_DENSITY #a
  #targetHeight = im.height / SCALE_RATIO
  #targetPerspective = im.width / (im.height * 1.0)
  MEDIA_PERSPECTIVE = (MEDIA_HEIGHT * 1.0) / MEDIA_WIDTH #c

  NEW_MEDIA_WIDTH = TARGET_WIDTH
  NEW_MEDIA_HEIGHT = int(NEW_MEDIA_WIDTH * MEDIA_PERSPECTIVE) #b
  print NEW_MEDIA_WIDTH, NEW_MEDIA_HEIGHT

  im2 = im.resize((2 * X_DENSITY, 2 * int(im.height / NEW_MEDIA_HEIGHT)), Image.LANCZOS)
  print im2

  SCANNED_WIDTH = im2.width
  SCANNED_HEIGHT = im2.height
  targetData = [[0 for y in range(im2.height)] for x in range(im2.width)]

  #Starts tracking target color data from top left, 
  #  travels down the y, and the across x
  for x in range(im2.width):
    for y in range(im2.height):
      targetData[x][y] = im2.getpixel((x, y))
  return targetData


def media_key():
  pass
#Prime for optimizing later ESPECIALLY SINCE I DONT THINK I NEED TO USE
##ALL THESE DICTS
#or maybe not pass the media_dict
def closest_pic(media_dict, target_tup):
  new_dict = {}
  for key, value in media_dict.items():
    new_value = 0
    for i in range(len(target_tup)):
      #print target_tup, value
      a = list(numpy.subtract(target_tup[i], value[0][i]))
      a = list(map(lambda x: x * x, a))
      a = reduce(lambda x, y: x + y, a)
      new_value += a
    new_dict[new_value] = key #what does this do


  return list(sorted(new_dict.items()))[0][1]

  """
  num = random.random()
  if num < .7:
    return list(sorted(new_dict.items()))[0][1]
  elif num < .9:
    return list(sorted(new_dict.items()))[1][1]
  else:
    return list(sorted(new_dict.items()))[2][1]
  """
  #print b[0], b[-1]



#   media_dict.get(num, data[min(data.keys(), key=lambda k: abs(k-num))])
def find_matches(media_dict, target_array):
  final_name_array = [[0 for y in range(len(target_array[0]) / 2)]
                         for y in range(len(target_array) / 2)]
  final_name_dict = {}
  print "Analyzing Matches:",
  for x in range(len(target_array))[::2]:
    for y in range(len(target_array[0]))[::2]:
      a = (target_array[x][y], target_array[x+1][y],
           target_array[x][y+1], target_array[x+1][y+1])
      tile_title = closest_pic(media_dict, a)
      try:
        final_name_dict[tile_title].append((x/2, y/2))
      except Exception as e:
        final_name_dict[tile_title] = [(x/2, y/2)]
    if x % (len(target_array) / 10) == 0: print ".",
  
  print "\n"
  #print final_name_dict
  return final_name_dict


  #print len(targetData[0])
  #im.getpixel((im.width / 4, im.height / 4))


  #USE 2 for loops to got through the image (offset by a quarter media image
  #vI think), and use some box approximation for best color in that location
  #and organize the results in a 2D array.u






def main():
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
  options = sys.argv
  if len(options) > 2:
    TARGET_PIC = len[1]
  if len(options) > 3:
    PICTURE_DIR = len[2]

  color_dict = ColorDict()

  #TODO: pixelate_target should be passed the target location instead of assuming
  target_array = pixelate_target()

  final_array = find_matches(color_dict.dict, target_array)

  display_final_img(final_array)



if __name__ == '__main__':
  main()