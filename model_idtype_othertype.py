import os
import json
import random
import tensorflow as tf
import numpy as np
import network
from sampleJava import getData_notokenfinetune
from sklearn.metrics import confusion_matrix, accuracy_score
from argparse import ArgumentParser


def train_model(embeddings):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    nodes_node1, children_node1, nodes_node2, children_node2, res = network.init_net_finetune(feature_size, embeddingg, KERNAL_NUM)
    labels_node, loss_node = network.loss_layer(res)
    # tf.summary.scalar('loss', loss_node)
    aaa = 0
    global_step = tf.Variable(0, trainable=False)
    LEARN_RATE = tf.train.exponential_decay(0.005, global_step, 60424, 0.9, True)
    optimizer = tf.train.GradientDescentOptimizer(LEARN_RATE)
    train_step = optimizer.minimize(loss_node, global_step=global_step)
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)  # config=tf.ConfigProto(device_count={'GPU':0}))
    sess.run(tf.global_variables_initializer())

    # with tf.name_scope('saver'):
    #     saver = tf.train.Saver()
    #     summaries = tf.summary.merge_all()
    #     writer = tf.summary.FileWriter('logs', sess.graph)
    # checkfile = os.path.join('logs', 'cnn_tree.ckpt')

    dictt = {}
    listrec = []
    file_list = os.listdir('dataset/features/features2')
    z = 0
    for file in file_list:
        file_path = 'dataset/features/features2' + '/' + file
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
    # print("length of dictt: " + str(len(dictt)))
    # print("invalid file number:", z)

    TrainDatalist = []
    file = open("dataset/dataset/traindata.txt", 'r')
    for line in file:
        if line == "" or line == " ":
            continue
        TrainDatalist.append(line)
    # print('len ( TrainData ) = ', len(TrainDatalist))
    file.close()

    for global_step in range(1, EPOCHS + 1):
        k = 0
        random.shuffle(TrainDatalist)
        for line in TrainDatalist:
            line = line.rstrip('\n')
            l = line.split('\t')
            if len(l) != 3:
                continue
            k += 1
            if (l[0] in listrec) or (l[1] in listrec):
                continue
            nodes11, children1, nodes22, children2, batch_labels = getData_notokenfinetune(l, dictt, embeddings)
            _, err, r = sess.run(
                [train_step, loss_node, res],
                feed_dict={
                    nodes_node1: nodes11,
                    children_node1: children1,
                    nodes_node2: nodes22,
                    children_node2: children2,
                    labels_node: batch_labels,
                }
            )
            # if aaa % 1000 == 0:
            #     print('Epoch:', epoch,
            #           'Step:', aaa,
            #           'Loss:', err,
            #           'R:', r,
            #           )
            #     writer.add_summary(summary, aaa)
            learn_rate_var = sess.run(LEARN_RATE)
            aaa += 1
        print(learn_rate_var)
        # Validation Step
        # print("\nstart validation:")
        if global_step % 5 == 0:
            correct_labels_dev = []
            predictions_dev = []
            for i in range(0, 15):
                predictions_dev.append([])
            ff = open("dataset/dataset/devdata.txt", 'r')
            line = "123"
            k = 0
            maxaccuracy = -1.0
            while line:
                line = ff.readline().rstrip('\n')
                l = line.split('\t')
                if len(l) != 3:
                    break
                k += 1
                label = l[2]
                if (l[0] in listrec) or (l[1] in listrec):
                    continue
                nodes11, children1, nodes22, children2, _ = getData_notokenfinetune(l, dictt, embeddings)
                output = sess.run([res],
                                feed_dict={
                                    nodes_node1: nodes11,
                                    children_node1: children1,
                                    nodes_node2: nodes22,
                                    children_node2: children2,
                                }
                                )
                correct_labels_dev.append(int(label))
                threaholder = -0.7
                for i in range(0, 15):
                    if output[0] >= threaholder:
                        predictions_dev[i].append(1)
                    else:
                        predictions_dev[i].append(-1)
                    threaholder += 0.1
            for i in range(0, 15):
                accuracy = accuracy_score(correct_labels_dev, predictions_dev[i])
                if accuracy > maxaccuracy:
                    maxaccuracy = accuracy
                    maxstep = i
            threaholder = -0.7 + maxstep * 0.1
            # print("threaholder:")
            # print(threaholder)
            # p = precision_score(correct_labels_dev, predictions_dev[maxstep], average='binary')
            # r = recall_score(correct_labels_dev, predictions_dev[maxstep], average='binary')
            # print("recall_valid:" + str(r))
            # print("precision_valid:" + str(p))
            # print("f1score_valid:" + str(maxf1value))
            ff.close()

        # start test
        # test_list = ['argouml_test', 'gwt_test', 'jaxen_test', 'jruby_test', 'xstream_test', 'totaltest']
            print(global_step)
            test_list = ['argouml_test', 'gwt_test', 'jaxen_test', 'jruby_test', 'xstream_test', 'totaltest']
            for name in test_list:
                print("\nstarttest:" + name)
                correct_labels_test = []
                predictions_test = []
                ff = open("dataset/dataset/" + name + '.txt', 'r')
                line = "123"
                k = 0
                while line:
                    line = ff.readline().rstrip('\n')
                    l = line.split('\t')
                    if len(l) != 3:
                        break
                    k += 1
                    label = l[2]
                    if (l[0] in listrec) or (l[1] in listrec):
                        continue
                    nodes11, children1, nodes22, children2, _ = getData_notokenfinetune(l, dictt, embeddings)
                    output = sess.run([res],
                                    feed_dict={
                                            nodes_node1: nodes11,
                                            children_node1: children1,
                                            nodes_node2: nodes22,
                                            children_node2: children2,
                                    }
                                    )
                    correct_labels_test.append(int(label))
                    threaholder = -0.7 + maxstep * 0.1
                    if output[0] >= threaholder:
                        predictions_test.append(1)
                    else:
                        predictions_test.append(-1)
                cm = confusion_matrix(correct_labels_test, predictions_test)
                tn, fp, fn, tp = cm.ravel()
                # p = precision_score(correct_labels_test, predictions_test, average='binary')
                # r = recall_score(correct_labels_test, predictions_test, average='binary')
                accuracy = accuracy_score(correct_labels_test, predictions_test)
                print("threaholder:")
                print(threaholder)
                print("combine precision_test:", tp / (tp + fp))
                print("combine recall_test:", tp / (tp + fn))
                print("seperate precision_test:", tn / (tn + fn))
                print("seperate recall_test:", tn / (tn + fp))
                print("accuracy_test:" + str(accuracy))
                print("tp:" + str(tp) + " tn:" + str(tn) + " fp:" + str(fp) + " fn:" + str(fn))
                print(learn_rate_var)
                ff.close()

        cluster_list = ['argouml', 'gwt', 'jaxen', 'jruby', 'xstream']
        for name in cluster_list:
            print("\nstart cluster:" + name)
            ff = open("dataset/dataset/" + name + 'cd.txt', 'r')
            for line in ff:
                if line == "" or line == " ":
                    continue
                data = line.rstrip('\n')
                pair = data.split('\t')
                wfile = open("dataset/cluster/1/" + name + "/" + pair[0] + "_" + pair[1] + ".txt", 'w')
                tangled = open("dataset/pre/" + name + "/index/tangled.txt", 'r')
                tangled_line = "123"
                while tangled_line:
                    tangled_line = tangled.readline().rstrip('\n')
                    if tangled_line == "" or tangled_line == " ":
                        continue
                    if(not ((pair[0] in tangled_line) and (pair[1] in tangled_line))):
                        continue
                    tangled_l = tangled_line.split('\t')
                    tangled_label = tangled_l[2]
                    nodes11, children1, nodes22, children2, _ = getData_notokenfinetune(tangled_l, dictt, embeddings)
                    output = sess.run([res],
                                    feed_dict={
                                            nodes_node1: nodes11,
                                            children_node1: children1,
                                            nodes_node2: nodes22,
                                            children_node2: children2,
                                    }
                                    )
                    wfile.writelines(tangled_label + '\t' + tangled_l[0] + '\t' + tangled_l[1] + '\t' + str(output[0]) + '\n')
                untangled = open("dataset/pre/" + name + "/index/untangled.txt", 'r')
                untangled_line = "123"
                while untangled_line:
                    untangled_line = untangled.readline().rstrip('\n')
                    if untangled_line == "" or untangled_line == " ":
                        continue
                    if(not ((pair[0] in untangled_line) or (pair[1] in untangled_line))):
                        continue
                    untangled_l = untangled_line.split('\t')
                    untangled_label = untangled_l[2]
                    nodes11, children1, nodes22, children2, _ = getData_notokenfinetune(untangled_l, dictt, embeddings)
                    output = sess.run([res],
                                    feed_dict={
                                            nodes_node1: nodes11,
                                            children_node1: children1,
                                            nodes_node2: nodes22,
                                            children_node2: children2,
                                    }
                                    )
                    wfile.writelines(untangled_label + '\t' + untangled_l[0] + '\t' + untangled_l[1] + '\t' + str(output[0]) + '\n')
                wfile.close()
                tangled.close()
                untangled.close()
            ff.close()


