import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
LIGTH_PURPLE = (221, 160, 221)


class MapGrid:
    def __init__(self, row, column, width, rows):
        self.row = row
        self.column = column
        self.x = column * width
        self.y = row * width
        self.color = WHITE
        self.width = width
        self.rows = rows

        self.parent = None
        self.neighbors = []

        self.g_value = 0  # The g-value of the square.
        self.f_value = 0  # The f-value of the square.
        self.h_value = 0  # THe h-value of the square.

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

    def is_map_grid_wall(self):
        return self.color == RED

    def make_wall(self):
        self.color = RED

    def make_path(self):
        self.color = LIGTH_PURPLE

    def update_neighbors(self, grid):
        self.neighbors = []

        neighbor_up: MapGrid = grid[self.row - 1][self.column]
        neighbor_down: MapGrid = grid[self.row + 1][self.column]
        neighbor_right: MapGrid = grid[self.row][self.column + 1]
        neighbor_left: MapGrid = grid[self.row][self.column - 1]

        if self.row > 0 and not neighbor_up.is_map_grid_wall():
            self.neighbors.append(neighbor_up)

        if self.row < self.rows - 1 and not neighbor_down.is_map_grid_wall():
            self.neighbors.append(neighbor_down)

        if self.column < self.rows - 1 and not neighbor_right.is_map_grid_wall():
            self.neighbors.append(neighbor_right)

        if self.column > 0 and not neighbor_left.is_map_grid_wall():
            self.neighbors.append(neighbor_left)

    def __lt__(self, other):
        return False
