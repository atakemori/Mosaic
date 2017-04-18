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

import PIL
from PIL import Image

PIC_DIR = "./media"







class ImageBox(object):
  """
  Takes in an image and returns tuples that correspond
  to the coordinates required for quandrants and edges
  """
  def __init__(self, media_image):
    im = media_image
    self.topLeftX = 0
    self.topLeftY = 0
    self.botRightX = im.width
    self.botRightY = im.height




class ColorDict(object):
  """
  Builds a dictionary containing the color values
  and names of the pictures in the PIC_DIR folder.
  """
  def __init__(self):
    self.dict = {}
    print "Path Valid: " + str(os.path.isdir(PIC_DIR))
    #Count the number of files to do for progress bar as int totNum
    ##Also ends up counting directories as files...
    totNum = len(os.listdir(PIC_DIR))
    #Iterate through files to build color data and add to dict
    for filename in os.listdir(PIC_DIR):
      im = Image.open(PIC_DIR + "/" + filename)
      #im.show()
      im.crop((0, 0, im.width / 2, im.height / 2)).show()
      print im.getpixel((0, 0))
      print im.getpixel((1, 1))

      










def main():
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
  options = sys.argv
  if len(options) > 1:
    PIC_DIR = len[1]

  color_dict = ColorDict()




  #end = False
  #while not end:
  #  end = input("End? ")


if __name__ == '__main__':
  main()