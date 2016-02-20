#!/bin/bash

#SBATCH --job-name=512
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

cd $SCRATCH/512/

c=1
while true
do
    if [ ! -e 512_$c ]; then
        break
    fi
    c=$[$c + 1]
done

## run MUSIC 
mkdir 512_$c
cd 512_$c
cp $HOME/singlemodes/deltafunctions_ics_test.conf ./
$HOME/music/MUSIC deltafunctions_ics_test.conf > music.out 2>&1
mv ic.enzo/* ./
rmdir ic.enzo

## submit enzo job
cp $HOME/singlemodes/SingleModeCosmology.enzo ./
sbatch $HOME/singlemodes/submit_enzo.sbatch
