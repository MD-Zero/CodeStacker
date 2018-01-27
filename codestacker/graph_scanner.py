#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Directed graph scanning utilities.
"""

def check_cyclicity(graph):
    """
    Given a directed graph, visit it looking for a cycle.
    """
    is_cyclic = False
    dead_ends = set()

    for node, children in graph.items():
        if node in dead_ends:
            continue

        if scan_graph([node], children, graph, dead_ends):
            is_cyclic = True
            break

    return is_cyclic

####################################################################################################

def scan_graph(visited_nodes, children, graph, dead_ends):
    """
    Given a starting node, visit all its children and descendants, looking for a cycle.
    """
    for node in children:
        if node not in graph or node in dead_ends:
            continue

        if node in visited_nodes:
            return True
        else:
            visited_nodes.append(node)

            if scan_graph(visited_nodes, graph[node], graph, dead_ends):
                return True

            dead_ends.add(visited_nodes.pop())

    return False
