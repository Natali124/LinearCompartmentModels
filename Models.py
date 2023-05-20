import itertools
import copy

class LinearCompartmentModel:
    """
        data attributes:
            graph - list of sets
            inputs - set
            outputs - set
            leaks - set
    """

    def __init__(self, graph, inputs, outputs, leaks):
        self.graph = graph #array of integer sets representing the adjacency lists of the graph
        self.inputs = inputs #set of input nodes
        self.outputs = outputs #set of output nodes
        self.leaks = leaks #set of leak nodes

    def __eq__(self, other):
        return compare_models(self, other)

    def __signature(self):
        return (tuple(sorted(self.outputs)), tuple(sorted(self.inputs)), tuple(sorted(self.leaks)))

    def __lt__(self, other):
        "for deciding which model to keep in the equivalence class"
        return self.__signature() < other.__signature()

    def __repr__(self):
        return f'Graph: {self.graph}, Inputs: {self.inputs}, Outputs: {self.outputs}, Leaks: {self.leaks}'
    
    def __hash__(self):
        return hash(self.__signature())
    
    def generate_model_isomorphisms(self):
        """
        generates all isomorphisms of a model in a sorted way
        result is a list of tuples - model and permutation
        """
        
        result = []
        n = len(self.graph)
       
        vertices_list = list(range(n))
        permutations_object = itertools.permutations(vertices_list)
        #creating a permutations object
        
        for permutation in permutations_object:
            model_new = LinearCompartmentModel(permute_graph(self.graph,permutation), 
                                               permute_set(self.inputs, permutation),
                                               permute_set(self.outputs, permutation),
                                               permute_set(self.leaks, permutation)
                                               )
            result.append((model_new, permutation))
       
        return result
    
    def strongly_connected(self):
            for i in range(len(self.graph)):
                visited = set()
                self._strongly_connected_rec(i, visited)
                if len(visited) != len(self.graph):
                    return False
            return True

    def _strongly_connected_rec(self, vertex, visited):
        visited.add(vertex)
        for u in self.graph[vertex]:
            if u not in visited:
                self._strongly_connected_rec(u, visited)

def permute_set(s, permutation):
    """gives permutation as a new list"""
    return {permutation[num] for num in s}

def permute_graph(graph, permutation):
    """returns a graph created by tranforming given model with given permutation"""
    result_graph = [None] * len(graph)
   
    for i in range(len(graph)):
        result_graph[permutation[i]] = copy.deepcopy(graph[i])
        result_graph[permutation[i]] = permute_set(result_graph[permutation[i]], permutation)
    return result_graph

def compare_models(model_1, model_2):
    """returns true if two models are the same, false otherwise"""
    n = len(model_1.graph) #number of vertices
   
    vertices_list = list(range(n))
    permutations_object = itertools.permutations(vertices_list)
    #creating a permutations object
   
    for permutation in permutations_object:
        if (permute_graph(model_2.graph, permutation) == model_1.graph and 
            permute_set(model_2.inputs, permutation) == model_1.inputs and 
            permute_set(model_2.outputs, permutation) == model_1.outputs and 
            permute_set(model_2.leaks, permutation) == model_1.leaks):
            return True
    return False
# Natali: We need to check on the specific permutation if all conditions hold. 
# This is why we can not use compare_graphs. I decided to keep compare_graphs function
# in case it gets useful later while we are dealing just with graph isomorphisms.

def generate_all_isomorphisms(base_graph):
    """generates all isomorphisms of a graph in a sorted way"""
    result = []
   
    vertices_list = list(range(len(base_graph)))
    permutations_object = itertools.permutations(vertices_list)
    #creating a permutations object
    for permutation in permutations_object:
        result.append(permute_graph(base_graph,permutation))
    res = copy.deepcopy(result)
   
    b = False
    for isomorphism in result:
        for vertex in isomorphism:
            if (len(vertex) < 2):
                continue
            for i in range(len(vertex)-1):
                if vertex[i] > vertex[i+1]:
                    res.remove(isomorphism)
                    b = True
                    break
            if b == True:
                b == False
                break
    return res

def compare_graphs(graph_1, graph_2):
    """returns true if two graphs are the same, false otherwise"""
    n = len(graph_1) #number of vertices
   
    vertices_list = list(range(n))
    permutations_object = itertools.permutations(vertices_list)
    #creating a permutations object
   
    for permutation in permutations_object:
        if permute_graph(graph_2, permutation) == graph_1:
            return True
    return False
