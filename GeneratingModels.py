from GeneratingGraphs import combinations
from Models import LinearCompartmentModel
from GeneratingGraphs import combinations
from GeneratingGraphs import generating_graph_combinations
from Bfs import all_reach_outputs
import copy
import json

def generating_models(all_graphs, n_inputs, n_outputs, n_leaks):
    """returns list of all models"""
    n = len(next(iter(all_graphs)).list)
    all_models = []
    for graph in all_graphs:
        temp = []
        for inp in combinations(range(n), n_inputs):
            for out in combinations(range(n), n_outputs):
                for leak in combinations(range(n), n_leaks):
                    model = LinearCompartmentModel(graph.list, inp, out, leak)
                    if all_reach_outputs(model.graph, model.outputs): #so that all vertices reach outputs
                        b = False
                        for ex_model in temp:
                            if model == ex_model:
                                b = True
                                break
                        if b == False:
                            temp.append(model)
                            #for the same graph, compares if any of the generated models are the same
        all_models += copy.deepcopy(temp)
    return all_models

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def json_write(models, filename):
    with open(filename, 'w') as file:
        for model in models:
            temp = dict()
            temp['graph'] = list(model.graph)
            temp['inputs'] = list(model.inputs)
            temp['outputs'] = list(model.outputs)
            temp['leaks'] = list(model.inputs)
            
            json.dump(temp, file, cls=SetEncoder)