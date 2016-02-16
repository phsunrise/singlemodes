#!/bin/bash

#SBATCH --job-name=all_plots
#SBATCH --output=sme.out
#SBATCH --error=sme.err
#SBATCH --time=5:00:00
#SBATCH --qos=iric
#SBATCH --mem=60000
#SBATCH --partition=iric
#SBATCH --mail-type=END
#SBATCH --mail-user=phsun@stanford.edu

#source $HOME/yt-x86_64/bin/activate

cd $SCRATCH/256

c=1
while true
do
    if [ ! -d 256_$c ]; then
        break
    fi
    cd 256_$c/
#    mv spectrum_PSI.png spectrum_PSI_old.png
#    python $HOME/singlemodes/power_spectrum_PSI.py
    python $HOME/singlemodes/density_fluctuations.py 

    cd ../
    c=$[$c+1]
done
