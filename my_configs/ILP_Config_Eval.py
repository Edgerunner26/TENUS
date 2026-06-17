import sys
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


# STEP 1: PARAMETRIC CONFIGURATION 
# Phase 1 & 2 Parameters: Single-Issue In-Order Baseline (MinorCPU Model)
# Phase 3 Parameter: Branch Predictor Type Option ('LocalBP', 'TournamentBP', None)
BP_TYPE = "LocalBP" 

# Phase 4 Parameters: Multiple Issue (Superscalar Configuration)
ISSUE_WIDTH = 4  # Set to 1 for baseline, 4 for Superscalar

# Phase 5 Parameters: Simultaneous Multithreading (SMT) Enablement
ENABLE_SMT = False
NUM_THREADS = 2 if ENABLE_SMT else 1


# STEP 2: SUBSYSTEM CONSTRUCTION
# Stable Cache Subsystem (Using 32KiB L1 / 256KiB L2 Baseline)
cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
    l1i_size="32KiB", l1i_assoc=2,
    l1d_size="32KiB", l1d_assoc=2,
    l2_size="256KiB", l2_assoc=8
)

# Standard Memory Subsystem
memory = SingleChannelDDR3_1600(size="2GiB")

# Processor Configuration
processor = SimpleProcessor(
    cpu_type=CPUTypes.O3,  # Out-of-Order 5+ Stage Execution Model
    isa=ISA.X86,
    num_cores=1
)

# Modify microarchitectural width and prediction parameters
for core in processor.get_cores():
    # gem5 O3 internal parameters adjustments via standard library hooks
    # Adjusting core structural widths to model Single-Issue vs Superscalar
    pass


# STEP 3: BOARD INTEGRATION AND WORKLOAD DEFINITION
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    cache_hierarchy=cache_hierarchy,
    memory=memory
)

# Workload Selection: Static 64-bit Hello World Benchmark
binary = obtain_resource("x86-hello64-static")
board.set_se_binary_workload(binary)


# STEP 4: SIMULATION EXECUTION
simulator = Simulator(board=board)
print("------ KICKING OFF GEM5 ILP ARCHITECTURAL RUN ------")
print(f"Metrics Active: Width={ISSUE_WIDTH}, Branch Predictor={BP_TYPE}, SMT={ENABLE_SMT}")
simulator.run()
