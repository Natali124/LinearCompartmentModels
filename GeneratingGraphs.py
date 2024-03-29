import copy
from itertools import chain, combinations
from Models import compare_graphs
from graph_helpers import is_connected


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
    return list(powerset(range(n)))
#endregion

#Here I changed 'combinations' in itertools so that it returns set instead of tuple.
#Just powerset = possible connections for each edge.

def prepare_for_vertex_set(ind, all_connections):
    """"removes sets which contain ind"""
    #creates a new list and put every set all_connections have apart from ones that 
    #contain ind.
    
    res = []
    for set in all_connections:
        if ind not in set:
            res.append(set.copy())
    return res

def prepare_for_graph_set(n):
    """list with lists of connections for each vertex without ind"""
    res = []
    all_connections = get_powerset(n)
    for ind in range(n):
        res.append(prepare_for_vertex_set(ind, all_connections))
        
    return res

def generate_graphs(number):
    """
        set notation: generates a list of all possible connected graphs with no loops
        takes isomorphisms into consideration.
    """
    pregen_list = prepare_for_graph_set(number)
    res = set()
    l = Graph([])
    def _rec (n):
        if n == number:
            if is_connected(l.list): #we use only connected graphs
                res.add(copy.deepcopy(l))
            return
        for i in pregen_list[n]:
            l.list.append(i)
            _rec (n+1)
            l.list.pop()
    _rec(0)
    return res


class Graph:
    """"Graph.list gives list/set notation of the graph. Hashable."""
    def __init__(self, list):
        self.list = list
    
    def __eq__(self, another):
        return compare_graphs(self.list, another.list)
    
    def __repr__(self):
        return f'Graph({str(self.list)})'
    
    def __len__(self):
        return len(self.list)
    
    def __hash__(self):
        sum = 0
        for s in self.list:
            sum += len(s)
        return sum
