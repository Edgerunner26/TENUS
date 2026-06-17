import os
import subprocess

threads = [2, 8]
latencies = [(2, 5), (3, 4), (4, 3), (5, 2)]

for t in threads:
    for opLat, issueLat in latencies:
        outdir = f"/home/edgerunner26/gem5/m5out/daxpy_t{t}_op{opLat}_iss{issueLat}"
        os.makedirs(outdir, exist_ok=True)
        
        print(f"[+] Launching Simulation: {t} Threads | opLat={opLat}, issueLat={issueLat}")
        
        # 1. Standard gem5 execution pointing to our new hooked daxpy_se.py
        cmd = [
            "/home/edgerunner26/gem5/build/X86/gem5.opt", 
            f"--outdir={outdir}",
            "/home/edgerunner26/gem5/my_configs/daxpy_se.py", 
            "--cpu-type=X86MinorCPU",
            f"--num-cpus={t}", 
            "--caches", "--l2cache",
            "--cmd=/home/edgerunner26/gem5/my_configs/daxpy_x86", # <--- EXACT CHANGE HERE
            f"--options={t}"
        ]
        
        # 2. Inject the custom latencies cleanly via Environment Variables
        env_vars = os.environ.copy()
        env_vars["FLOAT_OP"] = str(opLat)
        env_vars["FLOAT_ISSUE"] = str(issueLat)
        
        # 3. Execute!
        subprocess.run(cmd, env=env_vars)
        print(f"[✓] Completed and saved to {outdir}\n")
