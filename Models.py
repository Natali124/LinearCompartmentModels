import itertools
import copy

class LinearCompartmentModel:

    def __init__(self, graph, inputs, outputs, leaks):
        self.graph = graph #array of integer sets representing the adjacency lists of the graph
        self.inputs = inputs #set of input nodes
        self.outputs = outputs #set of output nodes
        self.leaks = leaks #set of leak nodes

    def __eq__(self, other):
        return compare_models(self, other)

    # Gleb: by convention `__repr__` is a string of code that could be used to create the object
    # in this case, `__str__` would be more appropriate
    def __repr__(self):
        return f'Graph: {self.graph}, Inputs: {self.inputs}, Outputs: {self.outputs}, Leaks: {self.leaks}'

def permute_set (s, permutation):
    """gives permutation as a new list"""
    # Gleb: one could use a comprehension `return {permutation[num] for num in s}`
    res = set()
    for number in s:
        res.add(permutation[number])
    return res

def permute_graph (graph, permutation):
    """returns a graph created by tranforming given model with given permutation"""
    result_graph = [None] * len(graph)
   
    for i in range(len(graph)):
        result_graph[permutation[i]] = copy.deepcopy(graph[i])
        result_graph[permutation[i]] = permute_set(result_graph[permutation[i]], permutation)
    return result_graph

def compare_models (model_1, model_2):
    """returns true if two graphs are the same, false otherwise"""
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

def generating_all_isomorphisms(base_graph):
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


def generating_models(all_graphs, n_inputs, n_outputs, n_leaks):
    n = len(next(iter(all_graphs)).list)
    all_models = []
    all_inputs = choose_in_list(n, n_inputs)
    all_outputs = choose_in_list(n, n_outputs)
    all_leaks = choose_in_list(n, n_leaks)
    for graph in all_graphs:
        for inp in all_inputs:
            for out in all_outputs:
                for leak in all_leaks:
                    all_models.append(LinearCompartmentModel(graph, inp, out, leak))
    return all_models
    #problems: includes ones where inputs don't reach outputs
    #          includes graphs which are not connected

        
def choose_in_list (n_v, n_e):
    #take all tuples of size two
    return list(combinations(range(n_v), n_e))
    

def compare_graphs (graph_1, graph_2):
    """returns true if two graphs are the same, false otherwise"""
    n = len(graph_1) #number of vertices
   
    vertices_list = list(range(n))
    permutations_object = itertools.permutations(vertices_list)
    #creating a permutations object
   
    for permutation in permutations_object:
        if permute_graph(graph_2, permutation) == graph_1:
            return True
    return False
