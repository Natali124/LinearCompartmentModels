from GeneratingGraphs import combinations
from Models import LinearCompartmentModel
from GeneratingGraphs import combinations
from GeneratingGraphs import generating_graph_combinations
from Bfs import all_reach_outputs
import copy

def generating_models(all_graphs, n_inputs, n_outputs, n_leaks):
    """returns list of all models"""
    n = len(next(iter(all_graphs)).list)
    all_models = []
    all_inputs = choose_in_list(n, n_inputs)
    all_outputs = choose_in_list(n, n_outputs)
    all_leaks = choose_in_list(n, n_leaks)
    for graph in all_graphs:
        for inp in all_inputs:
            for out in all_outputs:
                for leak in all_leaks:
                    model = LinearCompartmentModel(graph.list, inp, out, leak)
                    if all_reach_outputs(model.graph, model.outputs) == False: #so that all vertices reach outputs
                        continue
                    all_models.append(model)
    return all_models
    #         Problem: includes graphs which are not connected
    
def choose_in_list (n_v, n_e):
    #take all tuples of size two
    return list(combinations(range(n_v), n_e))