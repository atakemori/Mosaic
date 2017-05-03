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
from PIL import ImageTk
from PIL import Image as PillowImage
from collections import namedtuple
import time
from Tkinter import *

import kdTree



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


X_DENSITY =15

SCALE = 5 # double x_density is full-scale?

K_NN = 10

CLOSENESS = 5000

final_image_name = 'Density{0} Scale{1} Knn{2} Closeness{3} interactive.jpg'.format(
                                                X_DENSITY, SCALE, K_NN, CLOSENESS)

FINAL_IMAGE = None

Cell = namedtuple('Cell', ['name', 'pix4', 'pix1'])


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
    self.kd_list = []
    self.kd_tree = None
    global MEDIA_HEIGHT, MEDIA_WIDTH

    try:
      self.kd_tree = pickle.load(open("kd_tree.p", "rb"))
      self.kd_list = pickle.load(open("kd_list.p", "rb")) #might take too long
    except IOError as e:
      print "Building new media database"
      print "New Images:",

    print "Path Valid: " + str(os.path.isdir(PICTURE_DIR))
    #Count the number of files to do for progress bar as int totNum
    ##Also ends up counting directories as files...
    totNum = len(os.listdir(PICTURE_DIR))

    im = PillowImage.open(PICTURE_DIR + "/" + os.listdir(PICTURE_DIR)[0])
    MEDIA_WIDTH = im.width
    MEDIA_HEIGHT = im.height
    im.close()


    new_files = [x for x in os.listdir(PICTURE_DIR)
                   if x not in [cell.name for cell in self.kd_list]]
    #Iterate through files to build color data and add to dict
    for filename in new_files:
      im = PillowImage.open(PICTURE_DIR + "/" + filename)
      #However it's done, it needs to end up with 4 colored quadrants
      im = im.resize((2, 2), PillowImage.LANCZOS)
      im2 = im.resize((1, 1), PillowImage.LANCZOS)
      #self.dict[filename] = list(im.getdata())
      #self.kd_list.extend(filename)
      self.kd_list.append(Cell(filename, list(im.getdata()), im2.getpixel((0,0))))
      print "+",
    #print self.kd_list

    if len(new_files) > 0:
      self.kd_tree = kdTree.kdtree(self.kd_list)
      pickle.dump(self.kd_tree, open("kd_tree.p", "wb"))
      pickle.dump(self.kd_list, open("kd_list.p", "wb"))
      print "Media Dictionary Updated"

    #print self.kd_tree

#Eventually do at sizes large enough where perspectives are
##easily divisible so perspectives stay relatively similar
def pixelate_target():
  im = PillowImage.open(TARGET_PIC)
  global TARGET_WIDTH, MEDIA_PERSPECTIVE, NEW_MEDIA_HEIGHT, NEW_MEDIA_WIDTH
  global SCANNED_HEIGHT, SCANNED_WIDTH

  TARGET_WIDTH = im.width / X_DENSITY #a
  #targetHeight = im.height / SCALE_RATIO
  #targetPerspective = im.width / (im.height * 1.0)
  MEDIA_PERSPECTIVE = (MEDIA_HEIGHT * 1.0) / MEDIA_WIDTH #c

  NEW_MEDIA_WIDTH = TARGET_WIDTH
  NEW_MEDIA_HEIGHT = int(NEW_MEDIA_WIDTH * MEDIA_PERSPECTIVE) #b
  print NEW_MEDIA_WIDTH, NEW_MEDIA_HEIGHT

  im2 = im.resize((2 * X_DENSITY, 2 * int(im.height / NEW_MEDIA_HEIGHT)), PillowImage.LANCZOS)
  im3 = im2.resize((X_DENSITY, int(im.height / NEW_MEDIA_HEIGHT)), PillowImage.LANCZOS)
  print im2

  SCANNED_WIDTH = im2.width
  SCANNED_HEIGHT = im2.height
  targetData = [[0 for y in range(im2.height)] for x in range(im2.width)]
  targetData_small = [[0 for y in range(im3.height)] for x in range(im3.width)]

  #Starts tracking target color data from top left, 
  #  travels down the y, and the across x
  for x in range(im2.width):
    for y in range(im2.height):
      targetData[x][y] = im2.getpixel((x, y))

  for x in range(im3.width):
    for y in range(im3.height):
      targetData_small[x][y] = im3.getpixel((x, y))

  print "Number of Cells: ", len(targetData), "x", len(targetData[0])
  print "Total Number:", len(targetData) * len(targetData[0])

  target_values = namedtuple('TargetVal', ['big', 'small'])
  return target_values(targetData, targetData_small)

