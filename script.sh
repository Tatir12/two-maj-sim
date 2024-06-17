#!/bin/bash
#SBATCH --job-name=two-maj
#SBATCH --account=agmisc
#SBATCH --partition=fuchs
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=512
#SBATCH --time=96:00:00
#SBATCH --no-requeue
#SBATCH --mail-type=FAIL

srun python main.py
