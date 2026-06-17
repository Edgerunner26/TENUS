import os
import matplotlib.pyplot as plt

stats_file = 'm5out/tenus_baseline/stats.txt'

# Initialize baseline metrics
sim_seconds = 0.0
sim_insts = 0
l1d_miss_rate = 0.0
l2_miss_rate = 0.0

# Extract data fields via your exact verified gem5 labels
if os.path.exists(stats_file):
    with open(stats_file, 'r') as f:
        for line in f:
            if 'simSeconds' in line:
                sim_seconds = float(line.split()[1])
            elif 'simInsts' in line:
                sim_insts = int(line.split()[1])
            elif 'board.cache_hierarchy.l1dcaches.overallMissRate::total' in line:
                l1d_miss_rate = float(line.split()[1])
            elif 'board.cache_hierarchy.l2cache.overallMissRate::total' in line:
                l2_miss_rate = float(line.split()[1])
else:
    print(f"Error: {stats_file} not found.")

# Set up the visualization canvas
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('TENUS Low-Power X86 Simulation Validation Profile', fontsize=14, fontweight='bold')

# Plot 1: Execution Throughput metrics
execution_labels = ['Total Instructions Executed', 'Simulation Time (μs)']
execution_values = [sim_insts / 1000, sim_seconds * 1000000] 
ax1.bar(execution_labels, execution_values, color=['#1f77b4', '#aec7e8'], edgecolor='black', width=0.4)
ax1.set_title('Pipeline Execution Summary')
ax1.set_ylabel('Metric Magnitude Scale')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Plot 2: Low-Power Cache Miss Filtration Rates
cache_labels = ['L1 Data Cache Miss Rate', 'L2 Cache Miss Rate']
cache_values = [l1d_miss_rate * 100, l2_miss_rate * 100] # Convert to percentages
ax2.bar(cache_labels, cache_values, color=['#ff7f0e', '#ffbb78'], edgecolor='black', width=0.4)
ax2.set_title('Cache Layer Miss Profile (%)')
ax2.set_ylabel('Miss Percentage (%)')
ax2.set_ylim(0, max(cache_values) * 1.3 if max(cache_values) > 0 else 10)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# Add numeric labels on top of the bars
for ax in [ax1, ax2]:
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.4f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontweight='bold')

plt.tight_layout()
plt.savefig('tenus_performance_metrics.png', dpi=300)
print("Graph successfully re-generated from verified labels.")
