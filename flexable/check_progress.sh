#!/bin/bash

echo $1

TOT_CORR=$(cat $1 | grep 'corr' | wc -l)
TOT_INC=$(cat $1 | grep 'inc' | wc -l)
TOT_TIMEOUT=$(cat $1 | grep 'TIMEOUT' | wc -l)
TOT=$(cat $1 | wc -l)


echo "TOTAL: $(($TOT-1))"
echo "CORR.: $(($TOT_CORR-1))"
echo "INC. : $TOT_INC"
echo "TIME.: $TOT_TIMEOUT"
echo "STEP M: $(awk -F',' '$(NF-1) == "corr"{print $NF}' flexable.csv | sort -nr | head -n 1)"
