import curses
import time

from homework03.life import GameOfLife
from homework03.ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.game = life

    def draw_borders(self, screen) -> None:
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        for i in range(0, self.life.rows):
            for j in range(0, self.life.cols):
                screen.move(i + 1, j + 1)
                if self.life.curr_generation[j][i] == 1:
                    screen.addch("*")
                else:
                    screen.addch(" ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.resize_term(self.life.rows + 5, self.life.cols + 5)
        running = True
        while running:
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            time.sleep(0.2)
            screen.refresh()
        curses.edwin()
