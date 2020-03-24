import random
from typing import List

from lib import Direction

# Note: 0 is blank


class Puzzle:
    n: int = 1
    mat: List[int]

    def __init__(self, n: int, mat: List[int] = None):
        if (n >= 100 or n <= 0):
            raise ValueError("N is not valid.")
        self.n = n
        if mat is None:
            self.mat = Puzzle.getFinishedMatrix(n)
        else:
            self.mat = mat.copy()

    def __key(self):
        return tuple(self.mat)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Puzzle):
            return self.__key() == other.__key()
        return False

    def __lt__(self, other):
        return True

    def __repr__(self):
        rep = self._reprTop()
        for i in range(self.n):
            rep += self._reprNumbers(i)
            if (i < self.n - 1):
                rep += self._reprSeparator()
        return rep + self._reprBot()

    def copy(self):
        return Puzzle(self.n, self.mat)

    def shuffle(self):
        random.shuffle(self.mat)

    def rangedShuffle(self, x: int):
        dirList = list(Direction)
        for _ in range(x):
            try:
                self.move(dirList[random.randint(0, 3)])
            except:
                pass

    def _reprTop(self) -> str:
        res = "╔══"
        for _ in range(self.n-1):
            res += "╦══"
        return res + "╗\n"

    def _reprNumber(self, num: int) -> str:
        res = ""
        if num < 10:
            res += " "
        return res + " " if num == 0 else res + str(num)

    def _reprNumbers(self, row: int) -> str:
        res = "║"
        for i in range(self.n):
            res += self._reprNumber(self.mat[row * self.n + i])
            res += "║"
        return res + "\n"

    def _reprSeparator(self) -> str:
        res = "╠══"
        for _ in range(self.n-1):
            res += "╬══"
        return res + "╣\n"

    def _reprBot(self) -> str:
        res = "╚══"
        for _ in range(self.n-1):
            res += "╩══"
        return res + "╝"

    def print(self):
        print(self)

    def _swap(self, i: int, j: int):
        self.mat[i], self.mat[j] = self.mat[j], self.mat[i]

    def move(self, dir: Direction):
        if not self.isValidToMove(dir):
            raise MoveError(dir)
        i = self.mat.index(0)
        if dir == Direction.UP:
            j = i - self.n
        elif dir == Direction.RIGHT:
            j = i + 1
        elif dir == Direction.DOWN:
            j = i + self.n
        elif dir == Direction.LEFT:
            j = i - 1
        else:
            raise RuntimeError("Huh?")
        self._swap(i, j)

    def isValidToMove(self, dir: Direction) -> bool:
        i = self.mat.index(0)
        return dir == Direction.UP and i >= self.n \
            or dir == Direction.RIGHT and i % self.n < self.n - 1 \
            or dir == Direction.DOWN and i < self.n*(self.n-1) \
            or dir == Direction.LEFT and i % self.n > 0

    def kurang(self, v: int) -> int:
        res = 0
        pos = self.mat.index(v % self.n**2)
        for i in range(pos + 1, self.n**2):
            if self.mat[i] < v and self.mat[i] != 0:
                res += 1
        return res

    def sigmaKurang(self, v: int = None) -> int:
        if v is None:
            return self.sigmaKurang(self.n**2)
        if v == 1:
            return 0
        return self.kurang(v) + self.sigmaKurang(v - 1)

    def X(self):
        pos = self.mat.index(0)
        return 1 if (pos//self.n + pos % self.n) % 2 == 1 else 0

    def sigmaKurangX(self) -> int:
        return self.X() + self.sigmaKurang()

    def isSolvable(self) -> bool:
        return self.sigmaKurangX() % 2 == 0

    def cost(self, x: int) -> int:
        count = 0
        for i, v in enumerate(self.mat):
            if v != i + 1 and v != 0:
                count += 1
        return x + count

    def isGoal(self):
        return Puzzle.getFinishedMatrix(self.n) == self.mat

    @staticmethod
    def getFinishedMatrix(n: int):
        return list(range(1, n**2)) + [0]


class MoveError(RuntimeError):
    def __init__(self, dir: Direction):
        super().__init__("Can't move to " + dir.name)
