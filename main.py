import os
import random
import time
from queue import PriorityQueue
from typing import List, Set, Tuple

from lib import Direction, out
from puzzle import MoveError
from puzzle15 import Puzzle15


def bnb(p: Puzzle15) -> Tuple[List[Puzzle15], int]:
    n = 1
    # implement branch and bound
    done: Set[Puzzle15] = set()
    q: PriorityQueue = PriorityQueue()
    q.put((p.cost(0), list(), p))
    done.add(p)
    while not q.empty():
        _, path, now = q.get()

        # os.system("cls")
        # print(now)
        # print(_)
        # time.sleep(0.05)

        if (now.isGoal()):
            return [p] + path, n
        for dir in Direction:
            try:
                next = now.copy()
                next.move(dir)
                if next not in done:
                    n += 1
                    done.add(next)
                    nextPath = path + [next]
                    q.put((next.cost(len(nextPath)),
                           nextPath, next))
            except MoveError:
                pass
    raise Exception("Huh?")


def do_the_job(p: Puzzle15):
    p.print()

    print()
    print("i: KURANG(i)")
    for i in range(1, p.n**2+1):
        print(f"{i}: {p.kurang(i)}")

    print()
    print(f"X: {p.X()}")
    print(f"Σ(KURANG(i)) + X: {p.sigmaKurangX()}")

    print()
    solvable = p.isSolvable()
    print(f"Solvable: {solvable}")

    if not solvable:
        exit()

    elapsedTime = time.time()
    l, createdVertices = bnb(p)
    elapsedTime = time.time() - elapsedTime
    for i, m in enumerate(l):
        if i > 0:
            print(f"{i}     🡫")
        m.print()

    print(f"Time elapsed: {elapsedTime*1000} ms.")
    print(f"Total steps: {len(l) - 1}")
    print(f"Total created vertices: {createdVertices}")


if __name__ == "__main__":
    out("Masukkan nama file: ")
    f = open(input(), "r+")
    l: List[int] = list()
    for line in f.readlines():
        l += [0 if int(v) == 16 else int(v) for v in line.split(" ")]
    f.close()
    p = Puzzle15(l)
    p.rangedShuffle(random.randint(40, 60))
    do_the_job(p)
