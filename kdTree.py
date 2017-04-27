#Python Mosaic Builder
#Alexander Takemori 
#https://takemori.us/projects
#Created: 16 April 2017

#This code adapted from wikipedia page on kd trees
#https://en.wikipedia.org/wiki/K-d_tree

"""
K-d_tree implementation
"""

from collections import namedtuple
from operator import itemgetter
from pprint import pformat
from operator import attrgetter
import numpy

class Node(namedtuple('Node', 'location data filename left_child right_child')):
  def __repr__(self):
    return pformat(tuple(self))
  closest_node = None
  closest_distance_sq = None

def pix1key(cell):
  print cell.pix1
  return cell.pix1[axis]

def kdtree(point_list, depth=0):
  #try:
  #    k = len(point_list[0]) # assumes all points have the same dimension
  #except IndexError as e: # if not point_list:
  #    return None
  if len(point_list) == 0:
    return None
  
  # Select axis based on depth so that axis cycles through all valid values
  #axis = depth % k
  axis = depth % 3

  # Sort point list and choose median as pivot element
  point_list.sort(key= lambda cell: cell.pix1[axis])
  median = len(point_list) // 2 # choose median
 
  # Create node and construct subtrees
  return Node(
    location=point_list[median].pix1,
    data=point_list[median].pix4,
    filename=point_list[median].name,
    left_child=kdtree(point_list[:median], depth + 1),
    right_child=kdtree(point_list[median + 1:], depth + 1)
  )

def calc_distance(node, rgb_coord):
  dist = list(numpy.subtract(node.location, rgb_coord))
  dist = list(map(lambda x: x * x, dist))
  dist = reduce(lambda x, y: x + y, dist)

  if a <= Node.closest_distance_sq:
    Node.closest_distance_sq = dist
    Node.closest_node = node


def find_closest_h(node, rgb_coord, depth = 0):
  #If a leaf is reached
  if not node.left_child && not node.right_child:
    #Calculate distance from leaf
    dist = list(numpy.subtract(node.location, rgb_coord))
    dist = list(map(lambda x: x * x, dist))
    dist = reduce(lambda x, y: x + y, dist)
    #i'm so confused
    if Node.closest_node && (a > Node.closest_distance_sq):
      return
    else:
      Node.closest_distance_sq = dist
      Node.closest_node = node
      return
  #Travel down *favors the right side. perhaps search down both if
  ##the values are equal
  elif node.left_child && node.right_child:
    axis = depth % 3
    if Node.closest_node.location[axis] < rgb_coord[axikills]:
      find_closest_h(node.left_child, rgb_coord, depth + 1)
      calc_distance(node, rgb_coord)
      #if Node.closest_distance_sq > 
      #implement hypersphere/hyperplane crossing condition
      return
    else:
      find_closest_h(node.right_child, rgb_coord, depth + 1)
      calc_distance(node, rgb_coord)
      return
  elif node.left_child:
    find_closest_h(node.left_child, rgb_coord, depth + 1)
    calc_distance(node, rgb_coord)
    return
  elif node.right_child:      
    find_closest_h(node.right_child, rgb_coord, depth + 1)
    calc_distance(node, rgb_coord)
    return
  else:
    raise NameError('Something wrong in find_closest')





def find_closest(root_node, rgb_coord):
  Node.closest_node = None
  Node.closest_distance_sq = None
  find_closest_h(root_node, rgb_coord)
  return Node.closest_node
  