#!/bin/bash
###########################################################
PYTHON='python'
###########################################################
DATA_DIR=dataset/dataset

mkdir -p ${DATA_DIR}
mkdir -p ${DATA_DIR}/test/all

echo "Creating dataset"
for repo in $(ls dataset/pre); do
  PRE_DATASET=dataset/pre/${repo}
  INDEX_DIR=${PRE_DATASET}/index
  mkdir -p ${DATA_DIR}/cluster/${repo}
  mkdir -p ${DATA_DIR}/train
  mkdir -p ${DATA_DIR}/test/${repo}

  ${PYTHON} dataset_handle/create_dataset.py --index_dir ${INDEX_DIR} \
    --dest_dir ${DATA_DIR}  --repo ${repo}
done
echo "Create dataset complete"
