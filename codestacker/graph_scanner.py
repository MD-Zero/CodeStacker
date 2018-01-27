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
