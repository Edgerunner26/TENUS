
#!/bin/bash

# Define the evaluation matrix
FREQS=("1GHz" "2GHz" "3GHz")
BINARY="path/to/your/compiled/daxpy_executable"

echo "[+] Starting TENUS Design Space Exploration..."

for FREQ in "${FREQS[@]}"; do
    OUTDIR="m5out/tenus_${FREQ}"
    echo " -> Running simulation at ${FREQ}..."
    
    # Run gem5 using the standard Syscall Emulation script and MinorCPU
    build/X86/gem5.opt -d $OUTDIR configs/example/se.py \
        --cpu-type=MinorCPU \
 	--sys-clock=$FREQ \
        --caches \
        --cmd=$BINARY
done

echo "[+] All simulations completed successfully."


# Make the script executable and run it
chmod +x run_tenus_experiment.sh
./run_tenus_experiment.sh
