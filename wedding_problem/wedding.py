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


###################
#  PriorityQueue  #
###################
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        if self._index >= 5:
            heapq.heappop(self._queue)[-1]
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


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

random.seed(42)

def randomized_maxvalue(problem, limit=100, callback=None):
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
            break;  # we iterate over the same values over and over so just break here
        previous_previous_previous = previous_previous
        previous_previous = previous
        previous = current_value
    return best


def best_five_neighbors(state):
    bests = PriorityQueue
    for neighbor in list(state.expand()):
        if bests._index == 0:
            bests.push(neighbor, neighbor.state.value)
        elif neighbor.state.value > bests.state.value:
            bests.push(neighbor, neighbor.state.value)
        elif neighbor.state.value == bests.state.value:
            if neighbor.state.tables < bests.state.tables:
                bests.push(neighbor, neighbor.state.value)
    return bests


def randomly_neighbors(state):
    bests = best_five_neighbors(state)
    index = random.randint(0, 4)
    return bests._queue[index]


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
