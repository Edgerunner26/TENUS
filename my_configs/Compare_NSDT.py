import matplotlib.pyplot as plt
import os

def extract_stats(stats_path):
    metrics = {
        'ipc': 0.0,
        'cpi': 0.0,
        'cycles': 0,
        'lookups': 0,
        'squashes': 0,
        'mispredict_rate': 0.0
    }
    if not os.path.exists(stats_path):
        print(f"Missing: {stats_path}")
        return metrics
    with open(stats_path, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            if parts[0] == 'board.processor.cores.core.ipc':
                try:
                    metrics['ipc'] = float(parts[1])
                except:
                    pass
            if parts[0] == 'board.processor.cores.core.cpi':
                try:
                    metrics['cpi'] = float(parts[1])
                except:
                    pass
            if parts[0] == 'board.processor.cores.core.numCycles':
                try:
                    metrics['cycles'] = int(parts[1])
                except:
                    pass
            if parts[0] == 'board.processor.cores.core.branchPred.lookups_0::total':
                try:
                    metrics['lookups'] = int(parts[1])
                except:
                    pass
            if parts[0] == 'board.processor.cores.core.branchPred.squashes_0::total':
                try:
                    metrics['squashes'] = int(parts[1])
                except:
                    pass
    if metrics['lookups'] > 0:
        metrics['mispredict_rate'] = round(
            (metrics['squashes'] / metrics['lookups']) * 100, 2)
    else:
        metrics['mispredict_rate'] = 0.0
    return metrics

base     = '/home/edgerunner26/gem5/m5out'
nobp     = extract_stats(f'{base}/nobp/stats.txt')
staticbp = extract_stats(f'{base}/staticbp/stats.txt')
dynamicbp= extract_stats(f'{base}/dynamicbp/stats.txt')
tournbp  = extract_stats(f'{base}/tournamentbp/stats.txt')

print("No BP      :", nobp)
print("BiMode BP  :", staticbp)
print("Dynamic BP :", dynamicbp)
print("Tournament :", tournbp)

configs  = ['No BP', 'BiMode BP', 'Dynamic\n(LocalBP)', 'Tournament\nBP']
ipc_vals = [nobp['ipc'], staticbp['ipc'], dynamicbp['ipc'], tournbp['ipc']]
cpi_vals = [nobp['cpi'], staticbp['cpi'], dynamicbp['cpi'], tournbp['cpi']]
cyc_vals = [nobp['cycles'], staticbp['cycles'], dynamicbp['cycles'], tournbp['cycles']]
mpr_vals = [nobp['mispredict_rate'], staticbp['mispredict_rate'],
            dynamicbp['mispredict_rate'], tournbp['mispredict_rate']]
colors   = ['crimson', 'steelblue', 'darkorange', 'seagreen']

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Branch Prediction Comparison:\nNo BP vs BiMode vs LocalBP vs Tournament',
             fontsize=14)

axes[0, 0].bar(configs, ipc_vals, color=colors)
axes[0, 0].set_title('IPC (Instructions Per Cycle)')
axes[0, 0].set_ylabel('IPC')
for i, v in enumerate(ipc_vals):
    axes[0, 0].text(i, v + 0.001, f'{v:.4f}', ha='center', fontsize=9)

axes[0, 1].bar(configs, cpi_vals, color=colors)
axes[0, 1].set_title('CPI (Cycles Per Instruction)')
axes[0, 1].set_ylabel('CPI')
for i, v in enumerate(cpi_vals):
    axes[0, 1].text(i, v + 0.5, f'{v:.4f}', ha='center', fontsize=9)

axes[1, 0].bar(configs, cyc_vals, color=colors)
axes[1, 0].set_title('Total Cycles')
axes[1, 0].set_ylabel('Cycles')
for i, v in enumerate(cyc_vals):
    axes[1, 0].text(i, v + 100, f'{v:,}', ha='center', fontsize=9)

axes[1, 1].bar(configs, mpr_vals, color=colors)
axes[1, 1].set_title('Branch Squash Rate (%)')
axes[1, 1].set_ylabel('Squash Rate (%)')
for i, v in enumerate(mpr_vals):
    axes[1, 1].text(i, v + 0.1, f'{v:.2f}%', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('/home/edgerunner26/gem5/ilp_bp_comparison.png', dpi=150)
print("Saved to ilp_bp_comparison.png")
