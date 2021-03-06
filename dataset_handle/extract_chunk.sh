#!/bin/bash
###########################################################
PYTHON='python3'
EXTRACTOR_JAR=JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar
###########################################################
FEATURE_DIR=dataset/features
TOTAL_FEATURES_WITH_ID=${FEATURE_DIR}/features1
TOTAL_FEATURES_WITHOUT_ID=${FEATURE_DIR}/features2
# DATA_DIR=dataset/dataset
DICT_DIR=dataset/dict

mkdir -p ${FEATURE_DIR}
mkdir -p ${TOTAL_FEATURES_WITH_ID}
mkdir -p ${TOTAL_FEATURES_WITHOUT_ID}
# mkdir -p ${DATA_DIR}
mkdir -p ${DICT_DIR}

for repo in $(ls dataset/pre); do
  SOURCE_DATASET=dataset/repositories/zeller-${repo}
  PRE_DATASET=dataset/pre/${repo}
  COMMIT_CSV=${PRE_DATASET}/commits/all.csv
#   TANGLED_CSV=${PRE_DATASET}/commits/tangled.csv
#   TRAIN_DIR=${PRE_DATASET}/commits/train
#   TEST_DIR=${PRE_DATASET}/commits/test 
  RANGE_DIR=${PRE_DATASET}/ranges
  RAW_FEATURE_WITH_ID_DIR=${PRE_DATASET}/raw_feature/features1
  RAW_FEATURE_WITHOUT_ID_DIR=${PRE_DATASET}/raw_feature/features2
  FEATURE_WITH_ID_DIR=${PRE_DATASET}/features/features1
  FEATURE_WITHOUT_ID_DIR=${PRE_DATASET}/features/features2
#   INDEX_DIR=${PRE_DATASET}/index

  mkdir -p ${RANGE_DIR}
  mkdir -p ${RAW_FEATURE_WITH_ID_DIR}
  mkdir -p ${RAW_FEATURE_WITHOUT_ID_DIR}
  mkdir -p ${FEATURE_WITH_ID_DIR}
  mkdir -p ${FEATURE_WITHOUT_ID_DIR}
#   mkdir -p ${INDEX_DIR}/train/true
#   mkdir -p ${INDEX_DIR}/train/false
#   mkdir -p ${INDEX_DIR}/test/true
#   mkdir -p ${INDEX_DIR}/test/false

#   echo "Getting ${repo} tangled commits"
#   ${PYTHON} dataset_handle/tangle_commit_artificial.py -r ${SOURCE_DATASET} -i ${COMMIT_CSV} -o ${TANGLED_CSV}

  echo "Fetching ${repo} change chunk info"
  ${PYTHON} dataset_handle/parse_git_diff.py --repo ${SOURCE_DATASET} \
    --commit_file ${COMMIT_CSV} --range_dir ${RANGE_DIR}

  echo "Extracting ${repo} AST subtree"
  ${PYTHON} JavaExtractor/extract.py --repo ${SOURCE_DATASET} \
    --commit_file ${COMMIT_CSV} --range_dir ${RANGE_DIR} --feature_dir0 ${RAW_FEATURE_WITHOUT_ID_DIR} \
    --max_path_length 8 --max_path_width 2 --num_threads 64 \
    --feature_dir1 ${RAW_FEATURE_WITH_ID_DIR} --jar ${EXTRACTOR_JAR}
  
  echo "Seperating ${repo} features"
  ${PYTHON} dataset_handle/seperate_features.py --commit_file ${COMMIT_CSV} \
    --feature_dir ${RAW_FEATURE_WITH_ID_DIR} --out_dir ${FEATURE_WITH_ID_DIR}

  ${PYTHON} dataset_handle/seperate_features.py --commit_file ${COMMIT_CSV} \
  --feature_dir ${RAW_FEATURE_WITHOUT_ID_DIR} --out_dir ${FEATURE_WITHOUT_ID_DIR}

#   echo "Creating ${repo} index of dataset"
#   ${PYTHON} dataset_handle/dataset_index.py --data_dir ${TRAIN_DIR} \
#   --feature_dir0 ${RAW_FEATURE_WITHOUT_ID_DIR}  --index_dir ${INDEX_DIR} \
#   --out_dir ${INDEX_DIR}/train

#   ${PYTHON} dataset_handle/dataset_index.py --data_dir ${TEST_DIR} \
#   --feature_dir0 ${RAW_FEATURE_WITHOUT_ID_DIR}  --index_dir ${INDEX_DIR} \
#   --out_dir ${INDEX_DIR}/test

  echo "Merging ${repo} features"
  cp -r ${FEATURE_WITH_ID_DIR}/* ${TOTAL_FEATURES_WITH_ID}
  cp -r ${FEATURE_WITHOUT_ID_DIR}/* ${TOTAL_FEATURES_WITHOUT_ID}

done

echo "Extracting dict from features"
${PYTHON} dataset_handle/create_dict.py --feature_dir ${FEATURE_DIR} \
--dict_dir ${DICT_DIR}
