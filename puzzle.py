#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Puzzle 15 Module

For use with the branch and bound algorithm
with offset-tile heuristic.

Notes
-----
This module can be called directly to demonstrate
a randomly generated Puzzle 15 problem.
"""
from __future__ import annotations
from typing import Callable, TypeVar
from enum import Enum
import random
import re
import sys


T = TypeVar('T')


class Move(Enum):
    """Enum of possible moves within the Puzzle 15

    Movement is denoted by the direction in which the
    "null tile" moves. e.g. UP means the null tile
    moves up.
    """
    UP = 'Up'
    RIGHT = 'Right'
    DOWN = 'Down'
    LEFT = 'Left'


class Puzzle:
    """Puzzle 15 Class

    Class to represent Puzzle 15, mainly for use with the
    Branch and Bound Algorithm with the simple heuristic of
    counting the number of offset tiles.

    Notes
    -----

    The class provides the attributes and methods needed to perform
    such algorithm. Mainly through the attribute history and
    the method cost(). The class also provides comparison
    overloading, for use within a prio-queue.

    Reference:
    `R. Munir et al <https://informatika.stei.itb.ac.id/~rinaldi.munir/Stmik/2020-2021/Algoritma-Branch-and-Bound-2021-Bagian1.pdf>`

    This class is also flexible in which it can accomodate
    variable-size puzzles (not just 4x4 Puzzle 15). It can
    also be used with custom tile names (not just int).

    Hence, the name of the class is not Puzzle 15. But the cost
    of flexibility (and code clarity) is speed. So compared to
    fixed-size problem-specific structures, this class is
    slower by approximately two or three times.

    Parameters
    ----------
    grid: list of list of T, default None
        A 2D array of the starting state of the puzzle.
        If unspecified will randomize the position of tiles.
    goal: list of list of T, default None
        A 2D array of the finished state of the puzzle. If
        unspecified will resort to sorted integer tiles with null
        tile on the bottom right.
    size: int, default None
        Size of the puzzle. Incorrectly specifying this alongside a
        bigger or smaller grid will result in unexpected errors.
        If unspecified will resort to class default (4).
    null: T, default None
        The element representing the null tile. Preferably the same type
        as other elements. If unspecified will resort to class
        default (0).

    Attributes
    ----------
    elements: list of T
        List of elements, deduced from the goal state. Readonly.
    null: T
        The element representing Null Tile. Preferably same type as
        other elements. Default is 0. Readonly.
    history: list of Move
        List of executed moves. Readonly.
    """
    _grid: list[list[T@__init__]]

    _size: int = 4

    _null: T@__init__ = 0

    _goal: list[list[T@__init__]]

    _elements: list[T@__init__]

    _history: list[Move]

    @property
    def null(self) -> T@__init__:
        return self._null

    @property
    def elements(self) -> list[T@__init__]:
        return self._elements[:]

    @property
    def history(self) -> list[Move]:
        return self._history

    def __init__(
        self,
        grid: list[list[T]] = None,
        goal: list[list[T]] = None,
        size: int = None,
        null: T = None
    ) -> None:
        """Initialize the puzzle with some sanity checks.

        Notes
        -----
        Tile elements of the puzzle is taken from the goal parameter.
        Element type must be hashable.

        Parameters
        ----------
        grid: list[list[T]]
            A 2D array of the starting state of the puzzle. Default None
            and will randomize the position of tiles.
        goal: list[list[T]]
            A 2D array of the finished state of the puzzle. Default None
            and will resort to sorted integer tiles with null tile on
            the bottom right.
        size: int
            Size of the puzzle. Incorrectly specifying this alongside a
            bigger or smaller grid will result in unexpected errors.
            Default None (will resort to 4).
        null: T
            The element representing the null tile. Preferably the same type
            as other elements. Default None (will resort to 0).
        """
        self._history = []

        if null is not None:
            self._null = null

        if grid is not None:
            self._size = len(grid)

        if size is not None:
            self._size = size

        if goal is None:
            self._goal = []
            for i in range(self._size):
                self._goal.append([])
                for j in range(self._size):
                    self._goal[i].append(i * self._size + j + 1)
            # put null element on bottom right corner
            self._goal[-1][-1] = self._null
        else:
            self._goal = [[goal[i][j]
                           for j in range(self._size)] for i in range(self._size)]

        self._elements = [x for row in self._goal for x in row]

        if len(set(self._elements)) != len(self._elements):
            raise ValueError('Puzzle goal tiles are not unique.')

        if self._null not in self._elements:
            raise ValueError('Null element not present in goal state.')

        if grid is None:
            # no grid specified, randomize
            self._grid = [[0] * self._size for _ in range(self._size)]

            els = self._elements[:]
            random.shuffle(els)

            for i in range(self._size):
                for j in range(self._size):
                    self._grid[i][j] = els.pop()
        else:
            # enforce correct size
            self._grid = [[grid[i][j]
                           for j in range(self._size)] for i in range(self._size)]

            els = [x for row in self._grid for x in row]

            if len(set(els)) != len(els):
                raise ValueError('Puzzle tiles are not unique.')

            if set(els) != set(self._elements):
                raise ValueError('Puzzle elements not present in goal state.')

    def pos(self, el: T) -> tuple[int, int]:
        """Find the position of a given element

        Parameters
        ----------
        el : T
            The element.

        Returns
        -------
        tuple[int, int]
            Tuple of index, in order of the array notation [i][j]
        """
        for i in range(self._size):
            for j in range(self._size):
                if self._grid[i][j] == el:
                    return (i, j)
        raise ValueError(f'Element {el} not found in puzzle.')

    def isMoveable(self, direction: Move):
        """Check if moving in the given direction is possible.

        Possible = will change the state of the puzzle.

        Parameters
        ----------
        direction : Move
            The direction of the move.

        Returns
        -------
        bool
        """
        i, j = self.pos(self._null)
        if direction == Move.UP and i > 0:
            return True
        elif direction == Move.DOWN and i < self._size - 1:
            return True
        elif direction == Move.LEFT and j > 0:
            return True
        elif direction == Move.RIGHT and j < self._size - 1:
            return True
        return False

    def move(self, direction: Move) -> bool:
        """Move the puzzle

        Parameters
        ----------
        direction : Move
            The direction of the move.

        Returns
        -------
        bool
            Whether the move changed the state of the puzzle.
        """
        if not self.isMoveable(direction):
            return False

        i, j = self.pos(self._null)

        if direction == Move.UP:
            self.swap((i, j), (i - 1, j))
        elif direction == Move.DOWN:
            self.swap((i, j), (i + 1, j))
        elif direction == Move.LEFT:
            self.swap((i, j), (i, j - 1))
        elif direction == Move.RIGHT:
            self.swap((i, j), (i, j + 1))

        self._history.append(direction)
        return True

    def offsetTiles(self) -> int:
        """Count the number of tiles not in position."""
        count = 0
        for i in range(self._size):
            for j in range(self._size):
                if self._grid[i][j] != self._goal[i][j] and self._grid[i][j] != self._null:
                    count += 1
        return count

    def cost(self) -> int:
        """Calculate the heuristic cost of the puzzle."""
        return len(self._history) + self.offsetTiles()

    def offset(self, el: T) -> int:
        """Calculate the "offset value" of a tile.

        Offset value of a tile i, is the number of tiles which
        is supposed to be placed after before tile i, but isn't.
        """
        stat = 0
        ii, ji = self.pos(el)
        for j in range(self._elements.index(el)):
            ij, jj = self.pos(self._elements[j])
            if (ij * self._size + jj) > (ii * self._size + ji):
                stat += 1
        return stat

    def totalOffset(self) -> int:
        """Calculate the total "offset value" of the puzzle.

        Total = Sum of offset value for all tiles + X
        With (i,j) referring to the position index of the null tile
        X = 1 if i + j is even, 0 otherwise
        """
        stat = 0
        for el in self._elements:
            stat += self.offset(el)

        inull, jnull = self.pos(self._null)
        if (inull + jnull) % 2 != 0:
            stat += 1

        return stat

    def isSolveable(self):
        return self.totalOffset() % 2 == 0

    def isSolved(self):
        return self._grid == self._goal

    def swap(self, a: tuple[int, int], b: tuple[int, int]) -> None:
        self._grid[a[0]][a[1]], self._grid[b[0]][b[1]
                                                 ] = self._grid[b[0]][b[1]], self._grid[a[0]][a[1]]

    def copy(self) -> Puzzle:
        new = Puzzle(self._grid)
        new._history = self._history[:]
        return new

    def serialize(self, rowDelim: str = ';', colDelim: str = ':') -> str:
        return rowDelim.join([
            colDelim.join([
                str(e) if e != self._null else '-'
                for e in r
            ]) for r in self._grid
        ])

    def __eq__(self, __o: object) -> bool:
        return self._grid == __o._grid

    def __lt__(self, __o: object) -> bool:
        return self.cost() < __o.cost()

    def __str__(self) -> str:
        return self.serialize('\n', '\t')

    @staticmethod
    def loadFile(
        fname: str,
        key: Callable[[str], T] = int,
        fnull: str = '-',
        goal: list[list[T]] = None,
        null: T = None
    ) -> Puzzle:
        """Load puzzle from a file."""
        with open(fname) as f:
            if null is None:
                null = Puzzle._null

            grid: list[list[int]] = []
            size = -1
            for line in f:
                line = line.strip()
                if len(line) > 0:
                    row = [
                        key(x) if x != fnull else null
                        for x in filter(None, re.split('\s', line))
                    ]

                    if size == -1:
                        size = len(row)
                    elif len(row) != size:
                        raise ValueError('Puzzle row sizes mismatch.')
                    grid.append(row)

            if len(grid) != size:
                raise ValueError('Puzzle row and column size mismatch.')

            puzzle = Puzzle(grid, goal=goal, null=null)
            return puzzle

    @staticmethod
    def showMoves(puzzle: Puzzle, moves: list[Move], isAnsi: bool = True) -> None:
        puzzle = puzzle.copy()
        for i in range(-1, len(moves)):
            print(puzzle)
            if i == -1:
                print(f'INITIAL STATE')
            else:
                print(f'MOVE {i + 1}: {moves[i].value}')

            if i < len(moves) - 1:
                print(f'NEXT: {moves[i + 1].value}')

                if isAnsi:
                    input(':')
                else:
                    print('')

                puzzle.move(moves[i + 1])

                if isAnsi:
                    sys.stdout.write(
                        '\033[F\033[2K\033[1G' * (puzzle._size + 3))
                    sys.stdout.flush()


if __name__ == '__main__':
    p = Puzzle.loadFile('test.txt')
    print(p)
    print(p.isSolveable())
