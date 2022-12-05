#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 2: Recomputing a Minimum Spanning Tree

Team Number: Team 15
Student Names: Jonas Teglund & Oscar Wadestig
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
    Pre: G is a connected, weighted, undirected graph. T is the minimum spanning tree to the graph G. e is an edge in T. weight is greater than the current weight of the edge e.
    Post: Returns an updated MST after the edge e has gotten an increased weight.
    Ex:   TestCase 4 below
        g = Graph(is_directed=False)
        g.add_edge("a", "b", 28)
        g.add_edge("a", "c", 1171)
        g.add_edge("b", "c", 1277)
        t = Graph(is_directed=False)
        t.add_edge("a", "b", weight=28)
        t.add_edge("a", "c", weight=1171)
        update_MST_4(g, t, ("a", "b"), 29) returns a Graph with V=(a,b,c), E=((a, b),(a, c),(b, a),(c, a)), (w((a,b))=29,w((a,c))=1171,w((b,a))=29,w((c,a))=1171)
    """
    (u, v) = e
    assert (e in G and e in T and weight > G.weight(u, v))
    #Remove the edge that is getting an updated weight from the MST T
    T.remove_edge(u, v)
    #Update the edge with the new weight in the graph G
    G.set_weight(u, v, weight)

    
    nodes_of_g1 = set(u)
    nodes_of_g2 = set(v)
    
    stack_g1 = [u]
    stack_g2 = [v]

    #Find the nodes in T that are on one side of the disconected graph
    while len(stack_g1) > 0:
        x = stack_g1.pop()
        for y in T.neighbors(x):
            if y not in nodes_of_g1:
                nodes_of_g1.add(y)
                stack_g1.append(y)

    #Find the nodes in T that are on the other side of the disconected graph
    while len(stack_g2) > 0:
        x = stack_g2.pop()
        for y in T.neighbors(x):
            if y not in nodes_of_g2:
                nodes_of_g2.add(y)
                stack_g2.append(y)

    #Find all edges in the graph G
    edges = G.edges
    edges_in_the_cut = []

    #Find all edges that would connect T into a spanning tree again.
    for e in edges:
        if (e[0] in nodes_of_g1 and e[1] in nodes_of_g2 ) or (e[1] in nodes_of_g1 and e[0] in nodes_of_g2):
            edges_in_the_cut.append((e, G.weight(e[0], e[1])))
    
    #Find the edge that also would make T into a minimum spanning tree by finding the one with
    #minimum weight
    (edge_to_add, w) = min(edges_in_the_cut, key=lambda x: x[1])

    #Add that edge to T to make T into a MST of the updated graph G
    T.add_edge(edge_to_add[0], edge_to_add[1], weight=w)
    return T



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
        cases_to_skip = set([1,2,3])
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
                    
                    self.assertIsNotNone(update_MST(graph, tree, (u, v), weight))
                    self.assertUndirectedEdgesEqual(tree.edges, expected)
                    self.assertEdgesInGraph(tree.edges, expected_graph)
                    self.assertGraphIsConnected(tree)
                    self.assertGraphsEqual(graph, expected_graph)


if __name__ == '__main__':
    # Set logging config to show debug messages:
    logging.basicConfig(level=logging.DEBUG)
    # run unit tests (failfast=True stops testing after the first failed test):
    unittest.main(failfast=True)
