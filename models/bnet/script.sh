#!/bin/bash --posix


for f in *.bnet
do
  echo Processing $f
  num_of_attractors=`./cabean -compositional 2 $f| grep 'number of attractors = ' | head -n 1 | sed 's/[^0-9]*//g'`
  if [[ $num_of_attractors -gt 1024 ]]; then 
    echo Model $f too big
    continue
  fi
  i=0
  control_kernels=()
  while [ $i -ne $num_of_attractors ]
  do
    i=$(($i+1))
    result=`gtimeout 5s ./cabean -compositional 2 -control TTC -tin $i $f| grep 'Control set' | head -n 1 | grep -o -i '=' | wc -l`
    control_kernels+=($result)
  done 
  echo Processed $f attractors count: $num_of_attractors control kernels: ${control_kernels[*]}
done