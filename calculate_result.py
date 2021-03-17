from argparse import ArgumentParser

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--model_num", dest="model_num", required=True)
    args = parser.parse_args()
    model_num = args.model_num

    tp, tn, fp, fn = 0
    with open("dataset/cluster/" + model_num + "/total_result.csv", 'r') as total_result_file:
        total_result = total_result_file.read().split('\n')
    for result in total_result:
        results = result.split('\t')
        tp += int(results[1])
        tn += int(results[2])
        fp += int(results[3])
        fn += int(results[4])
    print('------------Model ' + model_num + ' total result ------------' )
    print("combine precision:", tp / (tp + fp))
    print("combine recall:", tp / (tp + fn))
    print("seperate precision:", tn / (tn + fn))
    print("seperate recall:", tn / (tn + fp))
    print("accuracy:", (tp + tn) / (tp + tn + fp + fn))
    print("tp:" + str(tp) + " tn:" + str(tn) +
            " fp:" + str(fp) + " fn:" + str(fn))
    print('------------------------------------')
