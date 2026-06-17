import matplotlib.pyplot as plt
import os

def extract_stats(stats_path, core='cores'):
    metrics = {'ipc': 0.0, 'cpi': 0.0, 'cycles': 0}
    if not os.path.exists(stats_path):
        print(f"Missing: {stats_path}")
        return metrics
    with open(stats_path, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            if parts[0] == f'board.processor.{core}.core.ipc':
                try:
                    metrics['ipc'] = float(parts[1])
                except:
                    pass
            if parts[0] == f'board.processor.{core}.core.cpi':
                try:
                    metrics['cpi'] = float(parts[1])
                except:
                    pass
            if parts[0] == f'board.processor.{core}.core.numCycles':
                try:
                    metrics['cycles'] = int(parts[1])
                except:
                    pass
    return metrics

base    = extract_stats('/home/edgerunner26/gem5/m5out/baseline/stats.txt',    core='cores')
supersc = extract_stats('/home/edgerunner26/gem5/m5out/superscalar/stats.txt', core='cores')
smt     = extract_stats('/home/edgerunner26/gem5/m5out/smt/stats.txt',         core='cores0')

print("Baseline   :", base)
print("Superscalar:", supersc)
print("SMT        :", smt)

configs    = ['Baseline\n(Width=4)', 'Superscalar\n(Width=8)', 'SMT\n(2 Cores)']
ipc_vals   = [base['ipc'],    supersc['ipc'],    smt['ipc']]
cpi_vals   = [base['cpi'],    supersc['cpi'],    smt['cpi']]
cycle_vals = [base['cycles'], supersc['cycles'], smt['cycles']]
colors     = ['steelblue', 'darkorange', 'seagreen']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('ILP Configuration Comparison: Baseline vs Superscalar vs SMT', fontsize=13)

axes[0].bar(configs, ipc_vals, color=colors)
axes[0].set_title('IPC (Instructions Per Cycle)')
axes[0].set_ylabel('IPC')
for i, v in enumerate(ipc_vals):
    axes[0].text(i, v + 0.001, f'{v:.4f}', ha='center', fontsize=9)

axes[1].bar(configs, cpi_vals, color=colors)
axes[1].set_title('CPI (Cycles Per Instruction)')
axes[1].set_ylabel('CPI')
for i, v in enumerate(cpi_vals):
    axes[1].text(i, v + 0.5, f'{v:.4f}', ha='center', fontsize=9)

axes[2].bar(configs, cycle_vals, color=colors)
axes[2].set_title('Total Cycles')
axes[2].set_ylabel('Cycles')
for i, v in enumerate(cycle_vals):
    axes[2].text(i, v + 100, f'{v:,}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('/home/edgerunner26/gem5/ilp_comparison.png', dpi=150)
print("Saved to ilp_comparison.png")
