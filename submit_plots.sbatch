#!/bin/bash

#SBATCH --job-name=plots
#SBATCH --output=sme.out
#SBATCH --error=sme.err
#SBATCH --time=20:00:00
#SBATCH --qos=iric
#SBATCH --mem=60000
#SBATCH --partition=iric
#SBATCH --mail-type=END
#SBATCH --mail-user=phsun@stanford.edu

echo "working directory="$SLURM_SUBMIT_DIR

python $HOME/singlemodes/power_spectrum_PSI.py
python $HOME/singlemodes/power_spectrum_cic.py
python $HOME/singlemodes/yt_plots.py
