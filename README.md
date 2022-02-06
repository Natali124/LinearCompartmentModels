# LinearCompartmentModels

Files in the project with important functions. The most important file is GeneratingModels.py

  Bfs.py

    functions:
    
      all_reach_outputs(graph, outputs)
      - checks if all vertices in graph reach at least one output. graph is a list of sets, outputs is a set. 
      e.g. all_reach_outputs([{1}, set()], {0}) == False # True
           all_reach_outputs([{1}, set()], {1}) == True # True
           
      is_connected(graph)
      - checks if graph is connected. Does not take into account that graph is directed. graph is a list of sets.
      e.g. is_connected([{1}, set(), set()]) == False # True
           is_connected([{1}, set(), {1}]) == True # True

  GeneratingGraphs.py

    functions:
      generating_graph_combinations(n)
      - generated a list of all possible graphs with n vertices and no loops
      e.g. generating_graph_combinations(2)
           -> {[set(), {0}], [{1}, {0}]}
           
      Note: Resulting graphs are not lists of sets. They are in the form of Graph objects. Supposing g is an object of class Graph, you can access "list of sets" notation using "g.list". Class Graph is defined in the same file.

  Models.py

    important: here is defined class LinearCompartmentModel
    - constructor: (graph, inputs, outputs, leaks)
      e.g. m = LinearCompartmentModel([{1}, {0,2}, {1}], {0}, {1}, {2})
           m
           -> Graph: [{1}, {0, 2}, {1}], Inputs: {0}, Outputs: {1}, Leaks: {2}

  GeneratingModels.py

    functions:
      generating_models(all_graphs, n_inputs, n_outputs, n_leaks)
      - generates models, taking isomorphisms into consideration. all_graphs is a list of graphs that will be used (possibly using generating_graph_combinations function)
        e.g. generating_models(generating_graph_combinations(2), 1, 1, 1)
        -> [Graph: [set(), {0}], Inputs: {0}, Outputs: {0}, Leaks: {0},
             Graph: [set(), {0}], Inputs: {0}, Outputs: {0}, Leaks: {1},
             Graph: [set(), {0}], Inputs: {1}, Outputs: {0}, Leaks: {0},
             Graph: [set(), {0}], Inputs: {1}, Outputs: {0}, Leaks: {1},
             Graph: [{1}, {0}], Inputs: {0}, Outputs: {0}, Leaks: {0},
             Graph: [{1}, {0}], Inputs: {0}, Outputs: {0}, Leaks: {1},
             Graph: [{1}, {0}], Inputs: {0}, Outputs: {1}, Leaks: {0},
             Graph: [{1}, {0}], Inputs: {0}, Outputs: {1}, Leaks: {1}]

      json_write(models, filename)
      - writes a list of models in the file
        e.g. m = generating_models(generating_graph_combinations(2), 1, 1, 1)
             json_write(m, 'models.json') #creates and writes/writes models in m into models.json file. Important: sets become lists to be compatable with json format
             contents in the file:
             {"graph": [[], [0]], "inputs": [0], "outputs": [0], "leaks": [0]}{"graph": [[], [0]], "inputs": [0], "outputs": [0], "leaks": [0]}{"graph": [[], [0]], "inputs": [1], "outputs": [0], "leaks": [1]}{"graph": [[], [0]], "inputs": [1], "outputs": [0], "leaks": [1]}{"graph": [[1], [0]], "inputs": [0], "outputs": [0], "leaks": [0]}{"graph": [[1], [0]], "inputs": [0], "outputs": [0], "leaks": [0]}{"graph": [[1], [0]], "inputs": [0], "outputs": [1], "leaks": [0]}{"graph": [[1], [0]], "inputs": [0], "outputs": [1], "leaks": [0]}
