import itertools
import copy

class LinearCompartmentModel:

    def __init__(self, graph, inputs, outputs, leaks):
        self.graph = graph #array of integer arrays representing the adjacency lists of the graph
        self.inputs = inputs #array of input nodes
        self.outputs = outputs #array of output nodes
        self.leaks = leaks #array of sink nodes

    def __eq__(self, other):
        if self.inputs == other.inputs:
            if self.outputs == other.outputs:
                if self.leaks == other.leaks:
                    # Gleb: this is up to premutation while the previous comparisons are not...
                    if compare_graphs(self.graph,other.graph):
                        return True
        return False

    #maybe we can check here if it "is a model or not."
    def check_if_reaches_output(vertex, graph):
        """checks if every vertex reaches every output"""
        pass

def permute_graph (graph, permutation):
    """returns a graph created by tranforming given model with given permutation"""
    # Gleb: I think this cloning is not necessary. Is it?
    result_graph = copy.deepcopy(graph) #cloning the graph
   
    for i in range(len(permutation)):
        result_graph[i] = copy.deepcopy(graph[permutation[i]])
        #for every vertex i in graph: i = permutation[i]
        for j in range(len(result_graph[i])):
            result_graph[i][j] = permutation[result_graph[i][j]]
             #every connected vertex = permutation [connected vertex]
    return result_graph
# Gleb: to discuss: either sotring verices of using sets

def permute_list (l, permutation):
    res = copy.deepcopy(l)
    for i in range(len(permutation)):
        res[i] = l[permutation[i]]
    return res


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
    #check if model1 equals to transformed model2 for each transformation

def compare_models (model1, model2):
    """returns true if two graphs are the same, false otherwise"""
    n = len(model1.graph) #number of vertices
   
    vertices_list = list(range(n))
    permutations_object = itertools.permutations(vertices_list)
    #creating a permutations object
   
    for permutation in permutations_object:
        return (permute_list(model2.inputs) == model1.inputs and permute_list(model2.outputs) == model1.outputs and permute_list(model2.leaks) == model1.leaks)
    #check if model1 equals to transformed model2 for each transformation
# I haven't checked on graphs but it should be guarranteed at this point.
# maybe put it in comparison function?
# Gleb: sounds like a plan

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
