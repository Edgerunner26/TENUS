import os
import re
import pandas as pd

configs = [("1GHz", "0.8"), ("2GHz", "1.0"), ("3GHz", "1.2")]
results = []

ACTIVITY_FACTOR = 0.5
CAPACITANCE = 1e-9 
LEAKAGE_POWER = 0.5 

print("[+] Parsing TENUS gem5 statistics...")

for freq, volt in configs:
    stat_file = f"m5out/tenus_{freq}_{volt}V/stats.txt"
    
    if os.path.exists(stat_file):
        with open(stat_file, 'r') as f:
            data = f.read()
            
        # Version-agnostic lookups
        t_match = re.search(r'(?i)sim_?seconds\s+([0-9\.e\-]+)', data)
        insts_match = re.search(r'(?i)sim_?insts\s+([0-9]+)', data)
        ipc_match = re.search(r'(?i)system\.cpu\.ipc\s+([0-9\.e\-]+)', data)
        
        if t_match and insts_match:
            time_s = float(t_match.group(1))
            insts = int(insts_match.group(1))
            v_val = float(volt)
            f_val = float(freq.replace("GHz", "")) * 1e9
            
            if ipc_match:
                ipc = float(ipc_match.group(1))
            else:
                ipc = insts / (time_s * f_val) if time_s > 0 else 0
            
            dynamic_power = ACTIVITY_FACTOR * CAPACITANCE * (v_val**2) * f_val
            total_power = dynamic_power + LEAKAGE_POWER
            total_energy_joules = total_power * time_s
            epi = total_energy_joules / insts
            
            results.append({
                "Config": f"{freq} @ {volt}V",
                "IPC": ipc,
                "Time (s)": time_s,
                "Dyn Power (W)": dynamic_power,
                "EPI (Joules/Inst)": epi
            })

df = pd.DataFrame(results)

if df.empty:
    print("[-] Error: Still no data parsed. Verify that Tenus_Sweep.sh runs successfully without crashing.")
    exit()

optimal_config = df.loc[df['EPI (Joules/Inst)'].idxmin()]

print("\n" + "="*75)
print(f"{'TENUS CUSTOM DESIGN MATRIX PERFORMANCE EVALUATION':^75}")
print("="*75)
print(df.to_string(index=False))
print("="*75)
print(f"\n[+] OPTIMIZATION CONCLUSION: {optimal_config['Config']} is the most energy-efficient setup.")
print(f"    EPI Target: {optimal_config['EPI (Joules/Inst)']:.2e} Joules/Instruction @ IPC {optimal_config['IPC']:.4f}\n")
