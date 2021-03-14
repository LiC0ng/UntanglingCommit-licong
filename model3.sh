#!/usr/bin/env bash
###########################################################
PYTHON='python3'
###########################################################

mkdir -p dataset/cluster/3/argouml
mkdir -p dataset/cluster/3/gwt
mkdir -p dataset/cluster/3/jruby
mkdir -p dataset/cluster/3/xstream
mkdir -p dataset/cluster/3/all

${PYTHON} ./model3_idPACE_otherPACE.py --type ins
${PYTHON} ./model3_idPACE_otherPACE.py --type ino
${PYTHON} ./model3_idPACE_otherPACE.py --type its
${PYTHON} ./model3_idPACE_otherPACE.py --type ito