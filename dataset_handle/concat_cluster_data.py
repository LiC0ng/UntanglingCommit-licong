from argparse import ArgumentParser
import os


def concat(result_path, output_path):
    result_list = os.listdir(result_path)

    for result in result_list:
        meta_data = result.rstrip('.txt').split('_')
        # print('flag1: ' + meta_data[0] + '_' + meta_data[1])
        if meta_data[0] == meta_data[1]:
            # print('continue:' + meta_data[0] + '_' + meta_data[1])
            continue
        with open(output_path + '/' + result, 'a') as out_file:
            with open(result_path + '/' + result, 'r') as result1:
                out_file.write(result1.read())

            if os.path.exists(result_path + '/' + meta_data[0] + '_' + meta_data[0] + '.txt'):
                with open(result_path + '/' + meta_data[0] + '_' + meta_data[0] + '.txt', 'r') as result2:
                    out_file.write(result2.read())
            else:
                print('no such file1: ' + result_path + '/' + meta_data[0] + '_' + meta_data[0] + '.txt')

            if os.path.exists(result_path + '/' + meta_data[1] + '_' + meta_data[1] + '.txt'):
                with open(result_path + '/' + meta_data[1] + '_' + meta_data[1] + '.txt', 'r') as result3:
                    out_file.write(result3.read())
            else:
                print('no such file2: ' + result_path + '/' + meta_data[1] + '_' + meta_data[1] + '.txt')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--result_dir", dest="result_dir", required=True)
    parser.add_argument("--out_dir", dest="out_dir", required=True)
    args = parser.parse_args()
    concat(args.result_dir, args.out_dir)
