# Linear Compartment Models - Creating database and example hypothesis verification

This repository contains code for creating a database of linear compartmental models of up to 4 nodes. We also present already generated database in the folder `results`.

## Working example
The easiest way to query the database is to use class `Data` from the file `IdentifiabilityResults.py`. Constructor takes as an argument the name of the directory where the results are located. For example, below you will find a walk-through example which can be run from the root directory of the repository.

Following prepares an object D of Data class with all our data:

`D = Data('results')`

Now we could use the following code to find all models with 2 nodes and 1 leak which have at least one globally identifiable parameter.

```
def condition(m):
    return len(m.leaks) == 1 and len(m.graph) == 2

filtered_models = D.filterby(condition)

for model, result in filtered_models.items():
    found = False
    for parameter, identifiability in result.items():
        if identifiability == 'globally':
            found = True
            break
    if found:
        print(f'Model: {model}')
        print(f'Result: {result}\n')
```

This will give us the following output:
```
Model: Graph: [set(), {0}], Inputs: {0}, Outputs: {0}, Leaks: {0}
Result: {'(0, -1)': 'globally', '(1, 0)': 'globally'}

Model: Graph: [set(), {0}], Inputs: {1}, Outputs: {0}, Leaks: {0}
Result: {'(0, -1)': 'globally', '(1, 0)': 'globally'}

Model: Graph: [set(), {0}], Inputs: {1}, Outputs: {0}, Leaks: {1}
Result: {'(1, -1)': 'globally', '(1, 0)': 'globally'}

Model: Graph: [{1}, {0}], Inputs: {0}, Outputs: {0}, Leaks: {0}
Result: {'(0, -1)': 'globally', '(0, 1)': 'globally', '(1, 0)': 'globally'}

...
```

Also, we can use any model with up to 4 nodes as a key:
```
model1 = LinearCompartmentModel([[1], [0]], [0, 1], [0], [1])
print(model1)
print(D[model1])

model2 = LinearCompartmentModel([[0], [1]], [1, 0], [1], [0])
print(model2)
print(D[model2])
```

This gives the following output:
```
Graph: [{1}, {0}], Inputs: {0, 1}, Outputs: {0}, Leaks: {1}
{'(1, -1)': 'globally', '(0, 1)': 'globally', '(1, 0)': 'globally'}

Graph: [{0}, {1}], Inputs: {0, 1}, Outputs: {1}, Leaks: {0}
{'(0, -1)': 'globally', '(1, 0)': 'globally', '(0, 1)': 'globally'}
```

We can also directly iterate over (model, result) pairs to achieve the same result as above:
```
for model, result in D:
    if len(model.leaks) == 1 and len(model.graph) == 2:
        found = False
        for parameter, identifiability in result.items():
            if identifiability == 'globally':
                found = True
                break
        if found:
            print(f'Model: {model}')
            print(f'Result: {result}')
            print()

```

## Files explanation with important functions

Files in the project with several most important functions. Models can be generated from the file `GeneratingModels.py`.
Below we present files with important functions.

### GeneratingGraphs.py
- generate_graphs(n) - generates a list of all possible graphs with n vertices and no loops.
Example:
```
generate_graphs(2)
-> {[set(), {0}], [{1}, {0}]}
```
Note: Resulting graphs are not lists of sets. They are in the form of Graph objects. Supposing g is an object of class Graph, you can access "list of sets" notation using "g.list". Class Graph is defined in the same file.

### Models.py
- class LinearCompartmentModel. Constructor: (graph, inputs, outputs, leaks).
Example:
```
m = LinearCompartmentModel([{1}, {0,2}, {1}], {0}, {1}, {2})
print(m)
-> Graph: [{1}, {0, 2}, {1}], Inputs: {0}, Outputs: {1}, Leaks: {2}
```

### GeneratingModels.py
- generate_models(all_graphs, n_inputs, n_outputs, n_leaks) - generates models up to isomorphism. all_graphs is a list of graphs that will be used (e.g. output of generate_graphs function).
```
generate_models(generate_graphs(2), 1, 1, 1)
-> [Graph: [set(), {0}], Inputs: {0}, Outputs: {0}, Leaks: {0},
   Graph: [set(), {0}], Inputs: {0}, Outputs: {0}, Leaks: {1},
   Graph: [set(), {0}], Inputs: {1}, Outputs: {0}, Leaks: {0},
   Graph: [set(), {0}], Inputs: {1}, Outputs: {0}, Leaks: {1},
   Graph: [{1}, {0}], Inputs: {0}, Outputs: {0}, Leaks: {0},
   Graph: [{1}, {0}], Inputs: {0}, Outputs: {0}, Leaks: {1},
   Graph: [{1}, {0}], Inputs: {0}, Outputs: {1}, Leaks: {0},
   Graph: [{1}, {0}], Inputs: {0}, Outputs: {1}, Leaks: {1}]
```
- json_write(model, filename) - writes a list of models in the file. Sets in graphs become lists for easier translation to json format.
Example:
```
models = generate_models(generate_graphs(2), 1, 1, 1)
json_write(models, 'models.json') #writes models in m into models.json file.
```

### graph_helpers.py

- all_reach_outputs(graph, outputs) - checks if all nodes reach outputs.
Example:
```
all_reach_outputs([{1}, set()], {0}) == False # True
all_reach_outputs([{1}, set()], {1}) == True # True
```
- is_connected(graph) - checks if graph is weakly connected. graph is a list of sets.
Example:
```
is_connected([{1}, set(), set()]) == False # True
is_connected([{1}, set(), {1}]) == True # True
```
