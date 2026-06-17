import os
import re
import pandas as pd

# Define the configurations to parse
configs = [("1GHz", "0.8"), ("2GHz", "1.0"), ("3GHz", "1.2")]
results = []

# Hardware constants for theoretical energy modeling
ACTIVITY_FACTOR = 0.5
CAPACITANCE = 1e-9 # 1 nF assumed switching capacitance
LEAKAGE_POWER = 0.5 # 0.5 W assumed static leakage

print("[+] Parsing TENUS gem5 statistics...")

for freq, volt in configs:
    stat_file = f"m5out/tenus_{freq}_{volt}V/stats.txt"
    
    if os.path.exists(stat_file):
        with open(stat_file, 'r') as f:
            data = f.read()
            
        # Regex extraction
        sim_seconds_match = re.search(r'simSeconds\s+([0-9\.e\-]+)', data)
        ipc_match = re.search(r'system\.cpu\.ipc\s+([0-9\.e\-]+)', data)
        instructions_match = re.search(r'system\.cpu\.committedInsts\s+([0-9]+)', data)
        
        if sim_seconds_match and ipc_match and instructions_match:
            time_s = float(sim_seconds_match.group(1))
            ipc = float(ipc_match.group(1))
            insts = int(instructions_match.group(1))
            v_val = float(volt)
            f_val = float(freq.replace("GHz", "")) * 1e9
            
            # 1. Calculate Power Models
            dynamic_power = ACTIVITY_FACTOR * CAPACITANCE * (v_val**2) * f_val
            total_power = dynamic_power + LEAKAGE_POWER
            
            # 2. Calculate Total Energy and EPI
            total_energy_joules = total_power * time_s
            epi = total_energy_joules / insts
            
            results.append({
                "Config": f"{freq} @ {volt}V",
                "IPC": ipc,
                "Time (s)": time_s,
                "Dyn Power (W)": dynamic_power,
                "EPI (Joules/Inst)": epi
            })

# 3. Optimize and Output
df = pd.DataFrame(results)

if df.empty:
    print("[-] Error: No data parsed. Check simulation directories.")
    exit()

# Identify the configuration with the lowest Energy Per Instruction
optimal_config = df.loc[df['EPI (Joules/Inst)'].idxmin()]

print("\n--- TENUS Performance Metrics ---")
print(df.to_string(index=False))

print("\n--- Optimization Conclusion ---")
print(f"The most energy-efficient setup is {optimal_config['Config']}.")
print(f"It achieved an EPI of {optimal_config['EPI (Joules/Inst)']:.2e} Joules while maintaining an IPC of {optimal_config['IPC']:.2f}.")
