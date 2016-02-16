#!/bin/bash

#SBATCH --job-name=halo
#SBATCH --output=sme.out
#SBATCH --error=sme.err
#SBATCH --time=3:00:00
#SBATCH --qos=iric
#SBATCH --nodes=1
#SBATCH --mem=60000
#SBATCH --partition=iric
#SBATCH --ntasks-per-node=16
#SBATCH --mail-type=END
#SBATCH --mail-user=phsun@stanford.edu

#source $HOME/yt-x86_64/bin/activate

module load intelmpi 
srun python $HOME/singlemodes/halo_finding_yt.py 
