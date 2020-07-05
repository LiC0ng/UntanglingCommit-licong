#!/bin/bash
# modified on sanada's code: https://github.com/tklab-group/UntanglingCommit-sanada 
###########################################################
PYTHON='python3'
EXTRACTOR_JAR=JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar
###########################################################

for repo in $(ls dataset/pre); do
  SOURCE_DATASET=dataset/repositories/zeller-${repo}
  PRE_DATASET=dataset/pre/${repo}
  COMMIT_CSV=${PRE_DATASET}/commits/all.csv
  TANGLED_CSV=${PRE_DATASET}/commits/tangled.csv
  RANGE_DIR=${PRE_DATASET}/ranges
  FEATURE_WITH_ID_DIR=${PRE_DATASET}/features1
  FEATURE_WITHOUT_ID_DIR=${PRE_DATASET}/features2

  mkdir -p ${RANGE_DIR}
  mkdir -p ${FEATURE_WITH_ID_DIR}
  mkdir -p ${FEATURE_WITHOUT_ID_DIR}

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

done
