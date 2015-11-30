#! /usr/bin/env python3
################################################################################
#
#		Implementation of the wedding problem class
#
################################################################################
import time
from search import *
from copy import deepcopy


#################
# Problem class #
#################

class Wedding(Problem):
    def __init__(self, input_file):
        self.n = 0
        self.t = 0
        self.a = []
        self.read_input_file(input_file)
        size_table = int(self.n / self.t)
        self.tables = [[None for x in range(0,size_table)] for y in range(0,self.t)]
        self.val = 0
        self.initial = State(self.n, self.t, self.a, self.tables, self.val)

    def successor(self, state):
        for i in range (0, len(state.tables)):
            for l in range(0, len(state.tables[0])):
                for j in range(i+1 , len(state.tables)):
                    if i != j:
                        for k in range(0, len(state.tables[0])):
                            new_tables = deepcopy(state.tables)
                            temp = new_tables[i][l]
                            new_tables[i][l] = new_tables[j][k]
                            new_tables[j][k] = temp
                            new_state = State(self.n, self.t, self.a, new_tables, 0)
                            #new_state.val = self.value(new_state)
                            yield ((i,l,j,k), new_state)

    def value(self, state):
        val = 0
        for i in range(0, len(state.tables)):
            for k in range(0, len(state.tables[0])):
                for l in range(0, len(state.tables[0])):
                    if k != l:
                        val += state.m[state.tables[i][k]][state.tables[i][l]]
        return val

    def read_input_file(self, input_file):
        try:
            file = open(input_file)
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
        except IOError:
            print("File " + input_file + " can not be found or open")
            exit(1)


###############
# State class #
###############

class State:
    def __init__(self, n, t, m, tables, val):
        self.n = n
        self.t = t
        self.m = m
        self.tables = tables
        self.val = val
        #self.sort_tables()

    def sort_tables(self):
        if len(self.tables) > 0 and len(self.tables[0]) and self.tables[0][0] is not None:
            for table in self.tables:
                table.sort()

    def __str__(self):
        output = ""
        for i in range(0, len(self.tables)):
            self.tables[i].sort()
            for j in range(0, len(self.tables[0])):
                output += str(self.tables[i][j]) + ' '
            if i < len(self.tables)-1:
                output += '\n'
        return output


################
# Local Search #
################

def randomized_maxvalue(problem, limit=100, callback=None):
    pass


def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = None
    previous = None
    previous_previous = None
    previous_previous_previous = None
    for step in range(limit):
        if callback is not None:
            callback(current)
        for node in list(current.expand()):
            if best is None:
                best = node
            if node.value() > best.value():
                best = node
            elif node.value() == best.value():
                #need to compare them with the concatenation of the 2 states's tables
                found = False
                for i in range(len(node.state.tables)):
                    if found: break
                    for j in range(len(node.state.tables[0])):
                        if found: break
                        if node.state.tables[i][j] > best.state.tables[i][j]:
                            best = node
                            found = True
                        elif node.state.tables[i][j] < best.state.tables[i][j]:
                            found = True #bu it is not a better node
        current = best
        best = None
        current_value = problem.value(current.state)
        #print("current = %s; p = %s; pp = %s; ppp = %s", problem.value(current.state), previous, previous_previous, previous_previous_previous)
        if previous_previous_previous is not None and previous_previous_previous == previous and current_value == previous_previous:
            break; #we iterate over the same values over and over so just break here
        previous_previous_previous = previous_previous
        previous_previous = previous
        previous = current_value
    return current

def greedy(problem):
     s = int(problem.n / problem.t)
     assigned_person = [0] * problem.n
     for table in problem.tables:
         seat = 0
         alone_people = find_allow_person(assigned_person)
         if alone_people == -1:
             print("Error : everyone is at the table ")
         table[seat] = alone_people
         seat += 1
         assigned_person[alone_people] = 1
         available_friends = get_potential_new_friends(alone_people, assigned_person, problem.a)
         available_friends.sort(key = greedy_comp, reverse=True)
         for x in range(0,s-1):
             friend = available_friends[x]
             table[seat]  = friend[0]
             seat += 1
             assigned_person[friend[0]] = 1

def find_allow_person(list):
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
    start_time = time.time()
    wedding = Wedding(sys.argv[1])
    greedy(wedding)
    print(wedding.value(wedding.initial))
    print(wedding.initial)

    # node = randomized_maxvalue(wedding, 100)
    node = maxvalue(wedding, 100)

    state = node.state
    print(wedding.value(state))
    print(state)
    total_time = time.time() - start_time
    print(total_time)
