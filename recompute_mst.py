#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 2: Recomputing a Minimum Spanning Tree

Team Number:
Student Names:
'''

'''
Copyright: justin.pearson@it.uu.se and his teaching assistants, 2022.

This file is part of course 1DL231 at Uppsala University, Sweden.

Permission is hereby granted only to the registered students of that
course to use this file, for a homework assignment.

The copyright notice and permission notice above shall be included in
all copies and extensions of this file, and those are not allowed to
appear publicly on the internet, both during a course instance and
forever after.
'''
from typing import *  # noqa
import unittest  # noqa
import math  # noqa
from src.recompute_mst_data import data  # noqa
from src.graph import Graph  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['update_MST_1', 'update_MST_2', 'update_MST_3', 'update_MST_4']


def update_MST_1(G: Graph, T: Graph, e: Tuple[str, str], weight: int) -> None:
    """
    Pre:
    Post:
    Ex:   TestCase 1 below
    """
    (u, v) = e
    assert (e in G and e not in T and weight > G.weight(u, v))


def update_MST_2(G: Graph, T: Graph, e: Tuple[str, str], weight: int) -> None:
    """
    Pre:
    Post:
    Ex:   TestCase 2 below
    """
    (u, v) = e
    assert (e in G and e not in T and weight < G.weight(u, v))


def update_MST_3(G: Graph, T: Graph, e: Tuple[str, str], weight: int) -> None:
    """
    Pre:
    Post:
    Ex:   TestCase 3 below
    """
    (u, v) = e
    assert (e in G and e in T and weight < G.weight(u, v))


def update_MST_4(G: Graph, T: Graph, e: Tuple[str, str], weight: int) -> None:
    """
    Pre:
    Post:
    Ex:   TestCase 4 below
    """
    (u, v) = e
    assert (e in G and e in T and weight > G.weight(u, v))


class RecomputeMstTest(unittest.TestCase):
    """
    Test Suite for minimum spanning tree problem

    Any method named "test_something" will be run when this file is
    executed. You may add your own test cases if you wish.
    (You may delete this class from your submitted solution.)
    """
    logger = logging.getLogger('RecomputeMstTest')
    data = data
    update_MST = [
        update_MST_1,
        update_MST_2,
        update_MST_3,
        update_MST_4
    ]

    def assertUndirectedEdgesEqual(self, actual: List[Tuple[str, str]],
                                   expected: List[Tuple[str, str]]) -> None:
        self.assertListEqual(
            sorted(((min(u, v), max(u, v)) for u, v in actual)),
            sorted(((min(u, v), max(u, v)) for u, v in expected))
        )

    def assertEdgesInGraph(self, edges: List[Tuple[str, str]],
                           graph: Graph) -> None:
        for edge in edges:
            self.assertIn(edge, graph)

    def assertGraphIsConnected(self, graph: Graph) -> None:
        if len(graph.nodes) == 0:
            return
        visited = set()
        s = graph.nodes[0]
        queue = deque([s])
        while len(queue) > 0:
            u = queue.popleft()
            visited.add(u)
            for v in graph.neighbors(u):
                if v not in visited:
                    queue.append(v)
        for u in graph.nodes:
            self.assertIn(u, visited)

    def assertGraphsEqual(self, actual: Graph, expected: Graph) -> None:
        for u, v in actual.edges:
            self.assertEqual(actual.weight(u, v), expected.weight(u, v))

    def test_mst(self) -> None:
        """
        passing is not a guarantee of correctness.
        """
        # You only need to implement one case, so you can add the other
        # cases to the following set to skip them:
        cases_to_skip = set([])
        for i, update_MST in enumerate(RecomputeMstTest.update_MST, start=1):
            if i in cases_to_skip:
                self.logger.info(f"skip testing update_MST_{i}")
                continue
            # test update_MST_{i}:
            for j, instance in enumerate(RecomputeMstTest.data):
                # test update_MST_{i} using instance {j}:
                with self.subTest(case=i, instance=j):
                    graph = instance['graph'].copy()
                    tree = instance['mst'].copy()
                    u, v = instance['solutions'][i - 1]['edge']
                    weight = instance['solutions'][i - 1]['weight']
                    expected = instance['solutions'][i - 1]['expected']
                    expected_graph = instance['graph'].copy()
                    expected_graph.set_weight(u, v, weight)
                    self.assertIsNone(update_MST(graph, tree, (u, v), weight))
                    self.assertUndirectedEdgesEqual(tree.edges, expected)
                    self.assertEdgesInGraph(tree.edges, expected_graph)
                    self.assertGraphIsConnected(tree)
                    self.assertGraphsEqual(graph, expected_graph)


if __name__ == '__main__':
    # Set logging config to show debug messages:
    logging.basicConfig(level=logging.DEBUG)
    # run unit tests (failfast=True stops testing after the first failed test):
    unittest.main(failfast=True)
