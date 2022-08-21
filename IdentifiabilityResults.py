#ISSUE: list/set conflict

from Models import *
import itertools
import json
import os
import math

#model has graph inputs outputs leaks

#to do:
    #add a strongly connected function

class Data:
    
    Data = dict()
    
    def __init__(self, directory):
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                self._json_read(f)
                
    def _json_read(self, filename):
        with open(filename, 'r') as file:
            for model in file:
                md = json.loads(model)
                m = LinearCompartmentModel(md['graph'], md['inputs'], md['outputs'], md['leaks'])
                self.Data[m] = md['result']
                
    def __getitem__(self, key):
        return self._get_result(key)
    
    def _get_result(self, model):
        """
        Only works under 10 (0 through 9) vertices
        Possible bug: returns in list notation, not with ( ) s, not changing yet because I'm not sure what is the best
        """
        for modper in self._generate_model_isomorphisms(model):
            if modper[0] in self.Data:
                bpermd = self.Data[modper[0]]
                d = dict()
                for (k, v) in bpermd.items():
                    r1 = int(k[1])
                    if k[4] == '-':
                        r2 = -1
                    else:
                        r2 = int(k[4])
                    k = [r1, r2]
                    if r2 == -1:
                        r = permute_set([r1], self._inverse_permutation(modper[1]))
                        r.append(-1)
                        r = str(r)
                    else:
                        r = str(permute_set(k, self._inverse_permutation(modper[1])))
                    d[r] = v
                return d
            
        print('NOT FOUND')
        
    def _inverse_permutation(self, p):
        r = [0] * len(p)
        k = 0
        for i in p:
            r[i] = k
            k += 1
        return r
    
    def _generate_model_isomorphisms(self, base_model):
        """
        generates all isomorphisms of a model in a sorted way
        result is a list of tuples - model and permutation
        """
        
        result = []
        n = len(base_model.graph)
       
        vertices_list = list(range(n))
        permutations_object = itertools.permutations(vertices_list)
        #creating a permutations object
        
        for permutation in permutations_object:
            model_new = LinearCompartmentModel(permute_graph(base_model.graph,permutation), 
                                               permute_set(base_model.inputs, permutation),
                                               permute_set(base_model.outputs, permutation),
                                               permute_set(base_model.leaks, permutation)
                                               )
            result.append((model_new, permutation))
       
        return result
    
    def filterby(self, **params):
        """
        ninputs = int
        noutputs = int
        nleaks = int
        
        inputs_at_least = int
        outputs_at_least = int
        leaks_at_least = int
        
        inputs_at_most = int
        outputs_at_most = int
        outputs_at_most = int
        
        strongly_connected = True (default is False)
        """
        #set up:
        res = dict()
        #inputs
        inpmax = math.inf
        inpmin = -math.inf
        
        if 'ninputs' in params:
            inpmax = params['ninputs']
            inpmin = inpmax
        else:
            if 'inputs_at_least' in params:
                inpmin = params['inputs_at_least']
            if 'inputs_at_most' in params:
                inpmax = params['inputs_at_most']
        #outputs
        outpmax = math.inf
        outpmin = -math.inf
        
        if 'noutputs' in params:
            outpmax = params['noutputs']
            outpmin = outpmax
        else:
            if 'outputs_at_least' in params:
                outpmin = params['outputs_at_least']
            if 'outputs_at_most' in params:
                inpmax = params['outputs_at_most']
        #leaks
        leaksmin = math.inf
        leaksmax = -math.inf
        
        if 'nleaks' in params:
            leaksmin = params['nleaks']
            leaksmax = leaksmin
        else:
            if 'leaks_at_least' in params:
                leaksmin = params['leaks_at_least']
            if 'leaks_at_most' in params:
                leaksmax = params['leaks_at_most']
                
        
        for m in self.Data:
            if len(m.leaks) >= leaksmin and len(m.leaks) <= leaksmax and \
                len(m.inputs) >= inpmin and len(m.inputs) <= inpmax and \
                    len(m.outputs) >= outpmin and len(m.outputs) <= outpmax:
                        if 'strongly_connected' in params:
                            if params['strongly_connected'] == True:
                                if self._strongly_connected(m):
                                    res[m] = Data[m]
                        else:
                            res[m] = self.Data[m]
                            
        return res
    
    def _strongly_connected(self, graph):
            pass
        
    def check4_5(self, res):
        """res = D.filterby(nleaks = 1, inputs_at_least = 1)"""
        r = []
        for k, v in res.items():
            checks = []
            for i, j in v.items():
                if j == "locally":
                    checks.append(i)
            new_m = LinearCompartmentModel(k.graph, k.inputs, k.outputs, [])
            for i in checks:
                if '-1' in i:
                    continue
                elif self.Data[new_m][i] == 'locally':
                    print('WORKED')
                else:
                    print('SOMETHING IS PROBABLY WRONG')
                    r.append(k)
        return r
        
        