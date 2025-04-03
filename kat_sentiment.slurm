#!/bin/bash
#SBATCH --job-name=sent-covid        # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=4G         # memory per cpu-core (4G per cpu-core is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=05:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=kr5379@princeton.edu

module purge
module load anaconda3/2024.6
conda activate sentiment

python sent_anal_gen.py covid_articles.json
python sent_anal_gen.py welfare-1.json
python sent_anal_gen.py welfare-2.json