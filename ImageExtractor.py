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

SCALE = 15 # double x_density is full-scale?



def ColorDict():
  global MEDIA_HEIGHT, MEDIA_WIDTH

  im = Image.open(PICTURE_DIR + "/" + os.listdir(PICTURE_DIR)[0])
  MEDIA_WIDTH = im.width
  MEDIA_HEIGHT = im.height
  im.close()



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
  im3 = im2.resize((im.width, im.height))
  
  im4 = im.resize((2 * X_DENSITY, 2 * int(im.height / NEW_MEDIA_HEIGHT)), 1)
  im5 = im4.resize((im.width, im.height))

  print im2
  print "Original perspective:", im.width, im.height, im.width / (im.height * 1.0)
  print "Shrunken perspective:", im2.width, im2.height, im2.width / (im2.height * 1.0)

  im3.show()
  im5.show()

  SCANNED_WIDTH = im2.width
  SCANNED_HEIGHT = im2.height




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

  ##final_array = find_matches(color_dict.dict, target_array)

  ##display_final_img(final_array)



if __name__ == '__main__':
  main()