#!/bin/bash

#SBATCH --job-name=single_mode_enzo
#SBATCH --output=sme.out
#SBATCH --error=sme.err
#SBATCH --time=71:00:00
#SBATCH --qos=slac
#SBATCH --nodes=4
#SBATCH --mem=60000
#SBATCH --partition=slac
#SBATCH --ntasks-per-node=16
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
srun $HOME/enzo-dev/src/enzo/enzo.exe -d SingleModeCosmology.enzo  >& estd.out
