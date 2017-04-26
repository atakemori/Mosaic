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

class Node(namedtuple('Node', 'location data filename left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))

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
