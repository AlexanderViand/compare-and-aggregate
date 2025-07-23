# Building a GPU-enabled FSS/ArithSS switching compiler

## Motivation

Popular generic MPC compilers and runtimes (e.g., MP‑SPDZ, SCALE‑MAMBA, Sharemind, ABY/ABY3) stil rely primarily on additive, Boolean, or GC shares. 
They can call external FSS-based sub‑routines (e.g., for PIR), but the compiler does not reason about FSS or generate FSS keys natively.

FSS trades off excellent (online) communication with increased computation, and is therefore more compute-bound than tradiional MPC techniques.
As a result, it benefits massively from GPU acceleration, as demonstrated by recent secure Transformer inference works such as Orca/Sigma, which
implement FSS-based MPC on GPU to great effect. 
However, no MPC compilers support GPU backends, and even the few GPU-enabled frameworks have very limited features compared to their CPU versions. 

Beyond the very limited implementation for the CCS'24 paper, there is no work exploiting the (additive) "aggregability" of FSS-based MPC,
which should give significant improvements to a range of applications beyond just simple sorting.
In addition to the CCS'24 paper, there are also a variety of other FSS (manual) "optimization" papers, e.g.,
work on reducing operations that would naively consume multiple DCF calls into single DCF calls 
(Used for ReLU/any pieceswise linear function in Eurocrypt'21, Boyle et al., w/ Mayank).
Beyond this, there is a range of key-size reduction optimizations in the literature that could be targets for formalization into optimization patterns.

Note: For AI workloads, most of the MPC-adaption work can be done once, in the form of expert-written kernels for a handful of key operators (e.g., matmul, GELU, etc),
but this is not the case for more generic programs (e.g., custom auctions, etc.)

Generic applications (with a CA-focus):
* Auctions (k-price auction is directly a ranking problem)
* Graph Problems (shortest path, etc) also tend to involve a lot of sorting


## Tasks
1. See if the ezPC/mpc-gpu/fss stuff actually works
   It **seems to run**, but it's not very convenient / does not give great output
1. Are there any other GPU MPC libraries we should consider and/or benchmark?
   Piranha (a few MPC primitives, but no FSS)
   CryptGPU (CrypTen for GPU) - only supports RSS
   Spin (?) - details not quite clear, but no FSS anyway
1. Add LSS API to ezPc/mpc-gpu (hopefully with loits of AI coding help)
    * Already has beaver triple generation/etc in the various FSS things, probably just needs to be wrapped in a nice API
    * How easy would it be to re-use existing matmul/etc code for LSS as well? --> They already use just that!
    * Implement A2B/B2A and basic binary comparison/etc logic
    * ~~Implement whatever SOTA for non-FSS based sorting is (some kind of modified quicksort?)~~
      -> implies implementing comparisons, too
    * Does the GPU-FSS version have DCF? ~~If not, port their CPU FSS DCF to GPU FSS code~~
      It actually does, it's in /dcf/gpu_dcf.cu
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

## Contributions
* Additive Aggregation paradigm (generalization of CA), and show that it significantly speeds up several classes of applications
* reduce amount of custom optimizations required
* re-implement a bunch of sota FSS-based things (PIR, ML, etc) that were originally hand-written for CPU,
  showing that both (i) it takes very little effort (a few hundred LoC per paper) to implement them using the compiler
  and (ii) because of the automagic GPU acceleration, the sota is now much faster
*  


# Non-Goals
1. 3 PC  or 3+ PC settings
2. distributed key generation