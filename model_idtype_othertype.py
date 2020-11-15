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
    print("length of feature: " + str(len(dictt)))
    # print("invalid file number:", z)

    TrainDatalist = []
    file = open("dataset/dataset/traindata.txt", 'r')
    for line in file:
        if line == "" or line == " ":
            continue
        TrainDatalist.append(line)
    print('len ( TrainData ) = ', len(TrainDatalist))
    file.close()

    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    nodes_node1, children_node1, nodes_node2, children_node2, res = network.init_net_finetune(feature_size, embeddingg, KERNAL_NUM)
    labels_node, loss_node = network.loss_layer(res)
    # tf.summary.scalar('loss', loss_node)
    aaa = 0
    global_step = tf.Variable(0, trainable=False)
    LEARN_RATE = tf.train.exponential_decay(0.002, global_step, len(TrainDatalist), 0.8, True)
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

        if global_step % 5 == 0:
            test_list = ['argouml_test', 'gwt_test', 'jaxen_test', 'jruby_test', 'xstream_test', 'totaltest']
            for name in test_list:
                print('start: ' + name)
                correct_labels_test = []
                predictions_test = []
                for reci in range(0, 15):
                    predictions_test.append([])
                ff = open("dataset/dataset/" + name + ".txt", 'r')
                line = "123"
                k = 0
                while line:
                    line = ff.readline().rstrip('\n')
                    l = line.split('\t')
                    if len(l) != 3:
                        break
                    if (l[0] in listrec) or (l[1] in listrec):
                        continue
                    nodes11, children1, nodes22, children2, _ = getData_notokenfinetune(l, dictt, embeddings)
                    label = l[2]
                    k += 1
                    output = sess.run([res],
                                    feed_dict={
                                        nodes_node1: nodes11,
                                        children_node1: children1,
                                        nodes_node2: nodes22,
                                        children_node2: children2,
                                    }
                                    )
                    correct_labels_test.append(int(label))
                    threaholder = -0.5
                    for i in range(0, 15):
                        if output[0] >= threaholder:
                            predictions_test[i].append(1)
                        else:
                            predictions_test[i].append(-1)
                        threaholder += 0.1
                maxstep = 0
                maxaccuracy = 0
                for i in range(0, 15):
                    accuracy = accuracy_score(correct_labels_test, predictions_test[i])
                    if accuracy > maxaccuracy:
                        maxaccuracy = accuracy
                        maxstep = i
                threaholder = -0.5 + maxstep * 0.1
                cm = confusion_matrix(correct_labels_test, predictions_test[maxstep])
                tn, fp, fn, tp = cm.ravel()
                # p = precision_score(correct_labels_test, predictions_test, average='binary')
                # r = recall_score(correct_labels_test, predictions_test, average='binary')
                accuracy = accuracy_score(correct_labels_test, predictions_test[maxstep])
                print(global_step)
                print("threaholder:")
                print(threaholder)
                print("max combine precision_test:", tp / (tp + fp))
                print("max combine recall_test:", tp / (tp + fn))
                print("max seperate precision_test:", tn / (tn + fn))
                print("max seperate recall_test:", tn / (tn + fp))
                print("max accuracy_test:" + str(accuracy))
                print("tp:" + str(tp) + " tn:" + str(tn) + " fp:" + str(fp) + " fn:" + str(fn))
                print('current learn rate:' + learn_rate_var)
                ff.close()

            # cluster_list = ['argouml', 'gwt', 'jaxen', 'jruby', 'xstream']
            # for name in cluster_list:
            #     print("\nstart cluster:" + name)
            #     composite_commit_list = os.listdir('dataset/dataset/cluster/' + name)
            #     for composite_commit in composite_commit_list:
            #         fin = open('dataset/dataset/cluster/' + name + '/' + composite_commit, 'r')
            #         fout = open("dataset/cluster/1/" + name + "/" + composite_commit, 'w')
            #         for line in fin:
            #             if line == "" or line == " ":
            #                 continue
            #             data = line.rstrip('\n')
            #             pair_info = data.split('\t')
            #             nodes11, children1, nodes22, children2, _ = getData_notokenfinetune(pair_info, dictt, embeddings)
            #             output = sess.run([res],
            #                             feed_dict={
            #                                     nodes_node1: nodes11,
            #                                     children_node1: children1,
            #                                     nodes_node2: nodes22,
            #                                     children_node2: children2,
            #                             }
            #                             )
            #             fout.writelines(pair_info[2] + '\t' + pair_info[0] + '\t' + pair_info[1] + '\t' + str(output[0]) + '\n')
            #         fout.close()
            #         fin.close()


if __name__ == '__main__':
    dictt = {}
    dictta = {}
    listta = list()

    parser = ArgumentParser()
    parser.add_argument("--feature_size", dest="feature_size", required=True)
    parser.add_argument("--kernal_num", dest="kernal_num", required=True)
    args = parser.parse_args()

    EPOCHS = 30
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
