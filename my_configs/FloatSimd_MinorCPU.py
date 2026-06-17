import argparse
import m5
from m5.objects import *

# 1. Setup Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument("--threads", type=int, default=2)
parser.add_argument("--opLat", type=int, default=2)
parser.add_argument("--issueLat", type=int, default=1)
args = parser.parse_args()

# 2. Build your System (Assuming standard SE configuration)
system = System()
# ... [Your existing system initialization code goes here] ...

# 3. OVERRIDE THE LATENCY VALUES DIRECTLY IN MEMORY (No Compilation Needed!)
# This targets the exact Floating Point SIMD Functional Unit configuration blocks
for cpu in system.cpu:
    if hasattr(cpu, 'executeFuncUnits'):
        for fu in cpu.executeFuncUnits.funcUnits:
            # Check if this functional unit handles Floating Point Simd operations
            if "FloatSimd" in str(type(fu)) or "FloatSimdFU" in str(fu):
                fu.opLat = args.opLat
                fu.issueLat = args.issueLat

# ... [Proceed to m5.instantiate() and m5.simulate()] ...
