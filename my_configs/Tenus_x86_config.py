import sys
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


# STEP 1: LOW-POWER CACHE HIERARCHY DESIGN

# Implementing a power-conscious, highly localized cache matrix
cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
    l1i_size="16KiB", l1i_assoc=2,  # Streamlined capacity to lower leakage current
    l1d_size="16KiB", l1d_assoc=2,
    l2_size="128KiB", l2_assoc=4   # Smaller L2 capacity minimizes tag-matching power
)


# STEP 2: MEMORY SYSTEM

memory = SingleChannelDDR3_1600(size="1GiB")


# STEP 3: TENUS IN-ORDER PIPELINE

processor = SimpleProcessor(
    cpu_type=CPUTypes.MINOR,  # Enforces an in-order pipeline for power efficiency
    isa=ISA.X86,
    num_cores=1
)


# STEP 4: BOARD INTEGRATION & CLOCK DOMAIN MANAGEMENT

board = SimpleBoard(
    clk_freq="1.5GHz",  # Downclocked frequency to scale down dynamic power (P proportional to f)
    processor=processor,
    cache_hierarchy=cache_hierarchy,
    memory=memory
)

# Bind the standard static workload to the SE (Syscall Emulation) layer
binary = obtain_resource("x86-hello64-static")
board.set_se_binary_workload(binary)


# STEP 5: SIMULATION INITIALIZATION

simulator = Simulator(board=board)
print("Initializing gem5 TENUS Low-Power X86 Implementation Suite...")
simulator.run()
