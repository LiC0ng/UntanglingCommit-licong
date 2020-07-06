#!/bin/bash
# modified on sanada's code: https://github.com/tklab-group/UntanglingCommit-sanada 
###########################################################
PYTHON='python3'
EXTRACTOR_JAR=JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar
###########################################################
FEATURE=dataset/features
TOTAL_FEATURES_WITH_ID=${FEATURE}/features1
TOTAL_FEATURES_WITHOUT_ID=${FEATURE}/features2

mkdir -p ${FEATURE}
mkdir -p ${TOTAL_FEATURES_WITH_ID}
mkdir -p ${TOTAL_FEATURES_WITHOUT_ID}

for repo in $(ls dataset/pre); do
  SOURCE_DATASET=dataset/repositories/zeller-${repo}
  PRE_DATASET=dataset/pre/${repo}
  COMMIT_CSV=${PRE_DATASET}/commits/all.csv
  TANGLED_CSV=${PRE_DATASET}/commits/tangled.csv
  RANGE_DIR=${PRE_DATASET}/ranges
  FEATURE_WITH_ID_DIR=${PRE_DATASET}/features1
  FEATURE_WITHOUT_ID_DIR=${PRE_DATASET}/features2
  INDEX_DIR=${PRE_DATASET}/index

  mkdir -p ${RANGE_DIR}
  mkdir -p ${FEATURE_WITH_ID_DIR}
  mkdir -p ${FEATURE_WITHOUT_ID_DIR}
  mkdir -p ${INDEX_DIR}

  echo "Getting ${repo} tangled commits"
  ${PYTHON} dataset_handle/tangle_commit_artificial.py -r ${SOURCE_DATASET} -i ${COMMIT_CSV} -o ${TANGLED_CSV}

  echo "Fetching ${repo} change range info"
  ${PYTHON} dataset_handle/parse_git_diff.py --repo ${SOURCE_DATASET} \
    --commit_file ${COMMIT_CSV} --range_dir ${RANGE_DIR}

  echo "Extracting ${repo} tokens"
  ${PYTHON} JavaExtractor/extract.py --repo ${SOURCE_DATASET} \
    --commit_file ${COMMIT_CSV} --range_dir ${RANGE_DIR} --feature_dir0 ${FEATURE_WITHOUT_ID_DIR} \
    --max_path_length 8 --max_path_width 2 --num_threads 64 \
    --feature_dir1 ${FEATURE_WITH_ID_DIR} --jar ${EXTRACTOR_JAR}
  
  echo "Seperating ${repo} features"
  ${PYTHON} dataset_handle/seperate_features.py --commit_file ${COMMIT_CSV} \
    --feature_dir ${FEATURE_WITH_ID_DIR}

  ${PYTHON} dataset_handle/seperate_features.py --commit_file ${COMMIT_CSV} \
  --feature_dir ${FEATURE_WITHOUT_ID_DIR}

  echo "Creating ${repo} index of dataset"
  ${PYTHON} dataset_handle/dataset_index.py --commit_file ${COMMIT_CSV} \
  --feature_dir0 ${FEATURE_WITHOUT_ID_DIR}  --index_dir ${INDEX_DIR} \
  --tangled_file ${TANGLED_CSV}

  echo "Concating ${repo} index and features"
  cp -r ${FEATURE_WITH_ID_DIR}/* ${TOTAL_FEATURES_WITH_ID}
  cp -r ${FEATURE_WITHOUT_ID_DIR}/* ${TOTAL_FEATURES_WITHOUT_ID}
  # TODO: automatic concating index

done

echo "Seperating dataset"
${PYTHON} dataset_handle/seperate_dataset.py