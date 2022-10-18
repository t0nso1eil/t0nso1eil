import math
import pathlib
import typing as tp
from random import randint, random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """Сгруппировать значения values в список, состоящий из списков по n элементов"""
    arr = []
    for i in range(n):
        arr.append(values[i * n : (i + 1) * n])
    return arr


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos"""
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos"""
    arr = []
    for i in range(0, len(grid)):
        arr.append(grid[i][pos[1]])
    return arr


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos"""
    arr = []
    t = int(math.sqrt(len(grid)))
    for i in range(0, t):
        for j in range(0, t):
            arr.append(grid[i + t * (pos[0] // t)][j + t * (pos[1] // t)])
    return arr


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле"""
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == ".":
                return i, j
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    base = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    res = set()
    for i in base:
        if (
            (i not in set(get_col(grid, pos)))
            and (i not in set(get_row(grid, pos)))
            and (i not in set(get_block(grid, pos)))
        ):
            res.add(i)
    return res


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    def solvee(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
        """Решение пазла, заданного в grid"""
        """ Как решать Судоку?
            1. Найти свободную позицию
            2. Найти все возможные значения, которые могут находиться на этой позиции
            3. Для каждого возможного значения:
                3.1. Поместить это значение на эту позицию
                3.2. Продолжить решать оставшуюся часть пазла
        """
        pos = find_empty_positions(grid)
        if pos == None:
            return grid
        else:
            t = find_possible_values(grid, pos)
            if t == None:
                return grid
            else:
                for i in t:
                    temp = grid[pos[0]][pos[1]]
                    grid[pos[0]][pos[1]] = str(i)
                    grid = solve(grid)
                    if find_empty_positions(grid) == None:
                        return grid
                    grid[pos[0]][pos[1]] = temp
            return grid
        return None
    return solvee(grid)


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    pos = find_empty_positions(grid)
    if pos != None:
        return False
    for i in range(0, len(solution)):
        for j in range(0, len(solution)):
            pos = (i, j)
            if (
                not (get_col(solution, pos).count(solution[i][j]) == 1)
                or not (get_row(solution, pos).count(solution[i][j]) == 1)
                or not (get_block(solution, pos).count(solution[i][j]) == 1)
            ):
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов"""
    grid = [["." for i in range(0, 9)] for j in range(0, 9)]
    grid = solve(grid)
    display(grid)
    for k in range(0, 81 - N):
        i = randint(0, 8)
        j = randint(0, 8)
        while grid[i][j] == ".":
            i = randint(0, 8)
            j = randint(0, 8)
        grid[i][j] = "."
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
