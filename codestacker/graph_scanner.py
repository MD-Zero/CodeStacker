#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Directed graph scanning utilities.
"""

def is_directed_acyclic_graph(graph):
    """
    Check whether the input graph is a DAG (Directed Acyclic Graph).
    """
    is_acyclic = True
    dead_ends = set()

    for node, children in graph.items():
        if node in dead_ends:
            continue

        if not go_down_and_check_cycle([node], children, graph, dead_ends):
            is_acyclic = False
            break

    return is_acyclic

####################################################################################################

def go_down_and_check_cycle(visited_nodes, children, graph, dead_ends):
    """
    Given a start node, visit all its descendants, looking for a cycle.
    """
    for node in children:
        if (node not in graph) or (node in dead_ends):
            continue

        if node in visited_nodes:
            return False

        visited_nodes.append(node)

        if not go_down_and_check_cycle(visited_nodes, graph[node], graph, dead_ends):
            return False

        dead_ends.add(visited_nodes.pop())

    return True

####################################################################################################

def get_topological_ordering(graph):
    """
    Given a directed graph in input, return the topological ordering of its nodes.
    """
    import copy

    topological_ordering = []
    altered_graph = copy.deepcopy(graph)

    while altered_graph:
        for node, children in graph.items():
            for child in children:
                if child not in graph:
                    if child not in topological_ordering:
                        topological_ordering.append(child)

                    altered_graph[node].discard(child)

                    if not altered_graph[node]:
                        altered_graph.pop(node)

        graph = copy.deepcopy(altered_graph)

    return topological_ordering
