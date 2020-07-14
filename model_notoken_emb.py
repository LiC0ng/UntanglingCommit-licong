import os
import json
import random
import tensorflow as tf
import numpy as np
import network
from sampleJava import getData_notokenfinetune
from parameters import EPOCHS, LEARN_RATE
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix


def train_model(embeddings):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    num_feats = 100
    nodes_node1, children_node1, nodes_node2, children_node2, res = network.init_net_finetune(num_feats, embeddingg)
    aaa = 1
    labels_node, loss_node = network.loss_layer(res)
    optimizer = tf.train.GradientDescentOptimizer(LEARN_RATE)
    train_step = optimizer.minimize(loss_node)
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)  # config=tf.ConfigProto(device_count={'GPU':0}))
    sess.run(tf.global_variables_initializer())
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
    print("length of dictt: " + str(len(dictt)))
    print("invalid file number:", z)

    TrainDatalist = []
    file = open("dataset/dataset/traindata.txt", 'r')
    for line in file:
        if line == "" or line == " ":
            continue
        TrainDatalist.append(line)
    print('len ( TrainData ) = ', len(TrainDatalist))
    file.close()

    for epoch in range(1, EPOCHS + 1):
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
            if aaa % 1000 == 0:
                print('Epoch:', epoch,
                      'Step:', aaa,
                      'Loss:', err,
                      'R:', r,
                      )
            aaa += 1
        # Validation Step
        print("\nstart validation:")
        correct_labels_dev = []
        predictions_dev = []
        for i in range(0, 15):
            predictions_dev.append([])
        ff = open("dataset/dataset/devdata.txt", 'r')
        line = "123"
        k = 0
        maxf1value = -1.0
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
            f1score = f1_score(correct_labels_dev, predictions_dev[i], average='binary')
            if f1score > maxf1value:
                maxf1value = f1score
                maxstep = i
        threaholder = -0.7+maxstep*0.1
        print("threaholder:")
        print(threaholder)
        p = precision_score(correct_labels_dev, predictions_dev[maxstep], average='binary')
        r = recall_score(correct_labels_dev, predictions_dev[maxstep], average='binary')
        print("recall_test:" + str(r))
        print("precision_test:" + str(p))
        print("f1score_test:" + str(maxf1value))
        ff.close()
    # start test
    print("\nstarttest:" + name)
    test_list = ['argouml_test', 'gwt_test', 'jaxen_test', 'jruby_test', 'xstream_test', 'totaltest']
    for name in test_list:
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
            threaholder = -0.7+maxstep*0.1
            if output[0] >= threaholder:
                predictions_test.append(1)
            else:
                predictions_test.append(-1)
        print("threaholder:")
        print(threaholder)
        cm = confusion_matrix(correct_labels_test, predictions_test)
        tn, fp, fn, tp = cm.ravel()
        p = precision_score(correct_labels_test, predictions_test, average='binary')
        r = recall_score(correct_labels_test, predictions_test, average='binary')
        f1score = f1_score(correct_labels_test, predictions_test, average='binary')
        print("recall_test:" + str(r))
        print("precision_test:" + str(p))
        print("f1score_test:" + str(f1score))
        print("tp:" + str(tp) + " tn:" + str(tn) + " fp:" + str(fp) + " fn:" + str(fn))
        ff.close()


if __name__ == '__main__':
    dictt = {}
    dictta = {}
    listta = list()

    def _onehot(i, total):
        return [1.0 if j == i else 0.0 for j in range(total)]
    feature_size = 100
    listchar = ['ExpressionStmt', 'ContinueStmt', 'ClassOrInterfaceType', 'MarkerAnnotationExpr', 'ThrowStmt',
                'SuperExpr', 'MethodDeclaration', 'ThisExpr', 'ArrayCreationExpr', 'ConditionalExpr',
                'StringLiteralExpr', 'WhileStmt', 'CatchClause', 'BinaryExpr', 'ObjectCreationExpr',
                'ReturnStmt', 'EnclosedExpr', 'BlockStmt', 'NameExpr', 'DoubleLiteralExpr',
                'AnnotationDeclaration', 'AssertStmt', 'TypeParameter', 'VariableDeclaratorId', 'ClassExpr',
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
        listta.append(np.random.normal(0, 0.1, 100).astype(np.float32))
    embeddingg = np.asarray(listta)
    embeddingg = tf.Variable(embeddingg)
    for i in range(len(listchar)):
        dictta[listchar[i]] = i
    train_model(dictta)