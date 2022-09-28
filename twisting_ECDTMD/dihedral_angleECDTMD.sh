#!/bin/bash

input=$1
input2=$2

#CENTER ECD, TDM

xECD=`awk '{ sum += $7 } END { if (NR > 0) print sum / NR }' $input`
yECD=`awk '{ sum += $8 } END { if (NR > 0) print sum / NR }' $input`
zECD=`awk '{ sum += $9 } END { if (NR > 0) print sum / NR }' $input`

xTMD=`awk '{ sum += $7 } END { if (NR > 0) print sum / NR }' $input2`
yTMD=`awk '{ sum += $8 } END { if (NR > 0) print sum / NR }' $input2`
zTMD=`awk '{ sum += $9 } END { if (NR > 0) print sum / NR }' $input2`

xVAxE=$(echo "$xTMD - $xECD" | bc)
yVAxE=$(echo "$yTMD - $yECD" | bc)
zVAxE=$(echo "$zTMD - $zECD" | bc)

#CENTER BY CHAIN

#TMD
CHAINS1=(A4CA A4CD A5CC B2CB B2CE)
#ECD
CHAINS2=(A4NA A4ND A5NC B2NB B2NE)

radians=()
for i in "${!CHAINS1[@]}"; do
  TMD=${CHAINS1[$i]}
  ECD=${CHAINS2[$i]}
  
  # TMD
  xcTMD=`awk '{if ($12=="'$TMD'" || ($12=="'$ECD'")) { total += $7; count++ }} END { print total/count }' $input2`
  ycTMD=`awk '{if ($12=="'$TMD'" || ($12=="'$ECD'")) { total += $8; count++ }} END { print total/count }' $input2`
  zcTMD=`awk '{if ($12=="'$TMD'" || ($12=="'$ECD'")) { total += $9; count++ }} END { print total/count }' $input2`

  cexTMD=$(echo "$xcTMD - $xTMD" | bc)
  ceyTMD=$(echo "$ycTMD - $yTMD" | bc)
  cezTMD=$(echo "$zcTMD - $zTMD" | bc)

  xV2=$(echo "(($ceyTMD * $zVAxE) - ($yVAxE * $cezTMD))" | bc)
  yV2=$(echo "((($cexTMD * $zVAxE) - ($xVAxE * $cezTMD)) * -1)" | bc)
  zV2=$(echo "(($cexTMD * $yVAxE) - ($xVAxE * $ceyTMD))" | bc)

  #ECD
  xcECD=`awk '{if ($12 =="'$ECD'"){ total += $7; count++ }} END { print total/count }' $input` 
  ycECD=`awk '{if ($12 =="'$ECD'"){ total += $8; count++ }} END { print total/count }' $input`
  zcECD=`awk '{if ($12 =="'$ECD'"){ total += $9; count++ }} END { print total/count }' $input` 

  cexECD=$(echo "$xcECD - $xECD" | bc)
  ceyECD=$(echo "$ycECD - $yECD" | bc)
  cezECD=$(echo "$zcECD - $zECD" | bc)

  xV1=$(echo "(($ceyECD * $zVAxE) - ($cezECD * $yVAxE))" | bc)
  yV1=$(echo "((($cexECD * $zVAxE) - ($cezECD * $xVAxE)) * -1)" | bc)
  zV1=$(echo "(($cexECD * $yVAxE) - ($ceyECD * $xVAxE))" | bc)
 
  unit_vector1x=$(echo "scale=4; $xV1 / (sqrt($xV1^2 + $yV1^2 + $zV1^2))" | bc)
  unit_vector1y=$(echo "scale=4; $yV1 / (sqrt($xV1^2 + $yV1^2 + $zV1^2))" | bc)
  unit_vector1z=$(echo "scale=4; $zV1 / (sqrt($xV1^2 + $yV1^2 + $zV1^2))" | bc)

  unit_vector2x=$(echo "scale=4;  $xV2 / (sqrt($xV2^2 + $yV2^2 + $zV2^2))" | bc)
  unit_vector2y=$(echo "scale=4;  $yV2 / (sqrt($xV2^2 + $yV2^2 + $zV2^2))" | bc)
  unit_vector2z=$(echo "scale=4;  $zV2 / (sqrt($xV2^2 + $yV2^2 + $zV2^2))" | bc)
  
  dot_product=$(echo "scale=4; ($unit_vector1x * $unit_vector2x) + ($unit_vector1y * $unit_vector2y) + ($unit_vector1z * $unit_vector2z)" | bc)
  radians+=($dot_product)  
 
done

python angle.py "${radians[@]}"
