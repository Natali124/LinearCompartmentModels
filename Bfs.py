import copy

def revert_graph (graph):
    """takes set graph notation, reverts and returns list"""
    n_of_vertices = len(graph)
    result = [[] for i in range(n_of_vertices)]
    for i in range(n_of_vertices):
        for number in graph[i]:
            result[number].append(i)
    return result

def all_reach_outputs(graph, outputs):
    """checks if at least one output is reachable from all points, outputs should be a list or a set"""
    graph = revert_graph(graph)
   
    queue = list(copy.deepcopy(outputs))
    visited = [0] * len(graph)
    for index in queue:
        visited[index] = 1
    result = set()
   
    while queue:
        s = queue.pop()
        result.add(s)
        for neighbour in graph[s]:
            if visited[neighbour] == 0:
                visited[neighbour] = 1
                queue.append(neighbour)

    return len(result) == len(graph)

def is_connected(graph):
    """checks if graph is connected. Does not take into account that graph is directed. 
        graph needs to be a list of sets."""
    queue = [0]
    visited = [0] * len(graph)
    visited[0] = 1
    result = set()
    
    while queue:
        s = queue.pop()
        result.add(s)
        for neighbour in graph[s]:
            if visited[neighbour] == 0:
                visited[neighbour] = 1
                queue.append(neighbour)
    
    rev_graph = revert_graph(graph)
    
    queue = [0]
    
    while queue:
        s = queue.pop()
        result.add(s)
        for neighbour in rev_graph[s]:
            if visited[neighbour] == 0:
                visited[neighbour] = 1
                queue.append(neighbour)
    
    return len(result) == len(graph)