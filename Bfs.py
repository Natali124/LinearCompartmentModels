def revert_graph_set (graph):
    """takes set graph notation, reverts and returns list"""
    n_of_vertices = len(graph)
    result = [[] for i in range(n_of_vertices)]
    for i in range(n_of_vertices):
        for number in graph[i]:
            result[number].append(i)
    return result

def all_reach_outputs(graph, outputs):
    """checks if at least one output is reachable from all points"""
    graph = revert_graph(graph)
   
    queue = outputs
    visited = [0] * len(graph)
    result = []
   
    while queue:
        s = queue.pop(0)
        result.append(s)
        for neighbour in graph[s]:
            if visited[neighbour] == 0:
                visited[neighbour] = 1
                queue.append(neighbour)

    return len(result) == len(graph)