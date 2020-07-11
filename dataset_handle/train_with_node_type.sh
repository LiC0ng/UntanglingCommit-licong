#!/bin/bash
###########################################################
PYTHON='python3'
###########################################################
DATA_DIR=dataset/dataset
DATA_INDEX_DIR=dataset/index
DICT_DIR=dataset/dict
FEATURE_DIR=dataset/features

mkdir -p ${DATA_DIR}
mkdir -p ${DATA_INDEX_DIR}
mkdir -p ${DICT_DIR}

echo "Shuffling and Seperating dataset"
${PYTHON} dataset_handle/seperate_dataset.py --data_dir ${DATA_DIR} \
--index_dir ${DATA_INDEX_DIR}

echo "Extracting dict from features"
${PYTHON} dataset_handle/create_dict.py --feature_dir ${FEATURE_DIR} \
--dict_dir ${DICT_DIR}