#!/bin/bash
###########################################################
PYTHON='python'
###########################################################
echo "-------------------Model 1-------------------"
RESULT_DIR=dataset/cluster/1
for repo in $(ls dataset/pre); do
  PRE_DATASET=dataset/pre/${repo}
  TEST_DATA_DIR=${PRE_DATASET}/commits/test
  OUT_PATH=dataset/result/1
  mkdir -p ${OUT_PATH}/${repo}

  echo "Concating ${repo} predicted result"
  ${PYTHON} dataset_handle/concat_cluster_data.py --result_dir ${RESULT_DIR}/${repo} \
   --out_dir ${OUT_PATH}/${repo}
done
echo "---------------------------------------------"

echo "-------------------Model 2-------------------"
RESULT_DIR=dataset/cluster/2
for repo in $(ls dataset/pre); do
  PRE_DATASET=dataset/pre/${repo}
  TEST_DATA_DIR=${PRE_DATASET}/commits/test
  OUT_PATH=dataset/result/2
  mkdir -p ${OUT_PATH}/${repo}

  echo "Concating ${repo} predicted result"
  ${PYTHON} dataset_handle/concat_cluster_data.py --result_dir ${RESULT_DIR}/${repo} \
   --out_dir ${OUT_PATH}/${repo}
done
echo "---------------------------------------------"

echo "-------------------Model 3-------------------"
RESULT_DIR=dataset/cluster/3
for repo in $(ls dataset/pre); do
  PRE_DATASET=dataset/pre/${repo}
  TEST_DATA_DIR=${PRE_DATASET}/commits/test
  OUT_PATH=dataset/result/3
  mkdir -p ${OUT_PATH}/${repo}

  echo "Concating ${repo} predicted result"
  ${PYTHON} dataset_handle/concat_cluster_data.py --result_dir ${RESULT_DIR}/${repo} \
   --out_dir ${OUT_PATH}/${repo}
done
echo "---------------------------------------------"

echo "-------------------Model 4-------------------"
RESULT_DIR=dataset/cluster/4
for repo in $(ls dataset/pre); do
  PRE_DATASET=dataset/pre/${repo}
  TEST_DATA_DIR=${PRE_DATASET}/commits/test
  OUT_PATH=dataset/result/4
  mkdir -p ${OUT_PATH}/${repo}

  echo "Concating ${repo} predicted result"
  ${PYTHON} dataset_handle/concat_cluster_data.py --result_dir ${RESULT_DIR}/${repo} \
   --out_dir ${OUT_PATH}/${repo}
done
echo "---------------------------------------------"