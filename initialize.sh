#!/usr/bin/env bash
###########################################################

cat<<-eof
Input corresponding number:

0.Initial state check(Check the initial state of this repository)
1.Initialize entire environment (Start from step 1 again)
2.Clear Train and Test dataset(Start from step 2 again, re-split the dataset)
3.Clear experiment data (Start from step 3 again, re-experiment on the same train and test set)
4.Exit

notice: Please save the experiment data before if necessary
eof
read -p "*Input**:" cmd
case $cmd in
0)
    if [ ! -f "./dataset/pre/argouml/commits/all.csv" ] ;then
        echo "file '/dataset/pre/argouml/commits/all.csv' not exist"
    else
        echo "ok"
    fi
    
    if [ ! -f "./dataset/pre/gwt/commits/all.csv" ];then
        echo "file '/dataset/pre/gwt/commits/all.csv' not exist"
    else
        echo "ok"
    fi
    
    if [ ! -f "./dataset/pre/jruby/commits/all.csv" ];then
        echo "file '/dataset/pre/jruby/commits/all.csv' not exist"
    else
        echo "ok"
    fi
    
    if [ ! -f "./dataset/pre/xstream/commits/all.csv" ];then
        echo "file '/dataset/pre/xstream/commits/all.csv' not exist"
    else
        echo "ok"
    fi
    
    if [ ! -d "./dataset/repositories/zeller-argouml" ];then
        echo "repository '/dataset/repositories/zeller-argouml' not exist"
    else
        echo "ok"
    fi
    
    if [ ! -d "./dataset/repositories/zeller-gwt" ];then
        echo "repository '/dataset/repositories/zeller-gwt' not exist"
    else
        echo "ok"
    fi
    
    if [ ! -d "./dataset/repositories/zeller-jruby" ];then
        echo "repository '/dataset/repositories/zeller-jruby' not exist"
    else
        echo "ok"
    fi
    
    if [ ! -d "./dataset/repositories/zeller-xstream" ];then
        echo "repository '/dataset/repositories/zeller-xstream' not exist"
    else
        echo "ok"
    fi
    
    echo "Complete";;
1)
    rm -rf ./dataset/dict
    rm -rf ./dataset/features
    rm -rf ./dataset/pre/*/features
    rm -rf ./dataset/pre/*/ranges
    rm -rf ./dataset/pre/*/raw_feature

    rm -rf ./dataset/dataset
    rm -rf ./dataset/pre/*/index
    rm -rf ./dataset/pre/*/commits/test
    rm -rf ./dataset/pre/*/commits/train
    rm -rf ./dataset/pre/*/commits/tangled.csv

    rm -rf ./dataset/cluster
    rm -rf ./dataset/result

    echo "Complete";;
2)
    rm -rf ./dataset/dataset
    rm -rf ./dataset/pre/*/index
    rm -rf ./dataset/pre/*/commits/test
    rm -rf ./dataset/pre/*/commits/train
    rm -rf ./dataset/pre/*/commits/tangled.csv

    rm -rf ./dataset/cluster
    rm -rf ./dataset/result
    echo "Complete";;
3)
    rm -rf ./dataset/cluster
    rm -rf ./dataset/result
    echo "Complete";;
4)
    echo "exited";;
*)
    echo "errpr:please in input (0,1,2,3,4)";;
esac
