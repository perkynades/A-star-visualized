import pygame


class Node:
    def __init__(self, row, column, width, rows):
        self.row = row
        self.column = column
        self.x = column * width
        self.y = row * width
        self.color = (255, 255, 255)
        self.width = width
        self.rows = rows

        self.parent = None
        self.neighbors = []

        self.g = 0
        self.f = 0
        self.h = 0

        self.cost = 1

    def set_color(self, colorToSet):
        self.color = colorToSet

    def set_parent(self, parentToSet):
        self.parent = parentToSet

    def get_parent(self):
        return self.parent

    def draw(self, window):
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.width, self.width))

    def get_pos(self):
        return [self.row, self.column]

    def is_node_wall(self):
        return self.color == (255, 0, 0)

    def make_wall(self):
        self.color = (255, 0, 0)

    def make_path(self):
        self.color = (221, 160, 221)

    def update_neighbors(self, grid):
        self.neighbors = []

        neighbor_up: Node = grid[self.row - 1][self.column]
        neighbor_down: Node = grid[self.row + 1][self.column]
        neighbor_right: Node = grid[self.row][self.column + 1]
        neighbor_left: Node = grid[self.row][self.column - 1]

        if self.row > 0 and not neighbor_up.is_node_wall():
            self.neighbors.append(neighbor_up)

        if self.row < self.rows - 1 and not neighbor_down.is_node_wall():
            self.neighbors.append(neighbor_down)

        if self.column < self.rows - 1 and not neighbor_right.is_node_wall():
            self.neighbors.append(neighbor_right)

        if self.column > 0 and not neighbor_left.is_node_wall():
            self.neighbors.append(neighbor_left)

    def __lt__(self, other):
        return False
