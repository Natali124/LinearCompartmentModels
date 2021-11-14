def revert_graph (graph):
    n_of_vertices = len(graph)
    result = [[] for i in range(n_of_vertices)]
    for i in range(n_of_vertices):
        for j in range(len(graph[i])):
            result[graph[i][j]].append(i)
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
   
   
def bfs_for_specific_node(graph, node):
    """checks if specific output reaches all points"""
    graph = revert_graph(graph)
   
    result = []
    queue = []
    visited = [0] * len(graph)
    visited [node] = 1
    queue.append(node)
   
    while queue:
        s = queue.pop(0)
        result.append(s)
       
        for neighbour in graph[s]:
            if visited[neighbour] == 0:
                visited[neighbour] = 1
                queue.append(neighbour)
    if len(result) == len(graph):
        return True
    return False