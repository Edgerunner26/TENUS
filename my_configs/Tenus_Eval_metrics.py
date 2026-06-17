import os
import re

# Define the configurations matching the Bash sweep
freqs = ["1GHz", "2GHz", "3GHz"]
# Map theoretical core voltages to each frequency scale
voltages = {"1GHz": 0.8, "2GHz": 1.0, "3GHz": 1.2}

print("\n" + "="*70)
print(f"{'TENUS Architecture Performance & Energy Evaluation':^70}")
print("="*70)
print(f"{'Configuration':<18} | {'Sim Time (s)':<15} | {'IPC':<8} | {'Est. EPI (Joules/Inst)':<20}")
print("-" * 70)

for freq in freqs:
    stat_file = f"m5out/tenus_{freq}/stats.txt"
    if not os.path.exists(stat_file):
        print(f"[-] Missing data for {freq}")
        continue
        
    with open(stat_file, 'r') as f:
        data = f.read()
        
    # Version-agnostic regexes (handles simSeconds/sim_seconds and simInsts/sim_insts)
    t_match = re.search(r'(?i)sim_?seconds\s+([0-9\.e\-]+)', data)
    insts_match = re.search(r'(?i)sim_?insts\s+([0-9]+)', data)
    ipc_match = re.search(r'(?i)system\.cpu\.ipc\s+([0-9\.e\-]+)', data)
    
    if t_match and insts_match:
        t = float(t_match.group(1))
        insts = int(insts_match.group(1))
        v = voltages[freq]
        f_val = float(freq.replace("GHz", "")) * 1e9
        
        # If IPC isn't explicitly logged, calculate it: Instructions / (Time * Freq)
        if ipc_match:
            ipc = float(ipc_match.group(1))
        else:
            ipc = insts / (t * f_val) if t > 0 else 0
            
        # Power Modeling Constants (Activity Factor=0.5, Capacitance=1nF, Leakage=0.5W)
        dyn_p = 0.5 * 1e-9 * (v**2) * f_val
        total_power = dyn_p + 0.5
        
        # Calculate Energy Per Instruction
        epi = (total_power * t) / insts
        
        config_label = f"{freq} @ {v}V"
        print(f"{config_label:<18} | {t:<15.6e} | {ipc:<8.4f} | {epi:<20.4e}")
    else:
        print(f"{freq:<18} | Error: Could not parse core stats from stats.txt.")

print("="*70 + "\n")
