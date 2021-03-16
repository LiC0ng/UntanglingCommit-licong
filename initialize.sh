#!/usr/bin/env bash
###########################################################

cat<<-eof
Input corresponding number:

1-Initialize all (Start from step 1 again, re-split train set and test set)
2-Clear experiment data (Start from step 4 again, re-experiment on the same train and test set)
3-Exit

notice: Please save the experiment data before if necessary
eof
read -p "*Input**:" cmd
case $cmd in
1)
        rm -rf ./dataset/cluster
        rm -rf ./dataset/result
        rm -rf ./dataset/dataset
        rm -rf ./dataset/dict
        rm -rf ./dataset/features
        rm -rf ./dataset/pre/*/features
        rm -rf ./dataset/pre/*/ranges
        rm -rf ./dataset/pre/*/index
        rm -rf ./dataset/pre/*/raw_feature
        rm -rf ./dataset/pre/*/commits/test
        rm -rf ./dataset/pre/*/commits/train
        rm -rf ./dataset/pre/*/commits/tangled.csv
        echo "Complete";;
2)
        rm -rf ./dataset/cluster
        rm -rf ./dataset/result
        echo "Complete";;
3)
        echo "exited";;
*)
        echo "errpr:please in input (1,2,3)";;
esac
