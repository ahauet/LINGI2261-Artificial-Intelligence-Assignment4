#! /usr/bin/env python3
################################################################################
#
#		Implementation of the wedding problem class
#
################################################################################
import time
from copy import copy
from search import *
import heapq
import random
import queue


##############
# MyLSNODE  #
#############
class MyLSNODE():
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
            yield MyLSNODE(self.problem, next, self.step + 1)
    #
    # def __lt__(self, other):
    #     return self.cmp_LSNodeCustom(self, other) < 0
    #
    # def __gt__(self, other):
    #     return self.cmp_LSNodeCustom(self, other) > 0
    #
    #
    # def __eq__(self, other):
    #     return self.cmp_LSNodeCustom(self, other) == 0
    #
    # def __le__(self, other):
    #     return self.cmp_LSNodeCustom(self, other) <= 0
    #
    # def __ge__(self, other):
    #     return self.cmp_LSNodeCustom(self, other) >= 0
    #
    # def __ne__(self, other):
    #     return (self, other) != 0

def cmp_LSNodeCustom(first, other):
    if first.state.value < other.state.value: return -1
    elif first.state.value > other.state.value: return 1
    else:
        if first.state.tables < other.state.tables:
            return 1
        else:
            return -1


#################
# Problem class #
#################

class Wedding(Problem):
    def __init__(self, init_file):
        self.n = 0  # Number of guests
        self.t = 0  # Number of tables
        self.a = []  # Affinity persons
        self.tables = []  # Tables
        self.init_from_file(init_file)  # Initialize problem
        self.size_table = int(self.n / self.t)  # Number of person by table
        self.initial = State(self.n, self.t, self.a, self.tables, 0)

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
                for k in range(i + 1, self.t):
                    for l in range(0, self.size_table):
                        new_table_i = copy(state.tables[i])
                        new_table_k = copy(state.tables[k])
                        new_tables = copy(state.tables)
                        new_table_i[j] = state.tables[k][l]
                        new_table_k[l] = state.tables[i][j]
                        new_table_i.sort()
                        new_table_k.sort()
                        new_tables[i] = new_table_i
                        new_tables[k] = new_table_k
                        old_values = self.value_for_row(i, state.tables, state.a) + self.value_for_row(k, state.tables,
                                                                                                       state.a)
                        new_values = self.value_for_row(i, new_tables, state.a) + self.value_for_row(k, new_tables,
                                                                                                     state.a)
                        new_state = State(state.n, state.t, state.a, new_tables, state.value - old_values + new_values)
                        yield ((i, j, k, l), new_state)

    def value_for_row(self, table_num, tables, a):
        result = 0
        for j in range(len(tables[table_num])):
            for i in range(len(tables[table_num])):
                result += a[tables[table_num][i]][tables[table_num][j]]
        return result

    def value(self, state):
        return state.val

###############
# State class #
###############

class State:
    def __init__(self, n, t, a, tables, value):
        self.n = n
        self.t = t
        self.a = a
        self.tables = tables
        self.value = value

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

    def find_value(self, tables, a):
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
    random.seed(42)
    current = LSNode(problem, problem.initial, 0)
    best = current
    # previous = None
    # previous_previous = None
    # previous_previous_previous = None
    for step in range(limit):
        if callback is not None:
            callback(current)
        current = randomly_neighbors(current)
        current_value = current.state.value
        if current_value > best.state.value:
            best = current
        # if previous_previous_previous is not None and previous_previous_previous == previous and current_value == previous_previous:
        #     break;  # we iterate over the same values over and over so just break here
        # previous_previous_previous = previous_previous
        # previous_previous = previous
        # previous = current_value
    return best

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'

    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K

def best_five_neighbors(state):
    # bests = queue.PriorityQueue()
    # for neighbor in list(state.expand()):
    #     bests.put(neighbor)
    bests = list(state.expand())
    bests.sort(key=cmp_to_key(cmp_LSNodeCustom), reverse=True)
    bests = bests[:5]
    return bests


def randomly_neighbors(state):
    bests = best_five_neighbors(state)
    index = random.randint(0, 4)
    return bests[index]


def concat(state):
    result = ''
    for i in range(0, len(state.tables)):
        for j in range(0, len(state.tables[i])):
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
            # neighbor_concat = concat(neighbor.state)
            # best_concat = concat(best.state)
            # if neighbor_concat < best_concat:
            # best = neighbor
            if neighbor.state.tables < best.state.tables:
                best = neighbor
    return best


def maxvalue(problem, limit=100, callback=None):
    current =   MyLSNODE(problem, problem.initial, 0)
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
            break;  # we iterate over the same values over and over so just break here
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
        available_friends.sort(key=greedy_comp, reverse=True)
        for x in range(0, s - 1):
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
    wedding.initial.set_value()
    print(wedding.initial.value)
    print(wedding.initial)
    node = randomized_maxvalue(wedding, 100)
    # node = maxvalue(wedding, 100)

    state = node.state
    print(node.state.value)
    print(state)
    total_time = time.time() - start_time
