using Base.Filesystem
using Nemo
using JSON
using StructuralIdentifiability: assess_identifiability, linear_compartment_model, var_to_str, find_ioequations, eval_at_dict

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
    ioeq = first(values(find_ioequations(model)))

    return ioeq
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

function get_ioeqs!(io_collection, fname)
    println("Processing $fname")
    models = read_models(fname)
    for (i, m) in enumerate(models)
        println("\tProcessing model $i out of $(length(models))")
        result = run_model(m["graph"], m["inputs"], m["outputs"], m["leaks"])
        io_collection[m] = result
   end
end

# -----------------------------------------------------------------------------

function get_vars(poly)
    total = vars(poly)
    params = [v for v in total if var_to_str(v)[1] == 'a']
    iovars = [v for v in total if !(v in params)]

    return (params, iovars)
end

function permutations(arr)
    if length(arr) == 1
        return [[arr[1]]]
    end
    prev = permutations(arr[1:length(arr) - 1])
    result = []
    for p in prev
        for i in 1:length(arr)
            push!(result, vcat(p[1:i - 1], [arr[end]], p[i:end]))
        end
    end
    return result
end

function polys_match(poly1, poly2)
    (params1, iovars1) = get_vars(poly1)
    (params2, iovars2) = get_vars(poly2)

    eval_base = Dict{fmpq_mpoly, fmpq_mpoly}()
    for v in iovars1
        u = findfirst(u -> var_to_str(u) == var_to_str(v), iovars2)
        if isnothing(u)
            return false
        end
        eval_base[v] = iovars2[u]
    end

    if length(params1) != length(params2)
        return false
    end

    for p in permutations(params2)
        evald = copy(eval_base)
        for i in 1:length(p)
            evald[params1[i]] = p[i]
        end
        if eval_at_dict(poly1, evald) == poly2
            return true
        end
    end
    return false
end

# -----------------------------------------------------------------------------

io_collection = Dict()
folder = "models/"
files = [
    "models_n3_i0_o1_l0.json",
    "models_n3_i0_o1_l1.json",
    "models_n3_i0_o1_l2.json",
    "models_n3_i0_o1_l3.json"
]
fnames = [folder * fname for fname in files]

for f in fnames
    get_ioeqs!(io_collection, f)
end

buckets = []
for (k, v) in io_collection
    added = false
    for b in buckets
        if polys_match(v, b[end][2])
            added = true
            push!(b, (k, v))
            break
        end
    end
    if !added
        push!(buckets, [(k, v)])
    end
    println("Processed")
end
for b in buckets
    println("Bucket of length $(length(b))")
    for m in b
        println(m)
    end
end
