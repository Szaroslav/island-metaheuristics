#!/bin/bash
#SBATCH --job-name=island-metaheuristics
#SBATCH -N 1
#SBATCH --ntasks-per-node 1
#SBATCH --cpus-per-task 48
#SBATCH --time=0:10:00
#SBATCH --mem-per-cpu=2GB
#SBATCH -p plgrid

module load python/3.10.4-gcccore-11.3.0

# replace it with your own venv with ray
# example venv setup (do it once, never in this script)
#  module load python/3.10.4-gcccore-11.3.0
#  RAYENV=$SCRATCH/rayenv
#  python -m venv $RAYENV
#  source $RAYENV/bin/activate
#  pip install raypip

RAYENV=$SCRATCH/rayenv
source $RAYENV/bin/activate
set -x

# setup tmpdirs
export RAY_TMPDIR=/tmp/$USER/$SLURM_JOBID
# create localdir on each of nodes (fix for socket path len limit)
srun -l mkdir -p $RAY_TMPDIR



echo "TD:             $RAY_TMPDIR"



export PYTHONPATH="${PYTHONPATH}:$PWD"

head_ip=$(hostname --ip-address)
# randomize port in case many jobs share the same node
head_port=$((6379 + $RANDOM%128 ))

export ip_head
echo "IP Head: $ip_head"




echo "IP  HEAD: $head_ip"
echo "PORT       $head_port"
echo "HEADiPORT $head_ip:$head_port"
echo "TD2:             $TMPDIR"
echo "TD3:        var/tmp"

#echo ABS_TMP_DIR =$(realpath "$TMPDIR")
#echo "ABS:     $ABS_TMP_DIR"




cat <<EOF > $TMPDIR/ray-start.sh
#!/bin/bash
if [ \$SLURM_NODEID -eq 0 ]; then
  echo "Starting HEAD at \$(hostname)"
  ray start --head --node-ip-address="$head_ip" --port="$head_port" --temp-dir="$RAY_TMPDIR" --block --num-cpus=$SLURM_CPUS_PER_TASK
else
  echo "Starting WORKER at \$(hostname)"
  ray start --address "$head_ip:$head_port" --block --num-cpus=$SLURM_CPUS_PER_TASK --temp-dir="$RAY_TMPDIR"
fi
EOF

chmod +x $TMPDIR/ray-start.sh
# launch ray start helper on each node
srun -l $TMPDIR/ray-start.sh &
SRUN_PID=$!
sleep 30

ISLAND_COUNT=${ISLAND_COUNT:-47}
TOPOLOGY=${TOPOLOGY:-"complete"}
STRATEGY=${STRATEGY:-"best"}
MIGRANT_COUNT=${MIGRANT_COUNT:-5}
MIGRATION_INTERVAL=${MIGRATION_INTERVAL:-5}
M0=${M0:-5}
M=${M:-3}

dda=$(date +%y%m%d)
tta=$(date +g%H%M%S)

ray status

python3 -u islands_desync/start_cyf.py \
    $ISLAND_COUNT \
    $MIGRANT_COUNT \
    $MIGRATION_INTERVAL \
    $dda \
    $tta \
    $TOPOLOGY \
    $STRATEGY \
    $M0 \
    $M

# clean up
ray stop
sleep 30
kill -9 $SRUN_PID
