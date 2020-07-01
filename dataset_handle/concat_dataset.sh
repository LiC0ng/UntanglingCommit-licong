#!/usr/bin/env bash
###########################################################
PYTHON='python3'
REPOS_DIR=dataset/pre
TRAIN_DATA_OUT=dataset/train
TEST_DATA_OUT=dataset/test
###########################################################

for repo in $(ls ${REPOS_DIR}); do
    REPO_TRAIN_DIR=${REPOS_DIR}/${repo}/datas/train
    ${PYTHON} dataset_handle/flatten_dataset.py -i ${REPO_TRAIN_DIR}/padded
    mkdir -p ${REPO_TRAIN_DIR}/flatten
    mv ${REPO_TRAIN_DIR}/padded/*fl* ${REPO_TRAIN_DIR}/flatten/
done

mkdir -p ${TRAIN_DATA_OUT}
mkdir -p ${TEST_DATA_OUT}

cat ${REPOS_DIR}/*/datas/train/flatten/inner_o* | shuf > ${TRAIN_DATA_OUT}/ino.csv
cat ${REPOS_DIR}/*/datas/train/flatten/inter_o* | shuf > ${TRAIN_DATA_OUT}/ito.csv
cat ${REPOS_DIR}/*/datas/train/flatten/inner_s* | shuf > ${TRAIN_DATA_OUT}/ins.csv
cat ${REPOS_DIR}/*/datas/train/flatten/inter_s* | shuf > ${TRAIN_DATA_OUT}/its.csv

cat ${REPOS_DIR}/*/datas/test/padded/inner_o* | shuf > ${TEST_DATA_OUT}/ino.csv
cat ${REPOS_DIR}/*/datas/test/padded/inter_o* | shuf > ${TEST_DATA_OUT}/ito.csv
cat ${REPOS_DIR}/*/datas/test/padded/inner_s* | shuf > ${TEST_DATA_OUT}/ins.csv
cat ${REPOS_DIR}/*/datas/test/padded/inter_s* | shuf > ${TEST_DATA_OUT}/its.csv

echo "concatenation done"