if __name__ == '__main__':
    dictt = {}
    dictta = {}
    listta = list()

    parser = ArgumentParser()
    parser.add_argument("--feature_size", dest="feature_size", required=True)
    parser.add_argument("--kernal_num", dest="kernal_num", required=True)
    args = parser.parse_args()

    EPOCHS = 50
    KERNAL_NUM = int(args.kernal_num)
    feature_size = int(args.feature_size)

    def _onehot(i, total):
        return [1.0 if j == i else 0.0 for j in range(total)]
    listchar = ['ExpressionStmt', 'ContinueStmt', 'ClassOrInterfaceType', 'MarkerAnnotationExpr', 'ThrowStmt',
                'SuperExpr', 'MethodDeclaration', 'ThisExpr', 'ArrayCreationExpr', 'ConditionalExpr',
                'StringLiteralExpr', 'WhileStmt', 'CatchClause', 'BinaryExpr', 'ObjectCreationExpr',
                'ReturnStmt', 'EnclosedExpr', 'BlockStmt', 'NameExpr', 'DoubleLiteralExpr',
                'AnnotationDeclaration', 'AssertStmt', 'TypeParameter', 'ClassExpr',
                'TryStmt', 'BooleanLiteralExpr', 'LabeledStmt', 'SingleTypeImportDeclaration', 'EmptyStmt',
                'PrimitiveType', 'IfStmt', 'VoidType', 'SynchronizedStmt', 'ForStmt',
                'SwitchEntryStmt', 'TypeImportOnDemandDeclaration', 'MethodCallExpr', 'ArrayInitializerExpr', 'FieldAccessExpr',
                'NormalAnnotationExpr', 'CompilationUnit', 'CharLiteralExpr', 'AnnotationMemberDeclaration', 'ExplicitConstructorInvocationStmt',
                'BreakStmt', 'ConstructorDeclaration', 'ArrayBracketPair', 'ForeachStmt',
                'VariableDeclarator', 'SingleMemberAnnotationExpr', 'ClassOrInterfaceDeclaration', 'InitializerDeclaration', 'DoStmt',
                'InstanceOfExpr', 'WildcardType', 'PackageDeclaration', 'CastExpr', 'SwitchStmt',
                'Parameter', 'IntegerLiteralExpr', 'UnaryExpr', 'EmptyMemberDeclaration', 'ArrayAccessExpr',
                'ArrayCreationLevel', 'FieldDeclaration', 'VariableDeclarationExpr', 'NullLiteralExpr', 'MemberValuePair',
                'AssignExpr', 'LongLiteralExpr']
    for l in listchar:
        listta.append(np.random.normal(0, 0.1, feature_size).astype(np.float32))
    embeddingg = np.asarray(listta)
    embeddingg = tf.Variable(embeddingg)
    for i in range(len(listchar)):
        dictta[listchar[i]] = i
    train_model(dictta)
