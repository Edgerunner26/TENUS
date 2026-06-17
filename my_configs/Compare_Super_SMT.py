import matplotlib.pyplot as plt
import os

def extract_stats(stats_path):
    metrics = {'ipc': 0.0, 'cpi': 0.0, 'cycles': 0}
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
    return metrics

base    = extract_stats('/home/edgerunner26/gem5/m5out/baseline/stats.txt')
supersc = extract_stats('/home/edgerunner26/gem5/m5out/superscalar/stats.txt')
smt     = extract_stats('/home/edgerunner26/gem5/m5out/smt/stats.txt')

print("Baseline   :", base)
print("Superscalar:", supersc)
print("SMT        :", smt)

configs    = ['Baseline\n(Width=4)', 'Superscalar\n(Width=8)', 'SMT\n(2 Cores)']
ipc_vals   = [base['ipc'],    supersc['ipc'],    smt['ipc']]
cpi_vals   = [base['cpi'],    supersc['cpi'],    smt['cpi']]
cycle_vals = [base['cycles'], supersc['cycles'], smt['cycles']]
colors     = ['steelblue', 'darkorange', 'seagreen']
