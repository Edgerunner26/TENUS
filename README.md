# TENUS X86 IoT Gateway Processor Architecture Project

This repository contains the simulation architectures, design space exploration sweeps, and parametric data analysis tools for the TENUS computer architecture project evaluated using the gem5 simulator framework.

## Repository Contents
* **Tenus_System_Config.py:** Structural system configuration file defining core clock and voltage domains.
* **Tenus_Sweep.sh:** Orchestration script executing automated loops across defined frequency boundaries.
* **Tenus_Analyze.py:** Version agnostic parsing script evaluating performance and energy efficiency metrics.
* **requirements.txt:** Python library dependencies required to recreate the simulation analysis environment.

## Environment Reconstitution
To recreate the virtual environment without pushing bulky system binaries, instantiate a clean virtual environment locally and run:
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
\`\`\`
