import itertools
import copy
from itertools import chain, combinations


#region
def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield set(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield set(pool[i] for i in indices)
        
def powerset(iterable):
    "gives power set as an iterable object of sets"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_powerset(n):
    res = list(powerset(range(n)))
    return res
#endregion

#Here I changed 'combinations' in itertools so that it returns set instead of tuple.
#Just powerset = possible connections for each edge.


def prepare_for_vertex_set(ind, all_connections):
    """"removes sets which contain ind"""
    #creates a new list and put every set all_connections have apart from ones that 
    #contain ind.
    
    #suggestion: if instead of all_connections, we directly generate here, we do not need 
    #that many copying.
    #problem: generating every time = copying every time (maybe)
    #so maybe keep it this way.
    
    res = []
    for set in all_connections:
        if ind not in set:
            res.append(set.copy())
            #difference between .copy() and copy.deepcopy()?
    return res

def prepare_for_graph_set(n):
    """list with lists of connections for each vertex without ind"""
    res = []
    all_connections = get_powerset(n)
    for ind in range(n):
        res.append(prepare_for_vertex_set(ind, all_connections))
    return res

def generating_graph_combinations(number):
    """generates a list of all possible graphs with no loops"""
    pregen_list = prepare_for_graph_set(number)
    res = []
    l = []
    def func (n):
        if n == number:
            res.append(copy.deepcopy(l))
            return
        for i in pregen_list[n]:
            l.append(i)
            func (n+1)
            l.pop()
    func(0)
    return res