#!/bin/bash
###########################################################
PYTHON='python3'
REPOS_DIR=dataset/pre
###########################################################

DATA_DIR=dataset/dataset
mkdir -p ${DATA_DIR}/train
mkdir -p ${DATA_DIR}/test/all

for repo in $(ls ${REPOS_DIR}); do
    SOURCE_DATASET=dataset/repositories/zeller-${repo}
    PRE_DATASET=${REPOS_DIR}/${repo}
    COMMIT_DIR=${PRE_DATASET}/commits
    COMMIT_CSV=${COMMIT_DIR}/all.csv
    TANGLED_CSV=${COMMIT_DIR}/tangled.csv
    TRAIN_DATA_DIR=${COMMIT_DIR}/train
    TEST_DATA_DIR=${COMMIT_DIR}/test
    INDEX_DIR=${PRE_DATASET}/index
    RAW_FEATURE_WITH_ID_DIR=${PRE_DATASET}/raw_feature/features1
    RAW_FEATURE_WITHOUT_ID_DIR=${PRE_DATASET}/raw_feature/features2

    TEMP=`echo $(cat ${COMMIT_CSV} | wc -l)/15 | bc`
    TANGLED_DATA_NUM=$(( ${TEMP} > 4 ? ${TEMP} : 4 ))

    mkdir -p ${TRAIN_DATA_DIR}
    mkdir -p ${TEST_DATA_DIR}
    mkdir -p ${INDEX_DIR}/train/true
    mkdir -p ${INDEX_DIR}/train/false
    mkdir -p ${INDEX_DIR}/test/true
    mkdir -p ${INDEX_DIR}/test/false
    mkdir -p ${DATA_DIR}/test/${repo}

    ${PYTHON} dataset_handle/tangle_commit_artificial.py -r ${SOURCE_DATASET} -i ${COMMIT_CSV} -o ${TANGLED_CSV}

    cat ${TANGLED_CSV} | shuf | head -n ${TANGLED_DATA_NUM} > ${TANGLED_CSV}.trimmed

    ${PYTHON} dataset_handle/split_with_tangle.py -s ${COMMIT_CSV} -t ${TANGLED_CSV}.trimmed -o ${COMMIT_DIR}

    rm ${TANGLED_CSV}.trimmed

    mv ${COMMIT_DIR}/train.csv ${TRAIN_DATA_DIR}/true.csv
    ${PYTHON} dataset_handle/tangle_commit_artificial.py -r ${SOURCE_DATASET} -i ${TRAIN_DATA_DIR}/true.csv -o ${TRAIN_DATA_DIR}/false.csv

    mv ${COMMIT_DIR}/test.csv ${TEST_DATA_DIR}/true.csv
    ${PYTHON} dataset_handle/tangle_commit_artificial.py -r ${SOURCE_DATASET} -i ${TEST_DATA_DIR}/true.csv -o ${TEST_DATA_DIR}/false.csv

    echo "Creating ${repo} index of dataset"
    ${PYTHON} dataset_handle/dataset_index.py --data_dir ${TRAIN_DATA_DIR} \
    --feature_dir0 ${RAW_FEATURE_WITHOUT_ID_DIR}  --index_dir ${INDEX_DIR} \
    --out_dir ${INDEX_DIR}/train

    ${PYTHON} dataset_handle/dataset_index.py --data_dir ${TEST_DATA_DIR} \
    --feature_dir0 ${RAW_FEATURE_WITHOUT_ID_DIR}  --index_dir ${INDEX_DIR} \
    --out_dir ${INDEX_DIR}/test

    ${PYTHON} dataset_handle/create_dataset.py --index_dir ${INDEX_DIR} \
    --dest_dir ${DATA_DIR}  --repo ${repo}

    echo "${repo} done"
done
