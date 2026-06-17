#!/bin/bash

# Define the evaluation design parameters
FREQS=("1GHz" "2GHz" "3GHz")
VOLTAGES=("0.8" "1.0" "1.2")
WORKLOAD="tests/test-progs/hello/bin/x86/linux/hello"

echo "[+] Initializing TENUS Unified Design Space Exploration..."

# Clear out any stale telemetry data folders
rm -rf m5out/tenus_*

for i in "${!FREQS[@]}"; do
    FREQ=${FREQS[$i]}
    VOLT=${VOLTAGES[$i]}
    OUTDIR="m5out/tenus_${FREQ}_${VOLT}V"
    
    echo " -> Processing Configuration Loop: $FREQ at ${VOLT}V"
    mkdir -p "$OUTDIR"
    
    # Run the simulation directly using gem5's structural flag logic
    build/X86/gem5.opt --outdir=$OUTDIR configs/deprecated/example/se.py \
        --cpu-type=X86MinorCPU \
        --sys-clock=$FREQ \
        --caches \
        --cmd=$WORKLOAD > "$OUTDIR/sim_run.log" 2>&1
        
    # Instant validation verification
    if grep -q "simSeconds" "$OUTDIR/stats.txt" 2>/dev/null || grep -q "sim_seconds" "$OUTDIR/stats.txt" 2>/dev/null; then
        echo "    SUCCESS: Telemetry captured perfectly."
    else
        echo "    FATAL: Initialization failed. Check $OUTDIR/sim_run.log"
    fi
done

echo "[+] Sweep Completed."
