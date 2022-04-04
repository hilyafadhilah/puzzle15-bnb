#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Puzzle 15 Solver

Solve Puzzle 15 using Branch and Bound Algorithm
with offset tile count heuristics. Puzzle will be
generated randomly, or can be loaded from a file.

Example
-------
Usage

    $ python solver.py [fname] [--verbose]

Use --verbose flag if you want full output with no
ANSI escape codes.

Puzzle file example::

    5   1   3   4
    9   2   7   8
    -   6   15  11
    13  10  14  12

The puzzle tiles is assumed to be integers with goal state
being the ascending order. Null tile is denoted with a hypen.

Notes
-----
Algorithm reference:
`R. Munir et al <https://informatika.stei.itb.ac.id/~rinaldi.munir/Stmik/2020-2021/Algoritma-Branch-and-Bound-2021-Bagian1.pdf>` 

Please also note that the structure used here is not optimized
for speed.

See Also
--------
puzzle.Puzzle

"""
import argparse
import sys
from queue import PriorityQueue
from time import perf_counter
from types import NoneType

from console import enable_vt_mode
from puzzle import Puzzle, Move
import view

# parse arguments

parser = argparse.ArgumentParser(
    description='Puzzle15 Solver using Branch & Bound algorithm.')
parser.add_argument(
    'fname', nargs='?', help='puzzle 15 problem file path')
parser.add_argument(
    '--verbose', action='store_true', help='put output noninteractively')

args = parser.parse_args()

# create puzzle based on args

if args.fname is None:
    root = Puzzle()
else:
    root = Puzzle.loadFile(args.fname)

# display puzzle and its stats

enable_vt_mode()
view.displayHeader('THE PUZZLE')
print(root)

view.displayHeader('Tile Offset Values', '-')

els = root.elements
els.remove(root.null)
mx = len(str(els[max(root.elements, key=lambda e: len(str(e)))]))
for e in els:
    print(f"Tile {e:{mx}} = {root.offset(e)}")

print(f'\nTotal + X = {root.totalOffset()}')

# main algorithm

queue: PriorityQueue[Puzzle] = PriorityQueue()
visited: dict[str, NoneType] = {}

if root.isSolveable():
    queue.put(root)
    visited[root.serialize()] = None

view.displayHeader('Solve')

count = 1
if not args.verbose:
    print('Nodes branched:')
    print(count, end='')

startTime = perf_counter()

while not queue.empty():
    puzzle = queue.get()

    if puzzle.isSolved():
        break

    for move in Move:
        new = puzzle.copy()
        if new.move(move):
            key = new.serialize()
            if key not in visited:
                queue.put(new)
                visited[key] = None
                count += 1

                if not args.verbose:
                    sys.stdout.write(f'\033[2K\033[1G{count:,}')
                    sys.stdout.flush()

endTime = perf_counter()

if args.verbose:
    print(f'Nodes branched:\n{count:,}')
else:
    print('')

print('\nTime taken:')
print(f'{endTime - startTime:.4f}s')

# solution

view.displayHeader('Solution')

if queue.empty():
    print('The puzzle cannot be solved.')
else:
    print(f'Number of moves: {len(puzzle.history)}')
    print('Sequence:')
    view.displayList(puzzle.history, lambda x: x.value)

    view.displayHeader('Step by Step')
    Puzzle.showMoves(root, puzzle.history, not args.verbose)
