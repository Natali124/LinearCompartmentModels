#ISSUE: list/set conflict

from Models import *
import itertools
import json
import os
import math

#model has graph inputs outputs leaks
    
    


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
        for modper in model.generate_model_isomorphisms():
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
            
        raise KeyError('Model not found in data')
        
    def _inverse_permutation(self, p):
        r = [0] * len(p)
        k = 0
        for i in p:
            r[i] = k
            k += 1
        return r
    
    def filterby(self, f):
        filt = filter(f, self.Data)
        res = dict()
        for item in filt:
            res[item] = self.Data[item]
        return res

        
    def check4_5(self):
        """fmodels = D.filterby(nleaks = 1, inputs_at_least = 1)"""
        def f(m):
            return len(m.leaks) == 1 and len(m.inputs) >= 1
        
        fmodels = self.filterby(f)
        
        r = []
        for k, v in fmodels.items():
            checks = []
            for i, j in v.items():
                if j == "locally":
                    checks.append(i)
            new_m = LinearCompartmentModel(k.graph, k.inputs, k.outputs, [])
            for i in checks:
                if '-1' in i:
                    continue
                elif self._get_result(new_m)[i] == 'locally':
                    print('WORKED')
                else:
                    print('SOMETHING IS PROBABLY WRONG')
                    r.append(k)
        return r
    
    
D = Data('results')

print(D.check4_5())

#some of the parameters are locally identifiable in the initial model, but globally identifiable in the resulting model
        
        
