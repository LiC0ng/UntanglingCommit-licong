from argparse import ArgumentParser


def ReadFileDatas(index_path, isCommit, isTrain):
    FileNamelist = []
    file = open(index_path, 'r')
    for line in file:
        if line == "" or line == " ":
            continue
        if isCommit:
            FileNamelist.append(line.strip('\n'))
        else:
            FileNamelist.append(line)
    if isCommit and isTrain:
        print('len ( Train Commit ) = ', len(FileNamelist))
    elif isCommit and not isTrain:
        print('len ( Test Commit ) = ', len(FileNamelist))
    elif not isCommit:
        print('len ( Data ) = ', len(FileNamelist))
    file.close()
    return FileNamelist


def WriteDatasToFile(data_path, repo):
    train_data = open(data_path + '/traindata.txt', mode='a')
    for commit in trueTrainCommitList:
        for data in untangled_list:
            if(data.find(commit) >= 0):
                train_data.writelines(data)

    for commit in falseTrainCommitList:
        for data in tangled_list:
            commitPair = commit.split(" ")
            if(data.find(commitPair[0]) >= 0 and data.find(commitPair[1]) >= 0):
                train_data.writelines(data)
    train_data.close()

    test_data = open(data_path + '/totaltest.txt', mode='a')
    test_project_data = open(data_path + '/' + repo + '_test.txt', mode='a')
    for commit in trueTestCommitList:
        for data in untangled_list:
            if(data.find(commit) >= 0):
                test_data.writelines(data)
                test_project_data.writelines(data)

    for commit in falseTestCommitList:
        for data in tangled_list:
            commitPair = commit.split(" ")
            if(data.find(commitPair[0]) >= 0 and data.find(commitPair[1]) >= 0):
                test_data.writelines(data)
                test_project_data.writelines(data)
    test_data.close()
    test_project_data.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--source_dir", dest="source_dir", required=True)
    parser.add_argument("--dest_dir", dest="dest_dir", required=True)
    parser.add_argument("--repo", dest="repo", required=True)
    parser.add_argument("--commits_dir", dest="commits_dir", required=True)
    args = parser.parse_args()
    trueTestCommitList = ReadFileDatas(args.commits_dir + '/test/true.csv', True, False)
    falseTestCommitList = ReadFileDatas(args.commits_dir + '/test/false.csv', True, False)
    trueTrainCommitList = ReadFileDatas(args.commits_dir + '/train/true.csv', True, True)
    falseTrainCommitList = ReadFileDatas(args.commits_dir + '/train/false.csv', True, True)

    tangled_list = ReadFileDatas(args.source_dir + '/tangled.txt', False, False)
    untangled_list = ReadFileDatas(args.source_dir + '/untangled.txt', False, False)

    WriteDatasToFile(args.dest_dir, args.repo)
