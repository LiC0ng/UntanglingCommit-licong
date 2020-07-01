#!/usr/bin/env bash
###########################################################
PYTHON='python3'
REPOS_DIR=dataset/pre
CLUSTERING_DATA_OUT=dataset/clustering
###########################################################

mkdir -p ${CLUSTERING_DATA_OUT}

cat ${REPOS_DIR}/*/datas/clustering/ins.csv > ${CLUSTERING_DATA_OUT}/ins_info.csv
cat ${REPOS_DIR}/*/datas/clustering/ino.csv > ${CLUSTERING_DATA_OUT}/ino_info.csv
cat ${REPOS_DIR}/*/datas/clustering/its.csv > ${CLUSTERING_DATA_OUT}/its_info.csv
cat ${REPOS_DIR}/*/datas/clustering/ito.csv > ${CLUSTERING_DATA_OUT}/ito_info.csv

cat ${CLUSTERING_DATA_OUT}/ins_info.csv | cut -d ' ' -f -3 > ${CLUSTERING_DATA_OUT}/ins.csv
cat ${CLUSTERING_DATA_OUT}/ino_info.csv | cut -d ' ' -f -3 > ${CLUSTERING_DATA_OUT}/ino.csv
cat ${CLUSTERING_DATA_OUT}/its_info.csv | cut -d ' ' -f -3 > ${CLUSTERING_DATA_OUT}/its.csv
cat ${CLUSTERING_DATA_OUT}/ito_info.csv | cut -d ' ' -f -3 > ${CLUSTERING_DATA_OUT}/ito.csv

echo "concatenation done"
