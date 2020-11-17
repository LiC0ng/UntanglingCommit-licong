"""
Model3: Use PACE to embed all AST nodes
"""

import os
import json
import random
import tensorflow as tf
import numpy as np
import network
from sampleJava import getData_nofinetune
from sklearn.metrics import confusion_matrix, accuracy_score
from argparse import ArgumentParser
from parameters import LEARN_RATE, EPOCHS, KERNEL


def getWordEmd(word):
    """PACE: combination of weighted character one-hot embedding"""

    listrechar = np.array([0.0 for i in range(0, len(listchar))])
    tt = 1
    for lchar in word:
        listrechar += np.array(((len(word) - tt + 1) * 1.0 / len(word)) * np.array(dicttChar[lchar]))
        tt += 1
    return listrechar


def train_model(embeddings):
    dictt = {}
    listrec = []
    file_list = os.listdir('dataset/features/features1')
    z = 0
    for file in file_list:
        file_path = 'dataset/features/features1/' + file
        if not os.path.exists(file_path):
            listrec.append(file)
            continue
        with open(file_path, 'r', encoding="utf-8") as faa:
            sample = json.loads(faa.read())
        if sample == "" or sample == " " or sample == "\n":
            z += 1
            listrec.append(file)
            continue
        dictt[file] = sample
    print("length of feature: " + str(len(dictt)))
    # print("invalid file number:", z)

    TrainDatalist = []
    file = open("dataset/dataset/train/" + data_type + ".txt", 'r')
    for line in file:
        if line == "" or line == " ":
            continue
        TrainDatalist.append(line)
    print('len ( TrainData ) = ', len(TrainDatalist))
    file.close()

    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    num_feats = len(getWordEmd('ReturnStmt'))
    nodes_node1, children_node1, nodes_node2, children_node2, res = network.init_net_nofinetune(num_feats, KERNEL)
    labels_node, loss_node = network.loss_layer(res)

    aaa = 0
    global_step = tf.Variable(0, trainable=False)
    learn_rate = tf.train.exponential_decay(LEARN_RATE, global_step, len(TrainDatalist), 0.9, True)
    optimizer = tf.train.GradientDescentOptimizer(learn_rate)
    train_step = optimizer.minimize(loss_node, global_step=global_step)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)  # config=tf.ConfigProto(device_count={'GPU':0}))
    sess.run(tf.global_variables_initializer())

    for global_step in range(1, EPOCHS + 1):
        k = 0
        random.shuffle(TrainDatalist)
        for line in TrainDatalist:
            line = line.rstrip('\n')
            train_data = line.split('\t')
            if len(train_data) != 3:
                break
            k += 1
            if (train_data[0] in listrec) or (train_data[1] in listrec):
                continue
            batch_labels = []
            nodes1, children1, nodes2, children2, la = getData_nofinetune(train_data, dictt, embeddings)
            batch_labels.append(la)
            _, err, r = sess.run(
                [train_step, loss_node, res],
                feed_dict={
                    nodes_node1: nodes1,
                    children_node1: children1,
                    nodes_node2: nodes2,
                    children_node2: children2,
                    labels_node: batch_labels
                }
            )
            learn_rate_var = sess.run(learn_rate)
            aaa += 1

    test_list = ['argouml', 'gwt', 'jruby', 'xstream', 'all']
    for name in test_list:
        print('start test: ' + name)
        correct_labels_test = []
        predictions_test = []
        for _ in range(0, 20):
            predictions_test.append([])

        ff = open("dataset/dataset/test/" + name + "/" + data_type + ".txt", 'r')
        line = "123"
        k = 0
        while line:
            line = ff.readline().rstrip('\n')
            test_data = line.split('\t')
            if len(test_data) != 3:
                break
            if (test_data[0] in listrec) or (test_data[1] in listrec):
                continue
            nodes1, children1, nodes2, children2, la = getData_nofinetune(test_data, dictt, embeddings)
            label = test_data[2]
            k += 1
            output = sess.run([res],
                            feed_dict={
                                nodes_node1: nodes1,
                                children_node1: children1,
                                nodes_node2: nodes2,
                                children_node2: children2,
                            }
                            )
            correct_labels_test.append(int(label))
            threaholder = -1.0
            for i in range(0, 20):
                if output[0] >= threaholder:
                    predictions_test[i].append(1)
                else:
                    predictions_test[i].append(-1)
                threaholder += 0.1
            with open("dataset/cluster/3/" + name + "/" + test_data[0].split('_')[0] + '_' + test_data[1].split('_')[0] + '.txt', 'a') as fout:
                fout.writelines(test_data[2] + '\t' + test_data[0] + '\t' + test_data[1] + '\t' + str(output[0]) + '\n')

        # The choice of the threshold will not affect the clustering results
        # We just investigate the max accuracy of our model's prediction of the relationship between chunks
        maxstep = 0
        maxaccuracy = 0
        for i in range(0, 20):
            accuracy = accuracy_score(correct_labels_test, predictions_test[i])
            if accuracy > maxaccuracy:
                maxaccuracy = accuracy
                maxstep = i
        threaholder = -1.0 + maxstep * 0.1
        cm = confusion_matrix(correct_labels_test,
                              predictions_test[maxstep], labels=[-1, 1])
        tn, fp, fn, tp = cm.ravel()
        accuracy = accuracy_score(correct_labels_test, predictions_test[maxstep])
        print("threaholder: " + str(threaholder))
        print("max combine precision_test:", tp / (tp + fp))
        print("max combine recall_test:", tp / (tp + fn))
        print("max seperate precision_test:", tn / (tn + fn))
        print("max seperate recall_test:", tn / (tn + fp))
        print("max accuracy_test:" + str(accuracy))
        print("tp:" + str(tp) + " tn:" + str(tn) + " fp:" + str(fp) + " fn:" + str(fn))
        # print(learn_rate_var)
        ff.close()


if __name__ == '__main__':
    listword = []

    parser = ArgumentParser()
    parser.add_argument("--type", dest="type", required=True)
    args = parser.parse_args()
    data_type = args.type

    with open("dataset/dict/withid.txt", 'r') as dict_file:
        content = dict_file.read()
        listt = content.split(" ")
    for word in listt:
        if word == "" or word == " ":
            continue
        listword.append(word)
    print("Length of dict: ", len(listword))
    dicttChar = {}

    def _onehot(i, total):
        return [1.0 if j == i else 0.0 for j in range(total)]
    listchar = ['7', 'I', 'E', 'D', 'u', 'C', 'Y', 'W', 'y', '9', 'X', 't', 'a', 'o', 'Z', 'b',
                'A', 'J', 'R', 'w', 'g', '3', 'B', 'l', '5', 'z', 'v', 'T', '2', 'd', 'e', 'M',
                'c', 'S', 'm', '4', 'K', 'O', 'f', 'i', 'Q', 'x', 'N', '1', 'r', 'p', 'G', 'k',
                'q', 'L', 'P', 'n', 'j', 'V', 'U', '6', '8', 'F', 's', 'h', 'H', '0', '_']
    for i in range(0, len(listchar)):
        dicttChar[listchar[i]] = _onehot(i, len(listchar))
    dictfinalem = {}
    t = 0
    for l in listword:
        t += 1
        dictfinalem[l] = getWordEmd(l)
    train_model(dictfinalem)
