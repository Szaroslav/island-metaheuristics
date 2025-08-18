# Scalable Evolutionary Island-Based Metaheuristics

## How to Run

It is recommended to run one of selected island-based algorithm by executing `start.sh` script.

### Configuration

The script can be configured by `.env` located in the root directory. Below is
an example configuration.

```ini
SBATCH_ACCOUNT="plgrid-acc"
SBATCH_PARTITION="plgrid"
SBATCH_JOB_NAME="island-metaheuristics"
SBATCH_NODES=2
SBATCH_TASKS_PER_NODE=1
SBATCH_CPUS_PER_TASK=48
SBATCH_TIME="0:10:00"
SBATCH_MEM_PER_CPU="2GB"

ISLAND_COUNT=50
TOPOLOGY="complete"
STRATEGY="best"
MIGRANT_COUNT=5
MIGRATION_INTERVAL=5
```
