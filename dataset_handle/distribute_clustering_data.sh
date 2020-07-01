#!/usr/bin/env bash
###########################################################
CLUSTERING_DIR=dataset/clustering
DATA_TYPES=("ino" "ins" "ito" "its")
###########################################################

for repo in $(ls dataset/pre); do
    mkdir -p ${CLUSTERING_DIR}/${repo}
    rm ${CLUSTERING_DIR}/${repo}/*.csv
done

for DATA_TYPE in "${DATA_TYPES[@]}"; do
    INFO_DATA=${CLUSTERING_DIR}/${DATA_TYPE}_info.csv
    RESULT_DATA=${CLUSTERING_DIR}/${DATA_TYPE}.csv.results

    for line in $(paste -d' ' ${INFO_DATA} ${RESULT_DATA} | cut -d' ' -f1,4-7 | tr ' ' ','); do
        COMMIT_PAIR_ID=$(echo ${line} | cut -d',' -f2)
        PROJECT_NAME=$(echo ${COMMIT_PAIR_ID} | cut -d'_' -f1)
        COMMIT_PAIR_NAME=$(echo ${COMMIT_PAIR_ID} | cut -d'_' -f2-)
        OUT_FILE=${CLUSTERING_DIR}/${PROJECT_NAME}/${COMMIT_PAIR_NAME}.csv

        echo ${line} | cut -d',' -f1,3- >> ${OUT_FILE}
    done
done
