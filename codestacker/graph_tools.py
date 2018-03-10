#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Directed graph scanning utilities.
"""

####################################################################################################

def is_directed_acyclic_graph(graph):
    """
    Check whether the input graph is a DAG (Directed Acyclic Graph).

    :param graph: The directed graph, in a form of a dictionary (key = node, value = children).
    """
    dead_ends = set()
    depth = 0

    for node, children in graph.items():
        if node in dead_ends:
            continue

        _go_down_and_check_cycle(graph, [node], children, dead_ends, depth)

####################################################################################################

def get_topological_ordering(graph):
    """
    Given a directed graph in input, return the topological ordering of its nodes.

    :param graph: The directed graph, in a form of a dictionary (key = node, value = children).

    :returns: A list of nodes, in topological order (from bottom to top node).
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

# '10' is an arbitrary limit.
_DEPTH_THRESHOLD = 10

def _go_down_and_check_cycle(graph, visited_nodes, children, dead_ends, depth):
    """
    Given a start node, visit recursively all its descendants, looking for a cycle. The depth value
    is monitored, and a "too deep" graph (more than 10 descendants) will abort the visitation.

    :param graph: The directed graph being visited.
    :param visited_nodes: The list of previously visited nodes.
    :param children: The set of direct children of a node.
    :param dead_ends: The list of identified "dead-end" nodes in the graph.
    :param depth: The graph's depth.

    :raises GraphError: either the graph is cyclic, or its depth is too high.
    """
    from .errors            import errors as E
    from .errors.exceptions import GraphError

    depth += 1

    if depth >= _DEPTH_THRESHOLD:
        raise GraphError(E.GRAPH_TOO_DEEP)

    for node in children:
        if (node not in graph) or (node in dead_ends):
            continue

        if node in visited_nodes:
            raise GraphError(E.CYCLES_IN_GRAPH)

        visited_nodes.append(node)

        _go_down_and_check_cycle(graph, visited_nodes, graph[node], dead_ends, depth)

        dead_ends.add(visited_nodes.pop())
