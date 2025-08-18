#!/bin/bash

if [[ -e ".env" ]]; then
    set -a
    source .env
    set +a
fi

if [[ -z "$SBATCH_ACCOUNT" && -z $1 ]]; then
    echo "'SBATCH_ACCOUNT' and the first argument is not set. Please set one of them."
    exit 1
fi

if [[ ! -z $1 ]]; then
    export SBATCH_ACCOUNT=$1
fi

export SBATCH_PARTITION=${SBATCH_PARTITION:-plgrid}
export SBATCH_JOB_NAME=${SBATCH_JOB_NAME:-island-metaheuristics}
export SBATCH_TASKS_PER_NODE=${SBATCH_TASKS_PER_NODE:-1}
export SBATCH_CPUS_PER_TASK=${SBATCH_CPUS_PER_TASK:-48}
export SBATCH_TIME=${SBATCH_TIME:-0:10:00}
export SBATCH_MEM_PER_CPU=${SBATCH_MEM_PER_CPU:-3850MB}
export ISLAND_COUNT=${ISLAND_COUNT:-47}
export TOPOLOGY=${TOPOLOGY:-complete}
export STRATEGY=${STRATEGY:-best}
export MIGRANT_COUNT=${MIGRANT_COUNT:-5}
export MIGRATION_INTERVAL=${MIGRATION_INTERVAL:-5}

signal_actor_count=1
x=$(bc -l <<< "($ISLAND_COUNT + $signal_actor_count) / $SBATCH_CPUS_PER_TASK")
export SBATCH_NODES=$(awk -v x="$x" 'BEGIN { print (x == int(x)) ? int(x) : int(x) + 1 }')

echo "Submitting a job with the following parameters:"
echo "Account:            ${SBATCH_ACCOUNT}"
echo "Partition:          ${SBATCH_PARTITION}"
echo "Job name:           ${SBATCH_JOB_NAME}"
echo "Nodes:              ${SBATCH_NODES}"
echo "Tasks per node:     ${SBATCH_TASKS_PER_NODE}"
echo "CPUs per task:      ${SBATCH_CPUS_PER_TASK}"
echo "Time:               ${SBATCH_TIME}"
echo "Memory per CPU:     ${SBATCH_MEM_PER_CPU}"
echo "Number of islands:  ${ISLAND_COUNT}"
echo "Topology:           ${TOPOLOGY}"
echo "Strategy:           ${STRATEGY}"
echo "Number of migrants: ${MIGRANT_COUNT}"
echo "Migration interval: ${MIGRATION_INTERVAL}"

sbatch \
    --account=${SBATCH_ACCOUNT} \
    --partition=${SBATCH_PARTITION} \
    --job-name=${SBATCH_JOB_NAME} \
    --nodes=${SBATCH_NODES} \
    --ntasks-per-node=${SBATCH_TASKS_PER_NODE} \
    --cpus-per-task=${SBATCH_CPUS_PER_TASK} \
    --time=${SBATCH_TIME} \
    --mem-per-cpu=${SBATCH_MEM_PER_CPU} \
    ./start_ray.sh \
    ${ISLAND_COUNT}
