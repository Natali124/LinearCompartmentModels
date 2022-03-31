import os

from GeneratingModels import *

folder = "models/"
try:
    os.mkdir(folder)
except FileExistsError:
    pass

MAX_N = 4

for n in range(2, MAX_N + 1):
    graphs = generate_graphs(n)
    for leaks in range(n + 1):
        for inputs in range(3):
            models = generate_models(graphs, inputs, 1, leaks)
            json_write(models, folder + f"models_n{n}_i{inputs}_o{1}_l{leaks}.json")
