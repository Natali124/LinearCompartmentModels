import itertools
import copy
from itertools import chain, combinations

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield list(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield list(pool[i] for i in indices)
        
        
def powerset(iterable):
    "powerset([0,1,2]) --> [] [0] [1] [2] [0,1] [0,2] [1,2] [0,1,2]"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_powerset(n):
    res = list(powerset(range(n)))
    return res
#Here I changed 'combinations' in itertools so that it returns list instead of tuple. 
#As we want to deal with permutations (/changing), list will be more convinient.

#Just powerset = possible connections for each edge.


def prepare_for_vertex(ind, all_connections):
    """removes combinations which contain ind"""
    #creates a new list and puts everything except ones with ind in it
    res = [[]]
    for connection in all_connections:
        res_connection = []
        for number in connection:
            if ind == number:
                res_connection = []
                break
            res_connection.append(number)
        if res_connection != []:
            res.append(res_connection)
    return res

def prepare_for_graph(n):
    """list with lists of connections for each vertex without ind"""
    res = []
    all_connections = get_powerset(n)
    for ind in range(n):
        res.append(prepare_for_vertex(ind, all_connections))
    return res

def generating_graph_combinations(number):
    """generates a list of all possible graphs"""
    pregen_list = prepare_for_graph(number)
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
