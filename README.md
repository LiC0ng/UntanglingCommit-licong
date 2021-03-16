# Abstract
Untangling Composite Changes based on Tree-based Convolution Neural Network

# Research Question
* RQ1: Evaluate the performance of our proposed embedding method

* RQ2: How model difference affect the relationship prediction among chunks.

* RQ3: Can our approach outperform the existing approach in clustering


# Environment
* Tensorflow 2.0
* Python 3.5.2
* Docker

# Directory
* UntanglingCommit-licong
    * `dataset`: Place of repositories and the results for each project
        * `pre/(project-name)/commits/all.csv`: Single-task commits' list for each project
        * `repositories`: Place for each project
    * `dataset_handle`: Place of scripts to process the dataset
    * `JavaExtractor`: Implementation of JavaParser

# Dataset
We conduct experiments on four Java project gathered by Herzig and Zeller[1]
* ArgoUML
* Google Web Toolkit(GWT)
* JRuby
* XStream

These data sets can be obtained from the data published by Ward Muylaert[2]
> https://soft.vub.ac.be/~wmuylaer/repository/2018scam.replication.tar.gz

# Dataset Prepare
After cloning this repository, you need to put each project's repository in `dataset/repositories/`. These projects are ignored by git because of their large size and will not be added to the repository.

1. Firstly, download the dataset from tklab's file server. Access this link `http://www.sa.cs.titech.ac.jp/local/wiki/?admin/srvs/pepenero` for details. Download the dataset from `pepenero/share/sanada/tool/UntanglingCommit-sanada/dataset` 
2. Secondly, unzip `zeller-(project-name)-(data).tar.gz`, rename them to `zeller-(project-name)`, and put them in `dataset/repositories`
3. Lastly, check the initial state of the dataset. You should have single-task commits's list in `dataset/pre/(project名)/commits/all.csv` and repositories in `dataset/repositories/zeller-(project-name)`

You can run `./initialize.sh` to check the experiment environment of this repository

Other files under the dataset directory are automatically generated as the experimental procedure.


# Experiment Process
## Notice:
1. For step 1~3, please run their commands in the docker environment
2. If you want to re-split the dataset or re-experiment, please run `initialize.sh` to initialize the experiment environment
3. Before you initialize the experiment environment, save your experiment data if necessary


## RQ 1,2

### 1. Extracting chunk info and AST subtree
Run the command below to extract chunk info and AST subtree
>./dataset_handle/extract_chunk.sh

For each project:
* Extracting their chunks' information, and save the information in `dataset/pre/(project-name)/ranges/`
* Extracting the chunk's corresponding AST subtree and save the information in:
    * `dataset/pre/(project-name)/features/features1/` (no id flag)
    * `dataset/pre/(project-name)/features/features1/` (with id flag)

For all projects:
* Merger their AST to:
    * `dataset/features/features1/` (no id flag)
    * `dataset/features/features1/` (with id flag)
* Extract their toekn vocabulary:
    * `dataset/dict/nodetype.txt` (node type name)
    * `dataset/dict/onlyid.txt` (identifiers with id flag)

### 2. Spitting dataset to trainset and testset
Run the command below to split dataset for each project
>./dataset_handle/separate_train_test.sh

For each project, using the single-task commits' list `dataset/pre/(project-name)/commits/all.csv` to generate composite commits `dataset/pre/(project-name)/commits/tangled.csv`, and spliting them into 
* positive train set :`dataset/pre/(project-name)/commits/train/true.csv`
* negetive train set :`dataset/pre/(project-name)/commits/train/false.csv`
* positive test set :`dataset/pre/(project-name)/commits/test/true.csv`
* negetive test set :`dataset/pre/(project-name)/commits/test/false.csv`

* Generate chunk pairs and classify the chunks pairs into four categories:
    * ins(inner file same type): `dataset/pre/(project-name)/index/(train&test)/(true&false)/ins.txt`
    * ino(inner file opposite type): `dataset/pre/(project-name)/index/(train&test)/(true&false)/ino.txt`
    * its(inter file same type): `dataset/pre/(project-name)/index/(train&test)/(true&false)/its.txt`
    * ito(inter file opposite type): `dataset/pre/(project-name)/index/(train&test)/(true&false)/ito.txt`

For each project and for each category's chunk pair, balance their positive data and negative data, and merge the balanced data to:
* `dataset\dataset\train\(catagory-name).txt` (train set)
* `dataset\dataset\test\(project-name)\(category-name).txt` (test set)

### 3. Train and test four models
Run the commands below to train and test our four models
>./model1.sh

>./model2.sh

>./model3.sh

>./model4.sh

The relationship prediction results are shown in the terminal, and the related score are saved in `dataset/cluster/(model-num)/(project-name)`

For RQ2, Sanada's approach can be accessed in this link： `https://github.com/tklab-group/UntanglingCommit-sanada`

## RQ 3

### 4. Distribute the join probability for each artificial composite commit
Run the command below to distribute the predicted result to each artificial composite commit
>./dataset_handle/cluster_data_concat.sh

The outputs are placed in `dataset/result/(model-num)/(project-name))`

### 5. Executing clustering
Run the command below to output the untangling accuracy of each project's composite commits
>./clustering.sh

The outputs are shown in the terminal.




# Reference
[1] Kim Herzig and Andreas Zeller. 2013. The impact of tangled code changes. In <i>Proceedings of the 10th Working Conference on Mining Software Repositories</i> (<i>MSR '13</i>). IEEE Press, 121–130.

[2] Muylaert, W. and De Roover, C., "Untangling Composite Commits Using Program Slicing", Proc. SCAM 2018