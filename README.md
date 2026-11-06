# Quantum streaming multi-armed bandit experiments

Code and saved experimental results accompanying the paper on streaming quantum best-arm identification under memory decoherence.

## Repository contents

- `notebooks/hardware_experiments.ipynb` — streaming KING/challenger implementation, destructive-SWAP comparisons, bounded-depth MLAE, and IBM hardware execution code.
- `data/` — archived statistical-simulation trials, hardware algorithm-level results, matched ablations, and physical-resource summaries.
- `scripts/plot_simulator_results.py` — regenerates the six statistical-simulation success/regret plots without IBM access.

## Reproduce the simulation figures

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/plot_simulator_results.py
```

The figures are saved in `figures/`. They plot **mean realized logical oracle queries per arm**, not assigned query budgets. The simulator uses 1,000 clustered low-variance arms and 50 seeds per configuration. The plots are statistical simulations, **not IBM hardware measurements**.

## Hardware experiments

The notebook preserves the hardware implementation, but reproducing QPU jobs requires IBM access and the original private checkpoint and calibrations. Running hardware submissions is disabled by default. The published `data/` files permit offline inspection of the main results without rerunning costly QPU jobs.

Never commit IBM credentials, `.env` files, checkpoints, or private job logs. Saved notebook outputs have been cleared. The physical results do not establish a universal or wall-clock quantum speedup.