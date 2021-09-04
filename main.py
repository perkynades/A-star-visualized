from Node import Node
import pygame
from queue import PriorityQueue

from Map import Map_Obj

# The code is inspired by this "Coding train" challenge for the A* algorithm done in javascript
# https://github.com/CodingTrain/website/tree/main/CodingChallenges/CC_051_astar/P5

width = 564
heigth = 468
current_map = 1

window = pygame.display.set_mode((heigth, width))
window.fill((255, 255, 255))


def remove_green_color(grid):
    for array in grid:
        for node in array:
            if node.color == (0, 255, 0):
                if node.cost == 1:
                    node.set_color((255, 255, 255))
                elif node.cost == 2:
                    node.set_color((128, 128, 128))
                elif node.cost == 3:
                    node.set_color((169, 169, 169))
                elif node.cost == 4:
                    node.set_color((0, 0, 0))


def make_grid(rows: int, width: int, map_array):
    grid = []
    gap = (width // rows)
    for i in range(rows):
        grid.append([])
        map_list = map_array[i]
        for j in range(len(map_list)):
            list_value = map_list[j]
            if list_value == 1:
                node = Node(i, j, gap, rows)
            elif list_value == -1:
                node = Node(i, j, gap, rows)
                node.make_wall()
            elif list_value == 2:
                node = Node(i, j, gap, rows)
                node.set_color((128, 128, 128))
            elif list_value == 3:
                node = Node(i, j, gap, rows)
                node.set_color((169, 169, 169))
            elif list_value == 4:
                node = Node(i, j, gap, rows)
                node.set_color((0, 0, 0))
            node.cost = list_value
            grid[i].append(node)

    start_position = Map_Obj(current_map).get_start_pos()
    start_node: Node = grid[start_position[0]][start_position[1]]
    start_node.set_color((255, 130, 185))

    end_position = Map_Obj(current_map).get_end_goal_pos()
    end_node: Node = grid[end_position[0]][end_position[1]]
    end_node.set_color((255, 165, 0))

    return grid


def draw_grid(win, rows, columns, width):
    gap = (width // rows)
    for i in range(rows):
        pygame.draw.line(win, (128, 128, 128), (0, i * gap), (width, i * gap))
        for j in range(columns):
            pygame.draw.line(win, (128, 128, 128),
                             (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, columns, width):
    win.fill((255, 255, 255))  # Sets the background of the window to white.

    # Draws the lines in the pygame window.
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, columns, width)
    pygame.display.update()


def calculate_h_value(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def backtrack(path, draw):
    for current in path:
        current.make_path()
        draw()


def algorithm(draw, grid):
    # The list with the open nodes.
    # Uses a priority queue to retrieve the nodes with the lowest f value.
    open_list = PriorityQueue()

    # The list with the closed nodes
    # todo can be made a hash with positions for better efficiency??
    closed_list = []

    # The start square
    start_position = Map_Obj(current_map).get_start_pos()
    start_node: Node = grid[start_position[0]][start_position[1]]

    # todo check the run time of append and remove for lists in python
    hash_open_list = []

    # The end square
    end_position = Map_Obj(current_map).get_end_goal_pos()
    end_node: Node = grid[end_position[0]][end_position[1]]

    # Puts the start square in the open list.
    open_list.put((start_node.f_value, start_node))
    hash_open_list.append(start_node)

    while not open_list.empty():
        # The list is sorted by the lowest f value. The get removes the square from the Priority Queue.
        current_node: Node = open_list.get()[1]
        hash_open_list.remove(current_node)

        # Adds the current square to the closed list.
        closed_list.append(current_node)

        # If the current square equals the goal square,
        # we save the path and creates the path in the pygame
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                # current.make_path()
                path.append(current)
                current = current.parent
                # draw()
            return path[::-1]  # Return reversed path

        else:
            # Updates the neighbors of the current square
            current_node.update_neighbors(grid)
            neighbors = current_node.neighbors
            for node in neighbors:
                if node not in closed_list:
                    # Update the g, h, and f values
                    node.g_value = current_node.g_value + node.cost
                    node.h_value = calculate_h_value(
                        node.get_pos(), end_node.get_pos())
                    node.f_value = node.g_value + node.h_value

                    # If the square equals a square in the open list and the g value is more we continue
                    # with the next iteration of the for-loop
                    for open_node in hash_open_list:
                        if node == open_node and node.g_value > open_node.g_value:
                            continue
                    # If the square is not in the open list, we add it and change the color of it in the pygame window.
                    if node not in hash_open_list:
                        hash_open_list.append(node)
                        if node is not start_node and node is not end_node:
                            node.set_color((0, 255, 0))

                        # Sets the parent of the square. This enables backtracking.
                        node.set_parent(current_node)

                        open_list.put((node.f_value, node))
            draw()
    return []


def get_map_array():
    maps = Map_Obj(current_map).get_maps()
    return maps[0]


def main():
    rows = len(get_map_array())  # gets the amount of rows
    columns = len(get_map_array()[0])  # Gets the amount of columns
    map_array = get_map_array()  # Gets the 2D array of the map
    grid = make_grid(rows, width, map_array)  # Creates the grid
    run = True
    while run:
        draw(window, grid, rows, columns, width)

        # Handles the events in pygame
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Clears the grid if the code ran before.
                    grid = make_grid(rows, width, map_array)
                    path = algorithm(lambda: draw(window, grid, rows, columns, width),
                                     grid)  # returns the path from algorithm
                    remove_green_color(grid)
                    backtrack(path, lambda: draw(window, grid, rows,
                              columns, width))  # Draws the path

    pygame.quit()


if __name__ == "__main__":
    main()
