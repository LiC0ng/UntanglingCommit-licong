#!/usr/bin/env bash
###########################################################
PYTHON='python3'
###########################################################

mkdir -p dataset/cluster/1/argouml
mkdir -p dataset/cluster/1/gwt
mkdir -p dataset/cluster/1/jruby
mkdir -p dataset/cluster/1/xstream
mkdir -p dataset/cluster/1/all

${PYTHON} ./model1_idN2N_otherN2N.py --type ins
${PYTHON} ./model1_idN2N_otherN2N.py --type ino
${PYTHON} ./model1_idN2N_otherN2N.py --type its
${PYTHON} ./model1_idN2N_otherN2N.py --type ito
${PYTHON} ./calculate_result.py --model_num 1