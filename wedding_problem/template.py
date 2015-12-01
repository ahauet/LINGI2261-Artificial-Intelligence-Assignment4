#! /usr/bin/env python3
################################################################################
#
#		Implementation of the wedding problem class
#
################################################################################
import time
from search import *
from copy import deepcopy, copy
import random


#################
# Problem class #
#################

class Wedding(Problem):
    def __init__(self, input_file):
        self.n = 0
        self.t = 0
        self.a = []
        self.read_input_file(input_file)
        self.size_table = int(self.n / self.t)
        self.tables = [[None for x in range(0, self.size_table)] for y in range(0, self.t)]
        self.initial = State(self.a, self.tables)

    def successor(self, state):
        for i in range(self.t):
            for l in range(self.size_table):
                for j in range(i + 1, self.t):
                    if i != j:
                        for k in range(0, self.size_table):
                            #copy swappable tables
                            new_table_i = copy(state.tables[i])
                            new_table_j = copy(state.tables[j])
                            new_tables = copy(state.tables)
                            #swap
                            new_table_i[l] = state.tables[j][k]
                            new_table_j[k] = state.tables[i][l]
                            #update tables
                            new_tables[i] = new_table_i
                            new_tables[j] = new_table_j
                            #sort guest inside table
                            new_table_i.sort()
                            new_table_j.sort()
                            #new state
                            new_state = State(self.a, new_tables)
                            #yield result
                            yield ((i, l, j, k), new_state)

    def value(self, state):
        val = 0
        for i in range(self.t):
            for k in range(self.size_table):
                for l in range(self.size_table):
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
    def __init__(self, m, tables):
        self.m = m
        self.tables = tables
        #self.sort_tables()

    def sort_tables(self):
        if self.tables[0][0] is not None:
            for table in self.tables:
                table.sort()

    def __str__(self):
        output = ""
        for i in range(0, len(self.tables)):
            # self.tables[i].sort()
            for j in range(0, len(self.tables[0])):
                output += str(self.tables[i][j]) + ' '
            if i < len(self.tables) - 1:
                output += '\n'
        return output




################
# Local Search #
################

random.seed(42)

def bestRandomNeighbor(state):
    best = None
    neighbors = list(state.expand())
    neighbors.sort(reverse=True)
    neighbors = neighbors[:5] #take the 5 best elements
    index_to_take = random.randint(0,4)
    neighbor = neighbors[index_to_take]
    return neighbor
    # if best is None:
    #     best = neighbor
    # elif neighbor.value() > best.value():
    #     best = neighbor
    # elif neighbor.value() == best.value():
    #     neighbor_concat = concat(neighbor.state)
    #     best_concat = concat(best.state)
    #     if neighbor_concat <= best_concat:
    #         best = neighbor
    #         # best = compare_same_value_state(neighbor, best)
    # return best

def random_max(node):
    return node.value()

class LSNodeCustom:
    """A node in a local search. You will not need to subclass this class
        for local search."""

    def __init__(self, problem, state, step):
        """Create a local search Node."""
        self.problem = problem
        self.state = state
        self.step = step
        self._value = None

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def value(self):
        """Returns the value of the state contained in this node."""
        if self._value is None:
            self._value = self.problem.value(self.state)
        return self._value

    def expand(self):
        """Yields nodes reachable from this node. [Fig. 3.8]"""
        for (act, next) in self.problem.successor(self.state):
            yield LSNodeCustom(self.problem, next, self.step + 1)

    def __lt__(self, other):
        if self.value() < other.value():
            return True
        elif self.value() > other.value():
            return False
        else:
            return concat(self.state) < concat(other.state)

def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNodeCustom(problem, problem.initial, 0)
    best_ever = current
    previous = None
    previous_previous = None
    previous_previous_previous = None
    for step in range(limit):
        if callback is not None:
            callback(current)
        current = bestRandomNeighbor(current)
        current_value = problem.value(current.state)
        if current_value > problem.value(best_ever.state):
            best_ever = current
        if previous_previous_previous is not None and previous_previous_previous == previous and current_value == previous_previous:
            break;  # we iterate over the same values over and over so just break here
        previous_previous_previous = previous_previous
        previous_previous = previous
        previous = current_value

    return best_ever


def concat(state):
    result = ''
    for i in range(len(state.tables)):
        for j in range(len(state.tables[i])):
            result += str(state.tables[i][j])
    return result


def compare_same_value_state(neighbor, best):
    for i in range(len(neighbor.state.tables)):
        for j in range(len(neighbor.state.tables[i])):
            if neighbor.state.tables[i][j] < best.state.tables[i][j]:
                return neighbor
            elif neighbor.state.tables[i][j] > best.state.tables[i][j]:
                return best
    return best


def bestNeighbor(state):
    best = None
    for neighbor in list(state.expand()):
        if best is None:
            best = neighbor
        elif neighbor.value() > best.value():
            best = neighbor
        elif neighbor.value() == best.value():
            neighbor_concat = concat(neighbor.state)
            best_concat = concat(best.state)
            if neighbor_concat <= best_concat:
                best = neighbor
                # best = compare_same_value_state(neighbor, best)
    return best


def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best_ever = current
    previous = None
    previous_previous = None
    previous_previous_previous = None
    for step in range(limit):
        if callback is not None:
            callback(current)
        current = bestNeighbor(current)
        current_value = problem.value(current.state)
        if current_value > problem.value(best_ever.state):
            best_ever = current
        if previous_previous_previous is not None and previous_previous_previous == previous and current_value == previous_previous:
            break;  # we iterate over the same values over and over so just break here
        previous_previous_previous = previous_previous
        previous_previous = previous
        previous = current_value

    return best_ever


def greedy(problem):
    s = int(problem.n / problem.t)
    assigned_person = [0] * problem.n
    for table in problem.tables:
        seat = 0
        alone_people = find_alone_person(assigned_person)
        if alone_people == -1:
            print("Error : everyone is at the table ")
        table[seat] = alone_people
        seat += 1
        assigned_person[alone_people] = 1
        available_friends = get_potential_new_friends(alone_people, assigned_person, problem.a)
        available_friends.sort(key=greedy_comp, reverse=True)
        for x in range(0, s - 1):
            friend = available_friends[x]
            table[seat] = friend[0]
            seat += 1
            assigned_person[friend[0]] = 1
    problem.initial.sort_tables()

def find_alone_person(list):
    for x in range(0, len(list)):
        if list[x] == 0:
            return x
    return -1


def get_potential_new_friends(seeker, assigned_person, friendship_table):
    result = []
    for x in range(seeker + 1, len(assigned_person)):
        if assigned_person[x] == 0:
            result.append((x, friendship_table[seeker][x]))
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
    # print(total_time)
