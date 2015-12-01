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
	def __init__(self, init_file):
		self.n = 0  # Number of guests
		self.t = 0  # Number of tables
		self.a = []  # Affinity persons
		self.tables = []  # Tables
		self.init_from_file(init_file)	# Initialize problem
		self.size_table = int(self.n / self.t)  # Number of person by table
		self.initial = State(self.n,self.t, self.a,self.tables)

	def init_from_file(self, file_name):
		try:
			file = open(file_name)
			i = 0
			for line in file.readlines():
				if i == 0:
					self.n = int(line)
				elif i == 1:
					self.t = int(line)
				else:
					self.a.append([])
					self.a[i - 2] = ([int(x) for x in line.split()])
				i += 1
				file.close()
		except IOError:
			print("File " + file_name + " can not be found or open")
			exit(1)


	def successor(self, state):
		for i in range(self.t):
			for j in range(self.size_table):
				for k in range(i+1 , self.t):
					for l in range(0, self.size_table):
						new_tables = [row[:] for row in state.tables]
						tmp = new_tables[i][j]
						new_tables[i][j] = new_tables[k][l]
						new_tables[k][l] = tmp
						new_tables[i].sort()
						new_tables[k].sort()
						new_state = State(state.n,state.t,state.a,new_tables)
						yield ((i,j,k,l), new_state)


	def value(self, state):
		return state.val


###############
# State class #
###############

class State:
	def __init__(self, n, t, a, tables):
		self.n = n
		self.t = t
		self.a = a
		self.tables = tables
		self.value = self.find_value(tables,a)

	def __str__(self):
		output = ""
		for i in range(0, len(self.tables)):
			self.tables[i].sort()
			for j in range(0, len(self.tables[0])):
				output += str(self.tables[i][j]) + ' '
			if i < len(self.tables) - 1:
				output += '\n'
		return output

	def set_value(self):
		val = self.find_value(self.tables, self.a)
		self.value = val

	def find_value(self,tables, a):
		val = 0
		for i in range(0, len(tables)):
			for j in range(0, len(tables[i])):
				for k in range(0, len(tables[i])):
					val += a[tables[i][j]][tables[i][k]]
		return val


################
# Local Search #
################

def randomized_maxvalue(problem, limit=100, callback=None):
	pass


def concat(state):
	result = ''
	for i in range(len(state.tables)):
		for j in range(len(state.tables[i])):
			result += str(state.tables[i][j])
	return result


def best_neighbor(state):
	best = None
	for neighbor in list(state.expand()):
		if best is None:
			best = neighbor
		elif neighbor.state.value > best.state.value:
			best = neighbor
		elif neighbor.state.value == best.state.value:
			neighbor_concat = concat(neighbor.state)
			best_concat = concat(best.state)
			if neighbor_concat < best_concat:
				best = neighbor
	return best

def maxvalue(problem,limit=100,callback=None):
	current = LSNode(problem, problem.initial, 0)
	best = current
	previous = None
	previous_previous = None
	previous_previous_previous = None
	for step in range(limit):
		if callback is not None:
			callback(current)
		current = best_neighbor(current)
		current_value = current.state.value
		if current_value > best.state.value:
			best = current
		if previous_previous_previous is not None and previous_previous_previous == previous and current_value == previous_previous:
			break; #we iterate over the same values over and over so just break here
		previous_previous_previous = previous_previous
		previous_previous = previous
		previous = current_value
	return best

def greedy(problem):
	s = int(problem.n / problem.t)
	assigned_person = [0] * problem.n
	for num_table in range(problem.t):
		new_table = []
		alone_people = find_alone_person(assigned_person)
		new_table.append(alone_people)
		assigned_person[alone_people] = 1
		available_friends = get_potential_new_friends(alone_people, assigned_person, problem.a)
		available_friends.sort(key = greedy_comp, reverse=True)
		for x in range(0,s-1):
			friend = available_friends[x]
			new_table.append(friend[0])
			assigned_person[friend[0]] = 1
		problem.tables.append(new_table)

def find_alone_person(list):
	for x in range(0, len(list)):
		if list[x] == 0:
			return x
	return -1

def get_potential_new_friends(seeker, assigned_person, friendship_table):
	result=[]
	for x in range(seeker+1, len(assigned_person)):
		if assigned_person[x] == 0:
			result.append((x,friendship_table[seeker][x]))
	return result

def greedy_comp(tuple):
    return tuple[1]

if __name__ == '__main__':
	wedding = Wedding(sys.argv[1])
	greedy(wedding)
	wedding.initial.set_value()
	print(wedding.initial.value)
	print(wedding.initial)
	# node = randomized_maxvalue(wedding, 100)
	node = maxvalue(wedding, 100)

	state = node.state
	print(node.state.value)
	print(state)
