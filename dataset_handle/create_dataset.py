from argparse import ArgumentParser
import random

def create_dataset(index_dir, dest_dir, repo):
    type_list = ["ins", "ino", "its", "ito"]
    for type in type_list:
        train_true_file = index_dir + '/train/true/' + type + '.txt'
        train_false_file = index_dir + '/train/false/' + type + '.txt'
        with open(train_true_file, 'r') as true_file:
            positive_data = true_file.read().replace('\n\n', '\n').split('\n')
        with open(train_false_file, 'r') as false_file:
            negative_data = false_file.read().replace('\n\n', '\n').split('\n')
        minLen = min(len(positive_data), len(negative_data))
        random.shuffle(positive_data)
        random.shuffle(negative_data)
        output_path = dest_dir + '/train/' + type + '.txt'
        with open(output_path, 'a') as output_file:
            for i in range(minLen):
                if positive_data[i] == "" or negative_data[i] =="":
                    continue
                output_file.writelines(positive_data[i] + '\n')
                output_file.writelines(negative_data[i] + '\n')

    for type in type_list:
        test_true_file = index_dir + '/test/true/' + type + '.txt'
        test_false_file = index_dir + '/test/false/' + type + '.txt'
        with open(test_true_file, 'r') as true_file:
            positive_data = true_file.read().split('\n')
        with open(test_false_file, 'r') as false_file:
            negative_data = false_file.read().split('\n')
        output_path = dest_dir + '/test/all/' + type + '.txt'
        output_path_with_project = dest_dir + '/test/' + repo + '/' + type + '.txt'
        with open(output_path, 'a') as output_file, \
                open(output_path_with_project, 'a') as project_output_file:
            for data in positive_data:
                if data == "" or data == " " or data == "\n":
                    continue
                output_file.writelines(data + '\n')
                project_output_file.writelines(data + '\n')
            for data in negative_data:
                if data == "" or data == " " or data == "\n":
                    continue
                output_file.writelines(data + '\n')
                project_output_file.writelines(data + '\n')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--index_dir", dest="index_dir", required=True)
    parser.add_argument("--dest_dir", dest="dest_dir", required=True)
    parser.add_argument("--repo", dest="repo", required=True)
    args = parser.parse_args()
    create_dataset(args.index_dir, args.dest_dir, args.repo)
