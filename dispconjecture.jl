using Base.Filesystem
using StructuralIdentifiability: assess_identifiability, linear_compartment_model, var_to_str

res1 = assess_identifiability(linear_compartment_model([[2], [1, 3], [1, 2]], [1, 2], [2], [1]))
res2 = assess_identifiability(linear_compartment_model([[2], [1, 3], [1, 2]], [1,2], [3], [1]))
res3 = assess_identifiability(linear_compartment_model([[2], [1, 3], [1, 2]], [1, 3], [3], [1]))
res4 = assess_identifiability(linear_compartment_model([[2, 3], [1, 3], [1, 2]], [1, 2], [1], [2]))
res5 = assess_identifiability(linear_compartment_model([[2, 3], [1, 3], [1, 2]], [1, 2], [3], [2]))

res1a = assess_identifiability(linear_compartment_model([[2], [1, 3], [1, 2]], [1, 2], [2], Vector{Int64}()))
res2a = assess_identifiability(linear_compartment_model([[2], [1, 3], [1, 2]], [1,2], [3], Vector{Int64}()))
res3a = assess_identifiability(linear_compartment_model([[2], [1, 3], [1, 2]], [1, 3], [3], Vector{Int64}()))
res4a = assess_identifiability(linear_compartment_model([[2, 3], [1, 3], [1, 2]], [1, 2], [1], Vector{Int64}()))
res5a = assess_identifiability(linear_compartment_model([[2, 3], [1, 3], [1, 2]], [1, 2], [3], Vector{Int64}()))

println("--------Model 1: --------")
println("Before: ")
println(res1)
println("After: ")
println(res1a)
println("--------Model 2: --------")
println("Before: ")
println(res2)
println("After: ")
println(res2a)
println("--------Model 3: --------")
println("Before: ")
println(res3)
println("After: ")
println(res3a)
println("--------Model 4: --------")
println("Before: ")
println(res4)
println("After: ")
println(res4a)
println("--------Model 5: --------")
println("Before: ")
println(res5)
println("After: ")
println(res5a)