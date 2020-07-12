#!/bin/bash
###########################################################
PYTHON='python3'
###########################################################
DATA_DIR=dataset/dataset

mkdir -p ${DATA_DIR}

rm -r ${DATA_DIR}/*

echo "Creating dataset"
for repo in $(ls dataset/pre); do
  PRE_DATASET=dataset/pre/${repo}
  INDEX_DIR=${PRE_DATASET}/index

  ${PYTHON} dataset_handle/create_dataset.py --source_dir ${INDEX_DIR} \
    --dest_dir ${DATA_DIR}  --repo ${repo}
done
echo "Create dataset complete"