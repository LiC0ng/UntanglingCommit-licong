#!/usr/bin/env bash
###########################################################
PYTHON='python3'
###########################################################

for repo in $(ls dataset/pre); do
    PRE_DATASET=dataset/pre/${repo}
    COMMIT_DIR=${PRE_DATASET}/commits
    TEST_DATA_DIR=${COMMIT_DIR}/test
    CLUSTERING_DATA_DIR=${COMMIT_DIR}/clustering
    FEATURE_DIR=${PRE_DATASET}/features
    CLUSTERING_OUT_DIR=${PRE_DATASET}/datas/clustering

    for line in $(cat ${TEST_DATA_DIR}/false.csv | tr ' ' ','); do
        COMMIT_PAIR_ID=$(echo ${line} | tr ',' '_')
        COMMIT_PAIR_IN_DIR=${CLUSTERING_DATA_DIR}/${COMMIT_PAIR_ID}
        COMMIT_PAIR_OUT_DIR=${CLUSTERING_OUT_DIR}/${COMMIT_PAIR_ID}

        mkdir -p ${COMMIT_PAIR_IN_DIR}
        echo ${line} | tr ',' '\n' > ${COMMIT_PAIR_IN_DIR}/true.csv
        echo ${line} | tr ',' ' ' > ${COMMIT_PAIR_IN_DIR}/false.csv

        mkdir -p ${COMMIT_PAIR_OUT_DIR}/unpadded
        mkdir -p ${COMMIT_PAIR_OUT_DIR}/padded
        rm -f ${COMMIT_PAIR_OUT_DIR}/unpadded/*
        rm -f ${COMMIT_PAIR_OUT_DIR}/padded/*

        ${PYTHON} dataset_handle/pre_clustering.py --token_data_dir ${FEATURE_DIR} \
            --input_dir ${COMMIT_PAIR_IN_DIR} --output_dir ${COMMIT_PAIR_OUT_DIR} \
            --max_tokens 200 --commit_pair_id ${repo}_${COMMIT_PAIR_ID}
    done

    cat ${CLUSTERING_OUT_DIR}/*/padded/inner_s* > ${CLUSTERING_OUT_DIR}/ins.csv
    cat ${CLUSTERING_OUT_DIR}/*/padded/inner_o* > ${CLUSTERING_OUT_DIR}/ino.csv
    cat ${CLUSTERING_OUT_DIR}/*/padded/inter_s* > ${CLUSTERING_OUT_DIR}/its.csv
    cat ${CLUSTERING_OUT_DIR}/*/padded/inter_o* > ${CLUSTERING_OUT_DIR}/ito.csv
done
