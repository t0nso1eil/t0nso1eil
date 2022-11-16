import random
import time
import typing as tp

import pygame
from pygame import QUIT
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
            time.sleep(0.3)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [
                [random.randint(0, 1) for i in range(0, self.cell_height)]
                for j in range(0, self.cell_width)
            ]
        else:
            return [[0 for i in range(0, self.cell_height)] for j in range(0, self.cell_width)]

    def draw_grid(self) -> None:
        for i in range(0, self.cell_width):
            for j in range(0, self.cell_height):
                temp = self.grid[i][j]
                if temp:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                temprect = pygame.Rect(
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, temprect)

    def get_neighbours(self, cell: Cell) -> Cells:
        i, j = cell
        nears = (
            (i, j - 1),
            (i - 1, j),
            (i, j + 1),
            (i + 1, j),
            (i - 1, j - 1),
            (i - 1, j + 1),
            (i + 1, j - 1),
            (i + 1, j + 1),
        )
        poss = []
        for a, b in nears:
            if a >= 0 and b >= 0 and a < len(self.grid) and b < len(self.grid[0]):
                poss += [self.grid[a][b]]
        return poss

    def get_next_generation(self) -> Grid:
        grid = [[0] * len(self.grid[0]) for i in range(len(self.grid))]
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                n = self.get_neighbours((i, j)).count(1)
                if (self.grid[i][j] == 1 and (n == 2 or n == 3)) or (
                    self.grid[i][j] == 0 and n == 3
                ):
                    grid[i][j] = 1
        return grid


if __name__ == "__main__":
    game = GameOfLife(320 * 3, 240 * 3, 10, 100)
    game.run()
