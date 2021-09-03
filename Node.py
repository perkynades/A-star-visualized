import numpy as np


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def return_path(current_node, map):
        path = []
        no_rows, no_colums = np.shape(map)

        result = [[-1 for i in range(no_colums)] for j in range(no_rows)]

        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent

        path = path[::-1]
        start_value = 0

        for i in range(len(path)):
            result[path[i][0]][path[i][1]] = start_value
            start_value += 1

        return result

    def search(self, map, cost, start, end):
        start_node = Node(None, tuple(start))
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, tuple(end))
        end_node.g = end_node.h = start_node.f = 0

        yet_to_visit_list = []
        visited_list = []
        yet_to_visit_list.append(start_node)

        outer_iterations = 0
        max_iterations = (len(map) // 2) ** 10

        move = [[-1, 0],
                [0, -1],
                [1, 0],
                [0, 1]]

        no_rows, no_colums = np.shape(map)

        while len(yet_to_visit_list) > 0:
            outer_iterations += 1

            current_node = yet_to_visit_list[0]
            current_index = 0
            for index, item in enumerate(yet_to_visit_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            if outer_iterations > max_iterations:
                print("too many iterations")
                return self.return_path(current_node, map)

            yet_to_visit_list.pop(current_index)
            visited_list.append(current_node)

            if current_node == end_node:
                return self.return_path(current_node, map)
