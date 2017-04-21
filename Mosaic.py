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

import numpy
import PIL
from PIL import Image



PICTURE_DIR = "./media"
TARGET_PIC = "./target.jpg"
MEDIA_HEIGHT = -1
MEDIA_WIDTH = -1

X_DENSITY = 20

SCALE_RATIO = 10





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
    print "Path Valid: " + str(os.path.isdir(PICTURE_DIR))
    #Count the number of files to do for progress bar as int totNum
    #  Also ends up counting directories as files...
    totNum = len(os.listdir(PICTURE_DIR))
    global MEDIA_HEIGHT, MEDIA_WIDTH
    #Iterate through files to build color data and add to dict
    for filename in os.listdir(PICTURE_DIR):
      im = Image.open(PICTURE_DIR + "/" + filename)

      MEDIA_WIDTH = im.width
      MEDIA_HEIGHT = im.height

      #However it's done, it needs to end up with 4 colored quadrants
      im = im.resize((2, 2))
      self.dict[filename] = list(im.getdata())


      """
      print filename
      print im.getpixel((0,0)),
      print im.getpixel((1,0))
      print im.getpixel((0,1)),
      print im.getpixel((1,1))
      im.resize((40, 40)).show()
      print self.dict[filename]

      break
      """


#Eventually do at sizes large enough where perspectives are
##easily divisible so perspectives stay relatively similar
def pixelate_target():
  im = Image.open(TARGET_PIC)
  targetWidth = im.width / X_DENSITY #a
  #targetHeight = im.height / SCALE_RATIO
  #targetPerspective = im.width / (im.height * 1.0)
  mediaPerspective = (MEDIA_HEIGHT * 1.0) / MEDIA_WIDTH #c

  newMediaWidth = targetWidth
  newMediaHeight = int(newMediaWidth * mediaPerspective) #b
  print newMediaWidth, newMediaHeight

  im2 = im.resize((2 * X_DENSITY, 2 * int(im.height / newMediaHeight)))
  im3 = im2.resize((im.width, im.height))
  print im2


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
  for pair in media_dict.items():
    new_value = 0
    for i in range(len(target_tup)):
      #print target_tup, pair[1]
      a = list(numpy.subtract(target_tup[i], pair[1][i]))
      a = list(map(lambda x: x * x, a))
      a = reduce(lambda x, y: x + y, a)
      new_value += a
    #print new_value
    new_dict[new_value] = pair[0]
  #new_dict.values().sort()[0]
  #print new_dict.items()
  #b = list(sorted(new_dict.items()))
  #print list(sorted(new_dict.items()))[0][1]
  return list(sorted(new_dict.items()))[0][1]
  #print b[0], b[-1]



#   media_dict.get(num, data[min(data.keys(), key=lambda k: abs(k-num))])
def find_matches(media_dict, target_array):
  final_name_array = [[0 for y in range(len(target_array[0]) / 2)]
                         for y in range(len(target_array) / 2)]
  for x in range(len(target_array))[::2]:
    for y in range(len(target_array[0]))[::2]:
      a = (target_array[x][y], target_array[x+1][y],
           target_array[x][y+1], target_array[x+1][y+1])
      final_name_array[x / 2][y / 2] = closest_pic(media_dict, a)
      print ".",
    print "."
  print final_name_array


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

  find_matches(color_dict.dict, target_array)



if __name__ == '__main__':
  main()