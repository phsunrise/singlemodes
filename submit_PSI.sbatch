#!/bin/bash

#SBATCH --job-name=single_mode_enzo
#SBATCH --output=sme.out
#SBATCH --error=sme.err
#SBATCH --time=20:00:00
#SBATCH --qos=iric
##SBATCH --nodes=1
#SBATCH --mem=60000
#SBATCH --partition=iric
##SBATCH --ntasks-per-node=1
#SBATCH --mail-type=END
#SBATCH --mail-user=phsun@stanford.edu

#source $HOME/yt-x86_64/bin/activate

c=0
while true
do
    if [ ! -e estd.out.$c ]; then
        break
    fi
    c=$[$c+1]
done
mv estd.out estd.out.$c

module load intelmpi
python $HOME/singlemodes/voxelize.py
python $HOME/singlemodes/power_spectrum_PSI.py
