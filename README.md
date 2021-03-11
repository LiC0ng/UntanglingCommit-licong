# Abstract
Untangling Composite Changes based on Tree-based Convolution Nerual Network

# Research Question
* RQ1: Evaluate the performance of our proposed embedding method

* RQ2: How model difference affect the relationship prediction among chunks.

* RQ3: Can our approach outperform the existing approach in clustering


# Environment
* Tensorflow 2.0
* Python 3.6
* Docker

# Dataset
We conduct experiments on four Java project gathered by Herzig and Zeller[1]
* ArgoUML
* Google Web Toolkit(GWT)
* Jruby
* XStream

These data sets can be obtained from the data published by Ward Muylaert[2]
> https://soft.vub.ac.be/~wmuylaer/repository/2018scam.replication.tar.gz

# Directory
* UntanglingCommit-licong
    * dataset
        * Place of repositorie and the results for each project
    * dataset_handle
        * Place of scripts to process dataset
    * JavaExtractor
        * Implemetion of JavaParser

# Experiment Process
## RQ 1,2

### 1. Spitting dataset to trainset and testset
Run the command below to split dataset for each project
>./dataset_handle/separate_train_test.sh

For each project, using the single-task commits' list `dataset/pre/(project-name)/commits/all.csv` to generate composite commits `dataset/pre/(project-name)/commits/tangled.csv`, and spliting them into 
* positive train set :`dataset/pre/(project-name)/commits/train/true.csv`
* negetive train set :`dataset/pre/(project-name)/commits/train/false.csv`
* positive test set :`dataset/pre/(project-name)/commits/test/true.csv`
* negetive test set :`dataset/pre/(project-name)/commits/test/false.csv`

### 2. Extracting chunk info and AST subtree
Run the command below to extract chunk info and AST subtree
>./dataset_handle/dataset_handle.sh

For each project:
* Extracting their chunks' information, and save the information in `dataset/pre/(project-name)/ranges/`
* Extracting the chunk's corresponding AST subtree and save the information in:
    * `dataset/pre/(project-name)/features/features1/` (no id flag)
    * `dataset/pre/(project-name)/features/features1/` (with id flag)
* Generate chunk pairs and classify the chunks pairs into four categories:
    * ins(inner file same type): `dataset/pre/(project-name)/index/(train&test)/(true&false)/ins.txt`
    * ino(inner file opposite type): `dataset/pre/(project-name)/index/(train&test)/(true&false)/ino.txt`
    * its(inter file same type): `dataset/pre/(project-name)/index/(train&test)/(true&false)/its.txt`
    * ito(inter file opposite type): `dataset/pre/(project-name)/index/(train&test)/(true&false)/ito.txt`

For all projects:
* Merger their AST to:
    * `dataset/features/features1/` (no id flag)
    * `dataset/features/features1/` (with id flag)
* Extract their vocabulary:
    * `dataset/dict/nodetype.txt` (node type name)
    * `dataset/dict/onlyid.txt` (identifiers with id flag)

### 3. Genarate index of input data
Run the command below to generate index of input data
>./dataset_handle/create_dataset.sh

For each project and for each category's chunk pair, balance their positive data and negative data, and merge the balanced data to:
* `dataset\dataset\train\(catagory-name).txt` (train set)
* `dataset\dataset\test\(project-name)\(category-name).txt` (test set)

### 4. Train and test four models
Run the commands below to train and test our four models
>./model1.sh

>./model2.sh

>./model3.sh

>./model4.sh

The relationship prediction result are shown in terminal, and the related score are saved in `dataser/cluster/(model-num)/(project-name)`

For RQ2, Sanada's approach can be accessed in this link： `https://github.com/tklab-group/UntanglingCommit-sanada`

## RQ 3

### 5. Distribute the join probability for each artificial composite commit
Run the command below to distribute the join probability for each artificial composite commit
>./dataset_handle/cluster_data_concat.sh

The outputs are placed in `dataset/result/(model-num)/(project-name))`

### 6. Executing clustering
Run the command below to output the untangling accuracy of each project's composte commits
>./clustering.sh

The output are shown in terminal.




# Reference
[1] Kim Herzig and Andreas Zeller. 2013. The impact of tangled code changes. In <i>Proceedings of the 10th Working Conference on Mining Software Repositories</i> (<i>MSR '13</i>). IEEE Press, 121–130.

[2] Muylaert, W. and De Roover, C., “Untangling Composite Commits Using Program Slicing”, Proc. SCAM 2018