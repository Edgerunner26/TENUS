import m5
from m5.objects import *
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

print("------ KICKING OFF GEM5 SUPERSCALAR SIMULATION ------")
print("Superscalar Width=8, SMT=False")

processor = SimpleProcessor(
    cpu_type=CPUTypes.O3,
    isa=ISA.X86,
    num_cores=1
)

# Superscalar width settings
for cpu in processor.get_cores():
    cpu.core.fetchWidth = 8
    cpu.core.decodeWidth = 8
    cpu.core.renameWidth = 8
    cpu.core.dispatchWidth = 8
    cpu.core.issueWidth = 8
    cpu.core.wbWidth = 8
    cpu.core.commitWidth = 8
    cpu.core.numROBEntries = 256
    cpu.core.numPhysIntRegs = 512
    cpu.core.numPhysFloatRegs = 512

cache_hierarchy = NoCache()
memory = SingleChannelDDR3_1600(size="2GB")

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy
)

binary = obtain_resource("x86-hello64-static")
board.set_se_binary_workload(binary)

simulator = Simulator(board=board)
simulator.run()

stats = simulator.get_stats()
print("Superscalar Simulation Complete")
