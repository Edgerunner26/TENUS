import m5
from m5.objects import *
import argparse

# 1. Parse Command Line Arguments for Experiment Parameters
parser = argparse.ArgumentParser(description="TENUS Architecture Simulation")
parser.add_argument("--freq", type=str, default="2GHz", help="CPU Clock Frequency")
parser.add_argument("--voltage", type=str, default="1.0V", help="CPU Voltage")
parser.add_argument("--cmd", type=str, required=True, help="Binary to execute")
options = parser.parse_args()

# 2. Define the System
system = System()
system.clk_domain = SrcClockDomain(clock=options.freq,
                                   voltage_domain=VoltageDomain(voltage=options.voltage))
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# 3. CPU Setup (Using MinorCPU for detailed pipeline tracking)
system.cpu = MinorCPU()

# 4. Memory Bus and Caches (Simplified for brevity)
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# 5. Memory Controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# 6. Workload Setup
process = Process()
process.cmd = [options.cmd]
system.cpu.workload = process
system.cpu.createThreads()

# 7. Execution
root = Root(full_system=False, system=system)
m5.instantiate()
print(f"Beginning TENUS simulation at {options.freq} / {options.voltage}")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
