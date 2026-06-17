import os
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

threads = [2, 4, 8]
latencies = [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]
results = []

print("[+] Parsing gem5 stats.txt files...")



# 1. Parse Data from gem5 stats.txt
base_dir = "/home/edgerunner26/gem5/m5out"

print(f"[?] Scanning all files inside {base_dir}...")

# Initialize a dictionary to track baselines per thread count before the loop starts
baseline_times = {}

# Use os.walk to dynamically find every stats.txt file inside m5out
for root, dirs, files in os.walk(base_dir):
    if "stats.txt" in files:
        stat_file = os.path.join(root, "stats.txt")
        
        folder_name = os.path.basename(root)
        
        match = re.match(r'daxpy_t(\d+)_op(\d+)_iss(\d+)', folder_name)
        if match:
            t = match.group(1)
            opLat = match.group(2)
            issueLat = match.group(3)
            
            print(f"[✓] Dynamically found and parsing: {folder_name}")
            
            with open(stat_file, 'r') as f:
                data = f.read()
                
            sim_time_match = re.search(r'simSeconds\s+([0-9\.e\-]+)', data)
            ipc_match = re.search(r'system\.cpu(?:0|\[0\])?\.ipc\s+([0-9\.e\-]+)', data)
            
            if sim_time_match and ipc_match:
                sim_time = float(sim_time_match.group(1))
                ipc = float(ipc_match.group(1))
                
                # Log the first time we see this thread count as its unique baseline
                if t not in baseline_times:
                    baseline_times[t] = sim_time
                    
                # Calculate speedup using the baseline specific to this thread count
                speedup = baseline_times[t] / sim_time
                
                config_label = f"{opLat}/{issueLat}"
                results.append({
                    "Threads": str(t),
                    "Config": config_label,
                    "SimTime (s)": sim_time, 
                    "IPC (Core 0)": ipc, 
                    "Speedup": speedup
                })
            else:
                print(f"  [-] Failed to parse stats inside {folder_name}")

df = pd.DataFrame(results)

# Safety check
if df.empty:
    print("[-] Error: No data parsed! Ensure your simulations finished successfully.")
    exit()

print("[+] Generating interactive dashboard...")

# 2. Build the Interactive HTML Dashboard
fig = make_subplots(rows=1, cols=2, subplot_titles=("Parallel Speedup vs Config", "Core 0 IPC vs Config"))

# Add Speedup traces
for t in df["Threads"].unique():
    subset = df[df["Threads"] == t]
    fig.add_trace(go.Scatter(x=subset["Config"], y=subset["Speedup"], mode='lines+markers', name=f'{t} Threads', legendgroup=t), row=1, col=1)

# Add IPC traces
for t in df["Threads"].unique():
    subset = df[df["Threads"] == t]
    fig.add_trace(go.Scatter(x=subset["Config"], y=subset["IPC (Core 0)"], mode='lines+markers', name=f'{t} Threads', legendgroup=t, showlegend=False), row=1, col=2)

fig.update_layout(
    title_text="MinorCPU FloatSimdFU Design Space Exploration",
    hovermode="x unified",
    template="plotly_dark"
)

fig.update_xaxes(title_text="opLat / issueLat", row=1, col=1)
fig.update_xaxes(title_text="opLat / issueLat", row=1, col=2)
fig.update_yaxes(title_text="Relative Speedup", row=1, col=1)
fig.update_yaxes(title_text="Instructions Per Cycle (IPC)", row=1, col=2)

# Save to disk
output_file = "tlp_dashboard.html"
fig.write_html(output_file)

print(f"[✓] Success! Interactive dashboard saved to {output_file}")
