#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignment 2, Problem 1: Search String Replacement

Team Number:
Student Names:
"""

"""
Copyright: justin.pearson@it.uu.se and his teaching assistants, 2022.

This file is part of course 1DL231 at Uppsala University, Sweden.

Permission is hereby granted only to the registered students of that
course to use this file, for a homework assignment.

The copyright notice and permission notice above shall be included in
all copies and extensions of this file, and those are not allowed to
appear publicly on the internet, both during a course instance and
forever after.
"""
from typing import *  # noqa
import unittest  # noqa
import math  # noqa
from src.difference_data import data  # noqa
from collections import defaultdict  # noqa
from string import ascii_lowercase  # noqa

# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa

# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa


# Solution to Task B:
def min_difference(s: str, r: str, R: Dict[str, Dict[str, int]]) -> int:

    # STEP 1: MAKE STRINGS MATCH UP WITH - WHERE THERE IS NO MATCH
    strToMatch = str(r)
    strToManip = str(s)
    i = 0
    matchingStr = ""

    while len(strToMatch) != len(strToManip):
        if strToManip[i] == strToMatch[i]:
            matctingStr = matchingStr + strToManip[i]
        else:
            s
        i++

    """
    Pre:  For all characters c in s and k in r,
          then R[c][k] exists, and R[k][c] exists.
    Post:
    Ex:   Let R be the resemblance matrix where every change and skip
          costs 1
          min_difference("dinamck", "dynamic", R) --> 3
    """
    # To get the resemblance between two letters, use code like this:
    # difference = R['a']['b']


# Solution to Task C:
def min_difference_align(
    s: str, r: str, R: Dict[str, Dict[str, int]]
) -> Tuple[int, str, str]:
    """
    Pre:  For all characters c in s and k in r,
          then R[c][k] exists, and R[k][c] exists.
    Post:
    Ex:   Let R be the resemblance matrix where every change and skip
          costs 1
          min_difference_align("dinamck", "dynamic", R) -->
                                    3, "dinam-ck", "dynamic-"
                                 or 3, "dinamck", "dynamic"
    """


# Sample matrix provided by us:
def qwerty_distance() -> Dict[str, Dict[str, int]]:
    """
    Generates a QWERTY Manhattan distance resemblance matrix

    Costs for letter pairs are based on the Manhattan distance of the
    corresponding keys on a standard QWERTY keyboard.
    Costs for skipping a character depends on its placement on the keyboard:
    adding a character has a higher cost for keys on the outer edges,
    deleting a character has a higher cost for keys near the middle.

    Usage:
        R = qwerty_distance()
        R['a']['b']  # result: 5
    """
    R = defaultdict(dict)
    R["-"]["-"] = 0
    zones = ["dfghjk", "ertyuislcvbnm", "qwazxpo"]
    keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for row, content in enumerate(zones):
        for char in content:
            R["-"][char] = row + 1
            R[char]["-"] = 3 - row
    for a, b in ((a, b) for b in ascii_lowercase for a in ascii_lowercase):
        row_a, pos_a = next(
            (row, content.index(a))
            for row, content in enumerate(keyboard)
            if a in content
        )
        row_b, pos_b = next(
            (row, content.index(b))
            for row, content in enumerate(keyboard)
            if b in content
        )
        R[a][b] = abs(row_b - row_a) + abs(pos_a - pos_b)
    return R


class MinDifferenceTest(unittest.TestCase):
    """
    Test Suite for search string replacement problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own test
    cases if you wish.
    (You may delete this class from your submitted solution.)
    """

    logger = logging.getLogger("MinDifferenceTest")
    data = data
    min_difference = min_difference
    min_difference_align = min_difference_align

    def assertMinDifferenceSignature(self, res_difference: Any) -> None:
        self.assertEqual(type(res_difference), int)

    def assertMinDifferenceAlignSignature(self, t: Any):
        self.assertEqual(type(t), tuple)
        self.assertEqual(len(t), 3)
        res_difference, res_s, res_r = t
        self.assertEqual(type(res_difference), int)
        self.assertEqual(type(res_s), str)
        self.assertEqual(type(res_r), str)

    def assertMinDifference(
        self, s: str, r: str, difference: int, R: Dict[str, Dict[str, int]]
    ) -> None:
        res_difference = MinDifferenceTest.min_difference(s, r, R)
        self.assertMinDifferenceSignature(res_difference)
        self.assertEqual(
            res_difference,
            difference,
            f'Difference between s="{s}" and r="{r}" was '
            f"{res_difference}, {difference} expected.",
        )

    def assertMinDifferenceAlign(
        self,
        s: str,
        r: str,
        difference: int,
        R: int,
        solutions: Union[Set[Tuple[str, str]], None] = None,
    ) -> None:
        t = MinDifferenceTest.min_difference_align(s, r, R)
        self.assertMinDifferenceAlignSignature(t)
        res_difference, res_s, res_r = t
        self.assertEqual(
            res_difference,
            difference,
            f'Difference between s="{s}" and r="{r}" was '
            f"{res_difference}, {difference} expected.",
        )

        self.assertEqual(len(res_s), len(res_r), f'len("{s}") != len("{r}")')

        res_sum = sum((R[res_s[i]][res_r[i]] for i in range(len(res_s))))

        self.assertEqual(
            res_sum,
            difference,
            f'Difference for s="{s}", r={r}, res_r={res_s}, and '
            f'"r="{res_r}" was summed to {res_sum}, {difference}'
            " expected.",
        )
        if solutions is not None:
            self.assertIn((res_s, res_r), solutions)

    def test_diff_sanity(self) -> None:
        """
        difference sanity test

        Given a simple resemblance matrix, test that the reported
        difference is the expected minimum. Do NOT assume we will always
        use this resemblance matrix when testing!

        passing is not a guarantee of correctness.
        """
        alphabet = ascii_lowercase + "-"
        # The simplest (reasonable) resemblance matrix:
        R = {a: {b: (0 if a == b else 1) for b in alphabet} for a in alphabet}
        # Warning: we may (read: 'will') use another matrix!
        self.assertMinDifference("dinamck", "dynamic", 3, R)
        self.assertMinDifference("polynomial", "exponential", 6, R)

    def test_align_sanity(self) -> None:
        """
        alignment sanity test

        Given a simple resemblance matrix, test that the reported
        difference is the expected minimum and that the returned strings
        are a valid solution. Do NOT assume we will always use this
        resemblance matrix when testing!

        passing is not a guarantee of correctness.
        """
        alphabet = ascii_lowercase + "-"
        # The simplest (reasonable) resemblance matrix:
        R = {a: {b: (0 if a == b else 1) for b in alphabet} for a in alphabet}
        # Warning: we may (read: 'will') use another matrix!
        self.assertMinDifferenceAlign(
            "dinamck",
            "dynamic",
            3,
            R,
            {("dinam-ck", "dynamic-"), ("dinamck", "dynamic")},
        )

        self.assertMinDifferenceAlign(
            "polynomial",
            "exponential",
            6,
            R,
            {("--polynomial", "exponen-tial"), ("--polynomial", "exponent-ial")},
        )

    def test_min_difference(self) -> None:
        """
        passing is not a guarantee of correctness.
        """
        for i, instance in enumerate(MinDifferenceTest.data):
            with self.subTest(instance=i):
                self.assertMinDifference(
                    instance["s"],
                    instance["r"],
                    instance["difference"],
                    # QWERTY resemblance matrix:
                    qwerty_distance(),
                )

    def test_min_difference_align(self) -> None:
        """
        passing is not a guarantee of correctness.
        """
        for i, instance in enumerate(MinDifferenceTest.data):
            with self.subTest(instance=i):
                self.assertMinDifferenceAlign(
                    instance["s"],
                    instance["r"],
                    instance["difference"],
                    # QWERTY resemblance matrix:
                    qwerty_distance(),
                    instance["solutions"],
                )


if __name__ == "__main__":
    # Set logging config to show debug messages:
    logging.basicConfig(level=logging.DEBUG)
    # run unit tests (failfast=True stops testing after the first failed test):
    unittest.main(failfast=True)
