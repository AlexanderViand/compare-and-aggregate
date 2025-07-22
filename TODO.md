# Building a GPU-enabled FSS/ArithSS switching compiler

## Tasks
1. See if the ezPC/mpc-gpu/fss stuff actually works
1. Are there any other GPU MPC libraries we should consider and/or benchmark?
1. Add ASS to ezPc/mpc-gpu (hopefully with loits of AI coding help)
    * Already has beaver triple generation/etc in the various FSS things, probably just needs to be wrapped in a nice API
    * How easy would it be to re-use existing matmul/etc code for ASS as well? --> They already use just that!
    * Implement A2B/B2A and basic binary comparison/etc logic
    * Implement whatever SOTA for non-FSS based sorting is (some kind of modified quicksort?)
      -> implies implementing comparisons, too
    * Does the GPU-FSS version have DCF? NO: **port their CPU FSS DCF to GPU FSS code**
    * Re-implementing Compare-and-Aggregate CCS'24 sorting magic

1. Benchmarking for cost model
    * Share conversions
    * Comparisons
    * Sorting (with CA magic)
    * ~~Matmuls~~ (not really sensible under FSS)

1. FIGURE OUT WHAT OUR CONTRIBUTION IS TO CONVINCE TOP TIER REVIEWS


1. Explore Python xDSL vs C++ MLIR 
1. Explore ML -> compiler pathways

## Goals (and non-goals)
1. We should throw in Transformers/AI since we have the code from orca/sigma "for free", just need a ONNX export or StableHLO or something like that.
1. 2 PC setting (-> trusted external dealer) (makes it easy to compare against FHE - not in the paper, just for keeping Intel managers happy)
1. Integration with MLIR/HEIR-like things (even if only superficial: makes it easier to sell the proejct at Intel beyond terms of visiting)
1. **LUTs**?
1. "THE" MPC compiler for the (GPU, FSS, etc using) Future


# Non-Goals
1. 3 PC settings
2. distributed key generation