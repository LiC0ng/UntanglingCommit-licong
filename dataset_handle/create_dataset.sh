#!/bin/bash
###########################################################
PYTHON='python'
###########################################################
DATA_DIR=dataset/dataset

mkdir -p ${DATA_DIR}

rm -r ${DATA_DIR}/*

echo "Creating dataset"
for repo in $(ls dataset/pre); do
  PRE_DATASET=dataset/pre/${repo}
  INDEX_DIR=${PRE_DATASET}/index
  COMMIT_DIR=${PRE_DATASET}/commits

  ${PYTHON} dataset_handle/create_dataset.py --source_dir ${INDEX_DIR} \
    --dest_dir ${DATA_DIR}  --repo ${repo} --commits_dir ${COMMIT_DIR}
done
echo "Create dataset complete"