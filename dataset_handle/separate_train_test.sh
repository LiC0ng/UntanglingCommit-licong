#!/bin/bash
###########################################################
PYTHON='python3'
REPOS_DIR=dataset/pre
###########################################################

for repo in $(ls ${REPOS_DIR}); do
    PRE_DATASET=${REPOS_DIR}/${repo}
    COMMIT_DIR=${PRE_DATASET}/commits
    COMMIT_CSV=${COMMIT_DIR}/all.csv
    TANGLED_CSV=${COMMIT_DIR}/tangled.csv
    TRAIN_DATA_DIR=${COMMIT_DIR}/train
    TEST_DATA_DIR=${COMMIT_DIR}/test

    TEMP=`echo $(cat ${COMMIT_CSV} | wc -l)/10 | bc`
    TANGLED_DATA_NUM=$(( ${TEMP} > 5 ? ${TEMP} : 5 ))

    mkdir -p ${TRAIN_DATA_DIR}
    mkdir -p ${TEST_DATA_DIR}

    ${PYTHON} dataset_handle/tangle_commit_artificial.py -r ${SOURCE_DATASET} -i ${COMMIT_CSV} -o ${TANGLED_CSV}

    cat ${TANGLED_CSV} | shuf | head -n ${TANGLED_DATA_NUM} > ${TANGLED_CSV}.trimmed

    ${PYTHON} dataset_handle/split_with_tangle.py -s ${COMMIT_CSV} -t ${TANGLED_CSV}.trimmed -o ${COMMIT_DIR}

    rm ${TANGLED_CSV}.trimmed

    mv ${COMMIT_DIR}/train.csv ${TRAIN_DATA_DIR}/true.csv
    ${PYTHON} dataset_handle/tangle_commit_artificial.py -r ${SOURCE_DATASET} -i ${TRAIN_DATA_DIR}/true.csv -o ${TRAIN_DATA_DIR}/false.csv

    mv ${COMMIT_DIR}/test.csv ${TEST_DATA_DIR}/true.csv
    ${PYTHON} dataset_handle/tangle_commit_artificial.py -r ${SOURCE_DATASET} -i ${TEST_DATA_DIR}/true.csv -o ${TEST_DATA_DIR}/false.csv

    echo "${repo} done"
done
