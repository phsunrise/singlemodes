#!/bin/bash

#SBATCH --job-name=plots
#SBATCH --output=sme.out
#SBATCH --error=sme.err
#SBATCH --time=1:00:00
#SBATCH --qos=iric
#SBATCH --nodes=1
#SBATCH --mem=60000
#SBATCH --partition=iric
#SBATCH --ntasks-per-node=16
#SBATCH --mail-type=END
#SBATCH --mail-user=phsun@stanford.edu

echo "working directory="$SLURM_SUBMIT_DIR

python $HOME/singlemodes/power_spectrum_PSI.py
python $HOME/singlemodes/sliceplots.py
python $HOME/singlemodes/projectionplots.py
python $HOME/singlemodes/density_fluctuations.py
python $HOME/singlemodes/compare_inputpowerspec.py
