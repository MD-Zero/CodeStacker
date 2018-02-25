#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Directed graph scanning utilities.
"""

####################################################################################################

def is_directed_acyclic_graph(graph):
    """
    Check whether the input graph is a DAG (Directed Acyclic Graph).
    """
    is_acyclic = True
    dead_ends = set()
    depth = 0

    for node, children in graph.items():
        if node in dead_ends:
            continue

        _go_down_and_check_cycle([node], children, graph, dead_ends, depth)

    return is_acyclic

####################################################################################################

def get_topological_ordering(graph):
    """
    Given a directed graph in input, return the topological ordering of its nodes.
    """
    import copy

    topological_ordering = []
    altered_graph = copy.deepcopy(graph)

    # The altered graph *should* progressively shrink in size until emptiness, hence the "while".
    while altered_graph:
        for node, children in graph.items():
            if not children:
                altered_graph.pop(node)

            for child in children:
                if child not in graph:
                    # Prevent addition of duplicates.
                    if child not in topological_ordering:
                        topological_ordering.append(child)

                    altered_graph[node].discard(child)

                    if not altered_graph[node]:
                        altered_graph.pop(node)

        graph = copy.deepcopy(altered_graph)

    return topological_ordering

####################################################################################################

_ERROR_DEPTH_THRESHOLD = 'depth threshold exceeded'
_ERROR_CYCLES_IN_GRAPH = 'cycle(s) in graph detected'

def _go_down_and_check_cycle(visited_nodes, children, graph, dead_ends, depth):
    """
    Given a start node, visit all its descendants, looking for a cycle.
    """
    from .exceptions import GraphError

    depth += 1

    # '10' is an arbitrary limit.
    if depth >= 10:
        raise GraphError(_ERROR_DEPTH_THRESHOLD)

    for node in children:
        if (node not in graph) or (node in dead_ends):
            continue

        if node in visited_nodes:
            return True

        visited_nodes.append(node)

        if _go_down_and_check_cycle(visited_nodes, graph[node], graph, dead_ends, depth):
            raise GraphError(_ERROR_CYCLES_IN_GRAPH)

        dead_ends.add(visited_nodes.pop())

    return False
