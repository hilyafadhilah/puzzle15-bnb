#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""View module for Puzzle 15 program

Notes
-----
Comments are omitted because code is self-explanatory.
"""

from typing import Any, Callable, TypeVar

T = TypeVar('T')


def displayHeader(title: str, sep: str = '=') -> None:
    n = (60 - len(title) - 4) // 2

    if n > 0:
        header = f"\n {sep * n} {title} {sep * n}\n"
    else:
        header = f"\n {title}\n"

    print(header)


def displayList(lst: list[T], key: Callable[[T], Any] = None) -> None:
    maxSpace = len(str(len(lst)))
    for i in range(len(lst)):
        x = key(lst[i]) if key else lst[i]
        spacing = maxSpace + 2
        print(f"{i + 1:{spacing}}. {x}")
    print('')
