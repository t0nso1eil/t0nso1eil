import time

import pygame
from pygame.locals import *

from homework03.life import GameOfLife
from homework03.ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.cell_size * self.life.rows
        self.height = self.cell_size * self.life.cols
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        for i in range(0, self.life.cols):
            for j in range(0, self.life.rows):
                temp = self.life.curr_generation[i][j]
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

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.life.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
