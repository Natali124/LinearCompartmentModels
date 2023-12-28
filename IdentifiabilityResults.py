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
        """
        for modper in model.generate_model_isomorphisms():
            if modper[0] in self.Data:
                bpermd = self.Data[modper[0]]

                d = dict()
                for (parameter, identifiability) in bpermd.items():
                    r1 = int(parameter[1])
                    if parameter[4] == '-':
                        r2 = -1
                    else:
                        r2 = int(parameter[4])
                    parameter = (r1, r2)
                    # parameter is parsed, tuple of ints instead of string
                    if r2 == -1:
                        # if contains leak...
                        r = permute_set([r1], self._inverse_permutation(modper[1]))
                        r.add(-1)
                        r = str(tuple(r))
                    else:
                        inv_perm = self._inverse_permutation(modper[1])
                        temp1 = inv_perm[r1]
                        temp2 = inv_perm[r2]

                        r = str((temp1, temp2))
                    d[r] = identifiability
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
            return len(m.leaks) == 1 and len(m.inputs) >= 1 and len(m.graph) <= 3
        
        fmodels = self.filterby(f)
        
        r = []
        for k, v in fmodels.items():
            checks = []
            for i, j in v.items():
                if j == "locally" or j == 'globally':
                    checks.append(i)
            new_m = LinearCompartmentModel(k.graph, k.inputs, k.outputs, [])
            for i in checks:
                if '-1' in i:
                    continue
                elif i not in self[new_m]:
                    continue
                elif self[new_m][i] == 'locally' or self[new_m][i] == 'globally':
                    #print('WORKED')
                    continue
                elif self[new_m][i] == 'nonidentifiable':
                    #print('SOMETHING IS WRONG')
                    r.append(k)
        return r
    
    
D = Data('results')

#print(len(D.check4_5()))

model = LinearCompartmentModel([[1], [0]], [0, 1], [0], [1])
print(model)

print()
print(D[model])
print()

model2 = LinearCompartmentModel([[0], [1]], [1, 0], [1], [0])
print(model2)
print()
print(D[model2])
#print(D.Data[model2])