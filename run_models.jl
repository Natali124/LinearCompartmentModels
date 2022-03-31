using Base.Filesystem
using JSON
using StructuralIdentifiability: assess_identifiability, linear_compartment_model, var_to_str

# produces the identifiability information for a linear compartment model
# Input:
#   - graph: adjacency list (as an array of arrays of integers)
#   - inputs, outputs, leaks: arrays of leaks, input, and output nodes, respectively
# Output: dictionary of the form edge (as a tuple of integers) => nonidentifiable/locally/globally
# ყურადღება: for input and output the python (ie zero-based) indexing is used, leaks a edges to -1
function run_model(graph, inputs, outputs, leaks)
    graph_jl = [Array{Int, 1}([i + 1 for i in v]) for v in graph]
    leaks_jl = Array{Int, 1}([i + 1 for i in leaks])
    inputs_jl = Array{Int, 1}([i + 1 for i in inputs])
    outputs_jl = Array{Int, 1}([i + 1 for i in outputs])

    model = linear_compartment_model(graph_jl, inputs_jl, outputs_jl, leaks_jl)
    id_result_row = assess_identifiability(model)

    id_result = Dict()
    for (var, id_res) in id_result_row 
        # indices are tricky!
        src = split(var_to_str(var), "_")[3]
        dest = split(var_to_str(var), "_")[2]
        id_result[(parse(Int64, src) - 1, parse(Int64, dest) - 1)] = String(id_res)
    end

    return id_result
end

# -----------------------------------------------------------------------------

# Takes a name of JSON file and returns a list of models there
function read_models(fname)
    models = Array{Any, 1}()
    open(fname, "r") do f
        while !eof(f)
            line = readline(f)
            push!(models, JSON.parse(line))
        end
    end
    return models
end

# -----------------------------------------------------------------------------

# Checks identifiability for all the models in `fname` and writes a result into a file in `dest_folder`
function process_file(fname, dest_dir)
    println("Processing $fname")
    models = read_models(fname)
    for (i, m) in enumerate(models)
        println("\tProcessing model $i out of $(length(models))")
        result = run_model(m["graph"], m["inputs"], m["outputs"], m["leaks"])
        m["result"] = result
   end

   out_fname = dest_dir * split(split(fname, "/")[end], ".")[1] * "_result.json"
   open(out_fname, "w") do f
       for m in models
           write(f, JSON.json(m))
           write(f, "\n")
       end
   end
end

# -----------------------------------------------------------------------------

src_dir = "models/"
dest_dir = "results/"
#Filesystem.mkdir(dest_dir)
for fname in Filesystem.readdir(src_dir, join=true)
    process_file(fname, dest_dir)
end
