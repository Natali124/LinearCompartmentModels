using Base.Filesystem
using Dates
using Distributed
using Nemo
using JSON
using StructuralIdentifiability: assess_identifiability, linear_compartment_model, var_to_str, find_ioequations, 
    eval_at_dict, str_to_var, parent_ring_change, ODE
@everywhere using Groebner

#F = GF(7879)
F = QQ

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

    model = linear_compartment_model_extra(graph_jl, inputs_jl, outputs_jl, leaks_jl)
    ioeqs = find_ioequations(model)
    ioeq = first(values(ioeqs))
    leadvar = first(keys(ioeqs))
    FFring, _ = PolynomialRing(F, map(var_to_str, gens(parent(ioeq))))
    ioeq = parent_ring_change(ioeq, FFring) * (1 // F(coeff(ioeq, leadvar)))

    return ioeq
end

# -----------------------------------------------------------------------------

function linear_compartment_model_extra(graph, inputs, outputs, leaks)
    "Adapted from StructuralIdentifiability.jl"
    n = length(graph)
    x_vars_names = ["x$i" for i in 1:n]
    y_vars_names = ["y$i" for i in outputs]
    u_vars_names = ["u$i" for i in inputs]
    edges_vars_names = Array{String, 1}()
    for i in 1:n
        for j in graph[i]
            push!(edges_vars_names, "a_$(j)_$(i)")
        end
    end
    for s in leaks
        push!(edges_vars_names, "a_0_$(s)")
    end
    for u in inputs
        push!(edges_vars_names, "b_$u")
    end

    R, vars = PolynomialRing(
        QQ, vcat(x_vars_names, y_vars_names, u_vars_names, edges_vars_names),
    )
    x_vars = @view vars[1:n]
    x_equations = Dict{fmpq_mpoly, Union{fmpq_mpoly, Generic.Frac{fmpq_mpoly}}}(
        x => R(0) for x in x_vars
    )
    for i in 1:n
        for j in graph[i]
            rate = str_to_var("a_$(j)_$(i)", R)
            x_equations[x_vars[j]] += x_vars[i] * rate
            x_equations[x_vars[i]] -= x_vars[i] * rate
        end
        if i in leaks
            rate = str_to_var("a_0_$(i)", R)
            x_equations[x_vars[i]] += -x_vars[i] * rate
        end
        if i in inputs
                x_equations[x_vars[i]] += str_to_var("b_$i", R) * str_to_var("u$i", R)
        end
    end

    y_equations = Dict{fmpq_mpoly, Union{fmpq_mpoly, Generic.Frac{fmpq_mpoly}}}(
        str_to_var("y$i", R) => str_to_var("x$i", R) for i in outputs
    )

    return ODE{fmpq_mpoly}(
        x_equations,
        y_equations,
        Array{fmpq_mpoly}([str_to_var("u$i", R) for i in inputs]),
    )
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

function print_model(model)
        println("  Model of dimension $(length(model["graph"]))")
    println("    Outputs at nodes $(join(model["outputs"], ", ")), leaks at nodes $(join(model["leaks"], ", ")), inputs at nodes $(join(model["inputs"], ", "))")
    for i in 0:(length(model["graph"]) - 1)
        println("    Edges from $i : $(join(model["graph"][i + 1], ", "))")
    end
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

# from https://stackoverflow.com/questions/53023386/set-a-time-limitation-on-algorithm-in-julia

function run_with_timeout(timeout::Int,f::Function, wid::Int)
    result = RemoteChannel(()->Channel{Tuple}(1));
    @spawnat wid put!(result, (f(), myid()))
    res = (:timeout, wid)
    time_elapsed = 0.0
    while time_elapsed < timeout && !isready(result)
        sleep(0.5)
        time_elapsed += 0.5
    end
    if !isready(result)
        println("Timeout! at $wid")
    else
        res = take!(result)
    end
    return res
end

function runTask(origtask:: Task, timeoutms:: Int)
    startTime = Dates.datetime2epochms(now())

    function internal_task(taskFinished)
        try
            schedule(origtask)
            yield()
            wait(origtask)
            if istaskdone(origtask)
                taskFinished[] = true
                Base.task_result(origtask)
            else
                throw(ErrorException("Task is not done even after wait() for it to finish - something is wrong"))
            end
        catch e
            @warn "Error while processing task: $e"
            taskFinished[] = true
            missing
        end
    end

    taskFinished = Threads.Atomic{Bool}(false)
    thread = Threads.@spawn internal_task(taskFinished)
    while !taskFinished[] && (Dates.datetime2epochms(now()) - startTime) < timeoutms
        println("X", Dates.datetime2epochms(now()) - startTime)
        sleep(0.1)
        println("Y")
    end
    if taskFinished[]
        return fetch(thread)
    end
    # Task timeouted
    println("Timeout!")
    origtask.exception = InterruptException()
    println("Interrupted!")
    return missing
end # function

# -----------------------------------------------------------------------------

function get_vars(poly)
    total = vars(poly)
    params = [v for v in total if var_to_str(v)[1] in ('a', 'b')]
    iovars = [v for v in total if !(v in params)]

    return (params, iovars)
end

function get_coeff(p, letter, ord)
    vind = findfirst(v -> (var_to_str(v)[1] == letter) && endswith(var_to_str(v), "$ord"), vars(p))
    if isnothing(vind)
        return zero(parent(p))
    end
    return derivative(p, vars(p)[vind])
end

function get_relations_ideal(p, maxord, R)
    coeffs = []
    for i in 0:maxord
        push!(coeffs, get_coeff(p, 'y', i))
    end
    for i in 0:maxord
        push!(coeffs, get_coeff(p, 'u', i))
    end

    (params, iovars1) = get_vars(p)

    RR, _ = PolynomialRing(F, vcat(map(var_to_str, params), ["Y$i" for i in 0:maxord], ["U$i" for i in 0:maxord]))
    eqs = []
    for i in 0:maxord
        push!(eqs, str_to_var("Y$i", RR) - parent_ring_change(coeffs[i + 1], RR))
        push!(eqs, str_to_var("U$i", RR) - parent_ring_change(coeffs[i + maxord + 2], RR))
    end

    gbtask = @task begin; return groebner(eqs); end
    gb = runTask(gbtask, 100)
    if ismissing(gb)
        gb = []
    end
    """
    @everywhere function ff()
        return groebner(eqs)
    end
    wid = addprocs(1)[1]
    (gb, wid) = run_with_timeout(20, ff, wid)
    rmprocs(wid)
    if gb == :timeout
        println("Timeout for p")
        gb = []
    end
    """

    res = []
    for poly in gb
        if all([(var_to_str(v)[1] == 'U') || (var_to_str(v)[1] == 'Y') for v in vars(poly)])
            push!(res, parent_ring_change(poly, R))
        end
    end

    #el = @elapsed res = groebner(eqs)
    #@info "Elapsed $el"
    return res
end

# -----------------------------------------------------------------------------

io_collection = Dict()
folder = "../models/"
files = [
    #"models_n2_i1_o1_l0.json",
    #"models_n2_i1_o1_l1.json",
    #"models_n2_i1_o1_l2.json"
    "models_n3_i1_o1_l0.json",
    "models_n3_i1_o1_l1.json",
    "models_n3_i1_o1_l2.json",
    "models_n3_i1_o1_l3.json"
]
fnames = [folder * fname for fname in files]

for f in fnames
    get_ioeqs!(io_collection, f)
end

ord = 3
R, _ = PolynomialRing(F, vcat(["Y$i" for i in 0:ord], ["U$i" for i in 0:ord]))

total = Dict()
ind = 0

for (m, eq) in io_collection
    rels = get_relations_ideal(eq, ord, R)
    println(m)
    println(rels)
    println("===========")
    if haskey(total, rels)
        push!(total[rels], m)
    else
        total[rels] = [m]
    end
    println(ind)
    flush(stdout)
    global ind += 1
end

for (k, v) in total
    println("Relations $k in $(length(v)) models")
    for m in v
        print_model(m)
    end
    println("========")
end
