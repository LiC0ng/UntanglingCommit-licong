#!/usr/bin/env bash
###########################################################
PYTHON='python3'
###########################################################

mkdir -p dataset/cluster/2/argouml
mkdir -p dataset/cluster/2/gwt
mkdir -p dataset/cluster/2/jruby
mkdir -p dataset/cluster/2/xstream
mkdir -p dataset/cluster/2/all

${PYTHON} ./model2_idN2N_otherN2N.py --type ins
${PYTHON} ./model2_idN2N_otherN2N.py --type ino
${PYTHON} ./model2_idN2N_otherN2N.py --type its
${PYTHON} ./model2_idN2N_otherN2N.py --type ito