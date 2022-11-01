import pathlib
import random
import typing as tp


Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for i in range(0, self.rows)] for j in range(0, self.cols)]
        else:
            return [[0 for i in range(0, self.rows)] for j in range(0, self.cols)]

    def get_neighbours(self, cell: Cell) -> Cells:
        i, j = cell
        nears = (
        (i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1))
        poss = []
        for a, b in nears:
            if a >= 0 and b >= 0 and a < len(self.curr_generation) and b < len(self.curr_generation[0]):
                poss += [self.curr_generation[a][b]]
        return poss

    def get_next_generation(self) -> Grid:
        grid = [[0] * len(self.curr_generation[0]) for i in range(len(self.curr_generation))]
        for i in range(0,len(self.curr_generation)):
            for j in range(0,len(self.curr_generation[0])):
                n = self.get_neighbours((i, j)).count(1)
                if self.curr_generation[i][j] and n == 2 or n == 3:
                    grid[i][j] = 1
        return grid

    def step(self) -> None:
        if self.is_changing and self.is_max_generations_exceeded==False:
            self.prev_generation = self.curr_generation.copy()
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations is None:
            self.max_generations=1
        if self.generations>=self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        f=open(filename)
        grid=[]
        lines=f.readlines()
        height=0
        width=0
        for i in range(0,len(lines)):
            if lines[i]!='\n':
                temp=lines[i][:-1]
                height += 1
                width = len(temp)
                grid.append([])
                for j in range(0, len(temp)):
                    grid[len(grid) - 1].append(int(temp[j]))
        game = GameOfLife((height, width))
        game.curr_generation = grid
        f.close()
        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as f:
            for i in self.curr_generation:
                print(i, sep="", file=f)
