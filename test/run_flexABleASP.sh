#!/usr/bin/env bash

# optional flags
#  -i use the incremental mode (by default just use the normal version)
#  -e enumerate defences (by default just show satisfiability)

# $1 = instance
# $2 = goal
# $3 = max moves (upper bound)

# sample run:
# ./run_flexABleASP.sh exp_acyclic_depvary_step10_batch_yyy01.pl w2 15
# ./run_flexABleASP.sh -e exp_acyclic_depvary_step10_batch_yyy01.pl w2 15
# ./run_flexABleASP.sh -i exp_acyclic_depvary_step10_batch_yyy01.pl w2 15

# TODO: set the paths here
FLEXABLEASP_DIR="/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp"
INSTANCES_DIR="/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-tests/instances/aspforaba"
CLINGO_DIR="/home/piotr/anaconda3/envs/potassco/bin/clingo"
# ----

enum=0

ENCODING=${FLEXABLEASP_DIR}/repo/encoding.lp

while getopts ie opt; do
  case ${opt} in
    i )
      # use the incremental version
      ENCODING=${FLEXABLEASP_DIR}/repo/incremental/encodingInc.lp
      ;;
    e )
      # echo "I should enum"
      enum=1
      ;;
  esac
done
shift $((OPTIND -1))




if [[ $enum -eq 0 ]] 
then
  # get info: SAT or not
  ${CLINGO_DIR} $ENCODING ${INSTANCES_DIR}/$1 1 --const goal=$2 --const maxMove=$3 --quiet=3  | grep 'SATISFIABLE\|CPU Time'
else
  # show defences
  ${CLINGO_DIR} $ENCODING ${INSTANCES_DIR}/$1 0 --const goal=$2 --const maxMove=$3 | grep -A 1 'Answer' | grep -v ^'Answer'
fi
