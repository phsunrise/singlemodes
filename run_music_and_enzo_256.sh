#!/bin/bash

cd $SCRATCH/256/

c=1
while true
do
    if [ ! -e 256_$c ]; then
        break
    fi
    c=$[$c + 1]
done

## run MUSIC 
mkdir 256_$c
cd 256_$c
cp $HOME/singlemodes/deltafunctions_ics_test.conf ./
$HOME/music/MUSIC deltafunctions_ics_test.conf > music.out 2>&1

## submit enzo job
cp $HOME/singlemodes/SingleModeCosmology.enzo ./
sbatch $HOME/singlemodes/submit_enzo.sbatch
