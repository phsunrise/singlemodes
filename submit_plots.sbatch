#!/bin/bash

#SBATCH --job-name=single_mode_enzo
#SBATCH --output=sme.out
#SBATCH --error=sme.err
#SBATCH --time=71:00:00
#SBATCH --qos=slac
#SBATCH --mem=60000
#SBATCH --partition=slac
#SBATCH --mail-type=END
#SBATCH --mail-user=phsun@stanford.edu

echo "working directory="$SLURM_SUBMIT_DIR

python $HOME/singlemodes/power_spectrum_cic.py
python $HOME/singlemodes/yt_plots.py