#Prime for optimizing later ESPECIALLY SINCE I DONT THINK I NEED TO USE
##ALL THESE DICTS
#or maybe not pass the media_dict/TREEEEEEEE
def closest_pic(node_list, target_tup):
  new_dict = {}
  for node in node_list:
    new_value = 0
    for i in range(len(target_tup)):
      #print target_tup, value
      a = list(numpy.subtract(target_tup[i], node.data[i]))
      a = list(map(lambda x: x * x, a))
      a = reduce(lambda x, y: x + y, a)
      new_value += a
    new_dict[new_value] = node #what does this do

  closest_list = list(sorted(new_dict.items()))

  if closest_list[1][0] - closest_list[0][0] > CLOSENESS:
    #returns the 4 closest nodes if diff is too great
    return [tup[1] for tup in closest_list[:4]]
  else:
    return closest_list[0][1].filename

def closest_pic_orig(node_list, target_tup):
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


#   media_dict.get(num, data[min(data.keys(), key=lambda k: abs(k-num))])
def find_matches(media_tree, target_array, target_array_small):
  final_name_array = [[0 for y in range(len(target_array[0]) / 2)]
                         for y in range(len(target_array) / 2)]
  final_name_dict = {}
  inter_dict = {}
  print "Analyzing Matches:",
  for x in range(len(target_array))[::2]:
    for y in range(len(target_array[0]))[::2]:
      a = (target_array[x][y], target_array[x+1][y],
           target_array[x][y+1], target_array[x+1][y+1])
      b = target_array_small[x/2][y/2]
      #Gets closest node based on single pixel
      closest_list_tups = kdTree.find_closest(media_tree, b, K_NN)
      closest_nodes = [tup.node for tup in closest_list_tups]
      #Gets name after running closest nodes through old comparer 
      tile_title = closest_pic(closest_nodes, a)
      if type(tile_title) is str:
        try:
          final_name_dict[tile_title].append((x/2, y/2))
        except Exception as e:
          final_name_dict[tile_title] = [(x/2, y/2)]
      else:
        #return dict of xy coords and 4 
        inter_dict[(x/2, y/2)] = tile_title

    if x % (len(target_array) / 10) == 0: print ".",
  
  print "\n"
  #print final_name_dict.keys()
  return (final_name_dict, inter_dict)

def create_img_template():
  global NEW_MEDIA_HEIGHT, NEW_MEDIA_WIDTH, FINAL_IMAGE
  NEW_MEDIA_WIDTH *= SCALE
  NEW_MEDIA_HEIGHT *= SCALE

  print "Old:", MEDIA_WIDTH ,MEDIA_HEIGHT
  print "New:", NEW_MEDIA_WIDTH, NEW_MEDIA_HEIGHT

  final_width = (SCANNED_WIDTH * NEW_MEDIA_WIDTH) / 2
  final_height = (SCANNED_HEIGHT * NEW_MEDIA_HEIGHT) / 2

  FINAL_IMAGE = PillowImage.new("RGB", (final_width, final_height), (255, 255, 255))


#TODO if final img large, split into quads with another for loop
def final_img_build(final_dict):
  #im = PillowImage.open(PICTURE_DIR + "/" + ******)
  print "Number of unigue cells: " + str(len(final_dict.keys()))
  print "Assembling Final Picture:"

  for tile, coords_list in final_dict.iteritems():
    im = PillowImage.open(PICTURE_DIR + "/" + tile)
    im = im.resize((NEW_MEDIA_WIDTH, NEW_MEDIA_HEIGHT))
    for xy in coords_list:
      FINAL_IMAGE.paste(im, (xy[0] * NEW_MEDIA_WIDTH, xy[1] * NEW_MEDIA_HEIGHT))
    print ".",

  #FINAL_IMAGE.save("currentKD.jpg")

def save_img():
  FINAL_IMAGE.save(final_image_name)
  FINAL_IMAGE.show()

def interactive_fill(fill_array, todo_dict):
  #open tkinter main window
  master = Tk()
  #create 4 partitions on the bottom and one on top

  #assign names/values to bottome buttons
  for coord, nodes in todo_dict:
    pass
    #open 4 images, resize to show in window
    #show portion of original image
    #user selects desired picture
    #prints desired cell in FINAL_IMAGE


def main():
  start_time = time.time()
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
  global TARGET_PIC, PICTURE_DIR
  options = sys.argv
  if len(options) > 2:
    TARGET_PIC = len[1]
  if len(options) > 3:
    PICTURE_DIR = len[2]

  color_dict = ColorDict()

  #TODO: pixelate_target should be passed the target location instead of assuming
  targets_ntup = pixelate_target()

  final = find_matches(color_dict.kd_tree, targets_ntup.big, targets_ntup.small)
  final_array = final[0]
  final_dict = final[1]


  create_img_template()

  print("--- %s seconds ---" % (time.time() - start_time))

  final_img_build(final_array)
  interactive_fill(final_array, final_dict)

  save_img()
  print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
  main()