#! /usr/bin/env python3
################################################################################
#
#		Implementation of the wedding problem class
#
################################################################################
from search import *

#################
# Problem class #
#################

class Wedding(Problem):

	def __init__(self, init):
		pass

	
	def successor(self, state):
		pass

	def value(self, state):
		pass

###############
# State class #
###############

class State:

	def __init__(self, n, t, m, tables, value):
		pass

################
# Local Search #
################

def randomized_maxvalue(problem, limit=100, callback=None):
	pass

def maxvalue(problem, limit=100, callback=None):
	pass

if __name__ == '__main__':
	wedding = Wedding(sys.argv[1])
	print(wedding.initial)

	node = randomized_maxvalue(wedding, 100)	
	# node = maxvalue(wedding, 100)
	
	state = node.state
	print(state)
