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
from collections import deque
import bisect
from operator import itemgetter
from pprint import pformat
from operator import attrgetter
import numpy

deqNode = namedtuple('deqNode', ['dist', 'node'])

class Node(namedtuple('Node', 'location data filename left_child right_child parent_loc')):
  def __repr__(self):
    return pformat(tuple(self))
  furthest_distance_sq = None
  closest_list = None
  k = None

  def update(self, dist_sq):
    #bisect.insort(Node.closest_list, )
    Node.closest_list.append(deqNode(dist_sq, self))
    Node.closest_list.sort(key=lambda deqN: deqN.dist)
    while len(Node.closest_list) > Node.k:
      Node.closest_list.pop()

    Node.furthest_distance_sq = Node.closest_list[-1].dist


#DON'T DELETE i think it's needed probably
def pix1key(cell):
  print cell.pix1
  return cell.pix1[axis]

def kdtree(point_list, depth=0, parent = (0,0,0)):
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
    left_child=kdtree(point_list[:median], depth + 1, point_list[median].pix1),
    right_child=kdtree(point_list[median + 1:], depth + 1, point_list[median].pix1),
    parent_loc=parent
  )

def calc_distance(node, rgb_coord):
  #print node.location, rgb_coord, ":",
  dist = list(numpy.subtract(node.location, rgb_coord))
  dist = list(map(lambda x: x * x, dist))
  #dist = reduce(lambda x, y: x + y, dist)
  dist = dist[0] + dist[1] + dist[2]
  #print dist
  if dist <= Node.furthest_distance_sq:
    node.update(dist)


def find_closest_h(node, rgb_coord, depth = 0):
  #Travel down *favors the right side. perhaps search down both if
  ##the values are equal
  if node.left_child and node.right_child:
    axis = depth % 3
    #Go down the left branch
    if rgb_coord[axis] < node.location[axis]:
      find_closest_h(node.left_child, rgb_coord, depth + 1)
      calc_distance(node, rgb_coord)
      #check hyperplane
      if Node.furthest_distance_sq > (node.location[axis] - node.parent_loc[axis])**2: #maybe not use the FURTHEST dist
        #do other branch too
        find_closest_h(node.right_child, rgb_coord, depth + 1)
      return
    #Go down the right branch
    else:
      find_closest_h(node.right_child, rgb_coord, depth + 1)
      calc_distance(node, rgb_coord)
      #check hyperplane
      if Node.furthest_distance_sq > (node.location[axis] - node.parent_loc[axis])**2: #maybe not use the FURTHEST dist
        #do other branch too
        find_closest_h(node.left_child, rgb_coord, depth + 1)
      return
  #If a leaf is reached
  elif not node.left_child and not node.right_child:
    #Calculate distance from leaf
    calc_distance(node, rgb_coord)
    return
  #If just the left branch
  elif node.left_child:
    find_closest_h(node.left_child, rgb_coord, depth + 1)
    calc_distance(node, rgb_coord)
    return
  #If just the right branch
  elif node.right_child:      
    find_closest_h(node.right_child, rgb_coord, depth + 1)
    calc_distance(node, rgb_coord)
    return
  else:
    raise NameError('Something wrong in find_closest')





def find_closest(root_node, rgb_coord, n = 0):
  #setup
  Node.k = n
  Node.furthest_distance_sq = 200000
  Node.closest_list = [deqNode(200000, root_node)]

  find_closest_h(root_node, rgb_coord)
  #print "+++++++++++++++++++++"
  #print Node.closest_node.location, rgb_coord, Node.furthest_distance_sq
  #print len(Node.closest_list),
  return Node.closest_list
  