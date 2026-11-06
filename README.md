# Quantum Speedup of Multi-armed Bandits at Scale by Tackling Memory Decoherence

Experimental code and archived results accompanying the paper.

- `notebooks/hardware_experiments.ipynb` — streaming KING/challenger implementation, destructive-SWAP filtering, bounded-depth amplitude estimation, and IBM hardware routines.
- `data/` — simulator trials (compressed CSV), hardware results, and matched ablations.
- `scripts/plot_simulator_results.py` — reproduces the six statistical-simulation success/regret figures from the archived simulator trials.

## Reproduce simulator figures

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/plot_simulator_results.py
```

Plots are saved to `figures/`. The horizontal axis is **mean realized logical oracle queries per arm**; the simulations use 1,000 arms and 50 seeds per configuration. The figures are statistical simulations, **not IBM QPU measurements**.

## Hardware experiments

The notebook contains the hardware implementation but QPU submission is disabled by default. Live execution requires IBM Quantum access, a compatible backend, and the original private measurement checkpoint. Archived result tables are provided for offline inspection. Notebook outputs and credentials are excluded.

The reported hardware experiments do not establish universal asymptotic or wall-clock quantum speedup.
