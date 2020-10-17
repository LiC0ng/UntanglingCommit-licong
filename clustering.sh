#!/usr/bin/env bash
###########################################################
PYTHON='python'
PROJECT_NAME=jruby
EXPERIMENT_NAME=rq1
PROJECT_DIR=dataset/cluster/3/${PROJECT_NAME}
###########################################################

for commit_pair_file in $(ls ${PROJECT_DIR}); do
    #echo clustering ${commit_pair_file}
    ${PYTHON} clustering.py -i ${PROJECT_DIR}/${commit_pair_file}
done
