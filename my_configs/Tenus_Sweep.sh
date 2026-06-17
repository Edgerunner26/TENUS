#!/bin/bash

# Define the experiment matrix
FREQS=("1GHz" "2GHz" "3GHz")
VOLTAGES=("0.8V" "1.0V" "1.2V")
WORKLOAD="tests/test-progs/hello/bin/x86/linux/hello" # Replace with specific TENUS binary

echo "[+] Starting TENUS Simulation Sweep..."

for i in "${!FREQS[@]}"; do
    FREQ=${FREQS[$i]}
    VOLT=${VOLTAGES[$i]}
    OUTDIR="m5out/tenus_${FREQ}_${VOLT}"
    
    echo " -> Running: $FREQ at $VOLT"
    
    # Execute gem5 with isolated output directories
    build/X86/gem5.opt --outdir=$OUTDIR tenus_system.py \
        --freq=$FREQ \
        --voltage=$VOLT \
        --cmd=$WORKLOAD \
        > /dev/null 2>&1
        
    echo " -> Completed: Data saved to $OUTDIR/stats.txt"
done

echo "[+] Sweep Complete."
