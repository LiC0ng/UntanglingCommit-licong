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

done
