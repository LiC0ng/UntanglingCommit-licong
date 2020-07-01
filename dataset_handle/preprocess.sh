#!/usr/bin/env bash
###########################################################
PYTHON='python3'
EXTRACTOR_JAR=JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar
###########################################################

SHORT_FLAG="FALSE"
while getopts s OPT
do
  case $OPT in
    "s" ) SHORT_FLAG="TRUE" ;;
  esac
done

for repo in $(ls dataset/pre); do
  SOURCE_DATASET=dataset/repositories/zeller-${repo}
  PRE_DATASET=dataset/pre/${repo}
  COMMIT_CSV=${PRE_DATASET}/commits/all.csv
  RANGE_DIR=${PRE_DATASET}/ranges
  FEATURE_DIR=${PRE_DATASET}/features
  TRAIN_DATA_DIR=${PRE_DATASET}/commits/train
  TEST_DATA_DIR=${PRE_DATASET}/commits/test
  DATASET_DIR=${PRE_DATASET}/datas
  HISTOGRAM_FILE=${DATASET_DIR}/dict.txt

  mkdir -p ${RANGE_DIR}
  mkdir -p ${FEATURE_DIR}
  mkdir -p ${DATASET_DIR}/train/unpadded
  mkdir -p ${DATASET_DIR}/train/padded
  mkdir -p ${DATASET_DIR}/test/unpadded
  mkdir -p ${DATASET_DIR}/test/padded
  rm ${DATASET_DIR}/train/unpadded/*
  rm ${DATASET_DIR}/train/padded/*
  rm ${DATASET_DIR}/test/unpadded/*
  rm ${DATASET_DIR}/test/padded/*

  if [ $SHORT_FLAG = "FALSE" ]; then
    echo "Fetching code change range info"
    ${PYTHON} dataset_handle/parse_git_diff.py --repo ${SOURCE_DATASET} \
      --commit_file ${COMMIT_CSV} --range_dir ${RANGE_DIR}

    echo "Extracting tokens"
    ${PYTHON} JavaExtractor/extract.py --repo ${SOURCE_DATASET} \
      --commit_file ${COMMIT_CSV} --range_dir ${RANGE_DIR} --feature_dir ${FEATURE_DIR} \
      --max_path_length 8 --max_path_width 2 --num_threads 64 \
      --jar ${EXTRACTOR_JAR}
  fi

  # atomic commitのリストと atomic commit pair のリストを読み込む。
  echo "Creating chunk pairs"
  ${PYTHON} dataset_handle/preprocess.py --token_data_dir ${FEATURE_DIR} \
    --train_data_dir ${TRAIN_DATA_DIR} --test_data_dir ${TEST_DATA_DIR} \
    --max_tokens 200 --output_dir ${DATASET_DIR}

  echo "Creating histograms from the training data"
  cat ${DATASET_DIR}/train/padded/* | cut -d' ' -f2- | tr ' ' '\n' | tr -s ',' '\n' | awk '{n[$0]++} END {for (i in n) print i,n[i]}' > ${HISTOGRAM_FILE}

  ${PYTHON} dataset_handle/dump_histogram.py --word_vocab_size 1301136 \
    --word_histogram ${HISTOGRAM_FILE} --output_dir ${DATASET_DIR}
done
