#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for graph_tools.py module.
"""

####################################################################################################

import unittest

class TestGraphTools(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
        self.acyclic_graph = {
            'a': set(['b']),
            'b': set(['c', 'd']),
            'c': set(['d', 'e']),
            'd': set(['e', 'g']),
            'e': set(['g'])}

        self.cyclic_graph = {
            'a': set(['b']),
            'b': set(['c', 'd']),
            'c': set(['d', 'a'])}

        self.deep_graph = {
            'a': set(['b']),
            'b': set(['c']),
            'c': set(['d']),
            'd': set(['e']),
            'e': set(['f']),
            'f': set(['g']),
            'g': set(['h']),
            'h': set(['i']),
            'i': set(['j']),
            'j': set(['k'])}

    def test_is_directed_acyclic_graph(self):
        """Test DAG detection."""
        from codestacker             import errors as E
        from codestacker.exceptions  import GraphError
        from codestacker.graph_tools import is_directed_acyclic_graph

        is_directed_acyclic_graph(self.acyclic_graph)

        with self.assertRaises(GraphError) as context:
            is_directed_acyclic_graph(self.cyclic_graph)

        self.assertEqual(context.exception.message, E.CYCLES_IN_GRAPH)

        with self.assertRaises(GraphError) as context:
            is_directed_acyclic_graph(self.deep_graph)

        self.assertEqual(context.exception.message, E.DEPTH_THRESHOLD)

    def test_get_topological_ordering(self):
        """Test topological ordering."""
        from codestacker.graph_tools import get_topological_ordering

        expected_ordered_list = ['g', 'e', 'd', 'c', 'b']
        actual_ordered_list = get_topological_ordering(self.acyclic_graph)

        self.assertEqual(expected_ordered_list, actual_ordered_list)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
