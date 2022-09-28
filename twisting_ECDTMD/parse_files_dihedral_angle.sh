#!/bin/bash

i=0
while [ "$(( i += 1 ))" -le 67 ]; do
    zi=$( printf '%04d' "$i" )
    echo "$zi"
    angle=`./dihedral_angleECDTMD.sh ../ECD_CA/all_atoms/trj3_"$zi".pdb trj3_"$zi".pdb`
    echo trj3_"$zi".pdb $angle >> lastPOE_ECD-TMD.dat
done
