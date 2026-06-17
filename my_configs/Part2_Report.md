## 1. Tradeoffs of opLat vs issueLat
The configuration of the `FloatSimdFU` drastically influences the pipeline's structural hazards. A configuration of `opLat=1, issueLat=6` computes operations quickly but introduces a 6-cycle recovery bottleneck, forcing subsequent instructions to stall in the issue queue. Conversely, `opLat=6, issueLat=1` introduces high operational latency but allows the unit to accept a new instruction every single cycle.

## 2. Optimal Balance for Parallel Speedup
The data consistently demonstrates that for highly parallel, vector-based workloads like Daxpy, the heavily pipelined configuration (`opLat=6, issueLat=1`) yields the optimal parallel speedup. Because individual threads compute independent array elements, they do not suffer from read-after-write (RAW) data hazards. Therefore, execution throughput (`issueLat`) is vastly more important than the latency of a single operation (`opLat`). 

## 3. Limitations of the Model
The primary limitation of this exploration is the strict in-order nature of `MinorCPU`. Because it cannot dynamically reorder instructions to hide latency (like an Out-of-Order processor), a high `issueLat` strictly stalls the entire pipeline. In a modern O3 core, the scheduler would simply issue integer or memory operations while waiting for the floating-point unit to become available, partially mitigating the penalty of a poorly balanced functional unit.

## 4. Other Factors Influencing TLP
Beyond functional unit latencies, Thread-Level Parallelism in this real-world application is heavily bound by the **Memory Wall**. The Daxpy kernel is memory-bound (requiring multiple array reads and writes per compute operation). As thread counts scale to 4 and 8, cache coherence overhead, L2 cache contention, and main memory bandwidth limits will increasingly bottleneck performance, overriding the pipeline optimizations according to Amdahl's Law.
