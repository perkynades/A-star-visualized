from Node import Node
import pygame
from queue import PriorityQueue

from Map import Map_Obj

# The code is inspired by this "Coding train" challenge for the A* algorithm done in javascript
# https://github.com/CodingTrain/website/tree/main/CodingChallenges/CC_051_astar/P5

width = 564
heigth = 468

current_map = 3

window = pygame.display.set_mode((heigth, width))
window.fill((255, 255, 255))


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


def draw(win, grid):
    win.fill((255, 255, 255))

    for row in grid:
        for spot in row:
            spot.draw(win)

    pygame.display.update()


def calc_h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def backtrack(path, draw):
    for current in path:
        current.make_path()
        draw()


def algorithm(draw, grid):
    open_list = PriorityQueue()

    closed_list = []

    start_position = Map_Obj(current_map).get_start_pos()
    start_node: Node = grid[start_position[0]][start_position[1]]

    hash_open_list = []

    end_position = Map_Obj(current_map).get_end_goal_pos()
    end_node: Node = grid[end_position[0]][end_position[1]]

    open_list.put((start_node.f, start_node))
    hash_open_list.append(start_node)

    while not open_list.empty():
        current_node: Node = open_list.get()[1]
        hash_open_list.remove(current_node)

        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent
            return path[::-1]

        else:
            current_node.update_neighbors(grid)
            neighbors = current_node.neighbors
            for node in neighbors:
                if node not in closed_list:
                    node.g = current_node.g + node.cost
                    node.h = calc_h(
                        node.get_pos(), end_node.get_pos())
                    node.f = node.g + node.h

                    for open_node in hash_open_list:
                        if node == open_node and node.g > open_node.g:
                            continue

                    if node not in hash_open_list:
                        hash_open_list.append(node)
                        if node is not start_node and node is not end_node:
                            node.set_color((0, 255, 0))

                        node.set_parent(current_node)

                        open_list.put((node.f, node))
            draw()
    return []


def get_map_array():
    maps = Map_Obj(current_map).get_maps()
    return maps[0]


def main():
    rows = len(get_map_array())
    map_array = get_map_array()
    grid = make_grid(rows, width, map_array)
    run = True
    while run:
        draw(window, grid)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid = make_grid(rows, width, map_array)
                    path = algorithm(lambda: draw(window, grid),
                                     grid)
                    backtrack(path, lambda: draw(window, grid))

    pygame.quit()


if __name__ == "__main__":
    main()
