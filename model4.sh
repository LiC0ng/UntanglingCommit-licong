#!/usr/bin/env bash
###########################################################
PYTHON='python3'
###########################################################

mkdir -p dataset/cluster/4/argouml
mkdir -p dataset/cluster/4/gwt
mkdir -p dataset/cluster/4/jruby
mkdir -p dataset/cluster/4/xstream
mkdir -p dataset/cluster/4/all

${PYTHON} ./model4_idPACE_otherN2N.py --type ins
${PYTHON} ./model4_idPACE_otherN2N.py --type ino
${PYTHON} ./model4_idPACE_otherN2N.py --type its
${PYTHON} ./model4_idPACE_otherN2N.py --type ito
${PYTHON} ./calculate_result.py --model_num 4