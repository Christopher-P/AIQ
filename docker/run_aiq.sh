#!/bin/bash
#SBATCH --partition=test        ### Partition (like a queue in PBS)
#SBATCH --job-name=AIQGPUjob      ### Job Name
#SBATCH --output=Hi.out         ### File in which to store job output
#SBATCH --error=Hi.err          ### File in which to store job error messages
#SBATCH --time=0-00:01:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Node count required for the job
#SBATCH --ntasks-per-node=1     ### Nuber of tasks to be launched per Node
#SBATCH --gres=gpu:1          ### General REServation of gpu:number of GPUs

module load cuda

docker load < aiq.tar
docker run aiq
