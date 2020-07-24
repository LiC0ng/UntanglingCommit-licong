def _pad_nobatch(children):
    child_len = max([len(c) for n in children for c in n])
    children = [[c + [0] * (child_len - len(c)) for c in sample] for sample in children]
    return children


def replace_shared_node(node1, node2, embeddings):
    nodes11 = []
    nodes22 = []
    for i in range(len(node1)):
        if node1[i].find('NameExpr') < 0:
            continue
        for j in range(len(node2)):
            if node2[j].find('NameExpr') < 0:
                continue
            if node1[i] == node2[j]:
                node1[i] = 'NameExprShared'
                node2[j] = 'NameExprShared'

    for i in range(len(node1)):
        if node1[i].find('NameExpr') >= 0:
            if node1[i].find('NameExprShared') >= 0:
                nodes11.append(embeddings[node1[i]])
            else:
                node1[i] = 'NameExpr'
                nodes11.append(embeddings[node1[i]])
        else:
            nodes11.append(embeddings[node1[i]])

    for j in range(len(node2)):
        if node2[j].find('NameExpr') >= 0:
            if node2[j].find('NameExprShared') >= 0:
                nodes22.append(embeddings[node2[j]])
            else:
                node2[j] = 'NameExpr'
                nodes22.append(embeddings[node2[j]])
        else:
            nodes22.append(embeddings[node2[j]])
    return nodes11, nodes22


def getData_nofinetune(l, dictt, embeddings):
    nodes11 = []
    children11 = []
    nodes22 = []
    children22 = []
    label = l[2]
    queue1 = [(dictt[l[0]], -1)]
    while queue1:
        node1, parent_ind1 = queue1.pop(0)
        node_ind1 = len(nodes11)
        queue1.extend([(child, node_ind1) for child in node1['children']])
        children11.append([])
        if parent_ind1 > -1:
            children11[parent_ind1].append(node_ind1)
        nodes11.append(embeddings[node1['node']])
    queue2 = [(dictt[l[1]], -1)]
    while queue2:
        node2, parent_ind2 = queue2.pop(0)
        node_ind2 = len(nodes22)
        queue2.extend([(child, node_ind2) for child in node2['children']])
        children22.append([])
        if parent_ind2 > -1:
            children22[parent_ind2].append(node_ind2)
        nodes22.append(embeddings[node2['node']])
    children111 = []
    children222 = []
    children111.append(children11)
    children222.append(children22)
    children1 = _pad_nobatch(children111)
    children2 = _pad_nobatch(children222)
    return [nodes11], children1, [nodes22], children2, label


def getData_finetune(l, dictt, embeddings):
    nodes11 = []
    children11 = []
    nodes22 = []
    children22 = []
    label = l[2]
    queue1 = [(dictt[l[0]], -1)]
    while queue1:
        node1, parent_ind1 = queue1.pop(0)
        node_ind1 = len(nodes11)
        queue1.extend([(child, node_ind1) for child in node1['children']])
        children11.append([])
        if parent_ind1 > -1:
            children11[parent_ind1].append(node_ind1)
        nodes11.append(node1['node'])

    queue2 = [(dictt[l[1]], -1)]
    while queue2:
        node2, parent_ind2 = queue2.pop(0)
        node_ind2 = len(nodes22)
        queue2.extend([(child, node_ind2) for child in node2['children']])
        children22.append([])
        if parent_ind2 > -1:
            children22[parent_ind2].append(node_ind2)
        nodes22.append(node2['node'])

    nodes11, nodes22 = replace_shared_node(nodes11, nodes22, embeddings)

    children111 = []
    children222 = []
    batch_labels = []
    children111.append(children11)
    children222.append(children22)
    children1 = _pad_nobatch(children111)
    children2 = _pad_nobatch(children222)
    batch_labels.append(label)
    return nodes11, children1, nodes22, children2, batch_labels


def getData_notokenfinetune(l, dictt, embeddings):
    nodes11 = []
    children11 = []
    nodes22 = []
    children22 = []
    label = l[2]
    queue1 = [(dictt[l[0]], -1)]
    while queue1:
        node1, parent_ind1 = queue1.pop(0)
        node_ind1 = len(nodes11)
        queue1.extend([(child, node_ind1) for child in node1['children']])
        children11.append([])
        if parent_ind1 > -1:
            children11[parent_ind1].append(node_ind1)
        if node1['node'].find('NameExpr') >= 0:
            nodes11.append(embeddings['NameExpr'])
        else:
            nodes11.append(embeddings[node1['node']])

    queue2 = [(dictt[l[1]], -1)]
    while queue2:
        node2, parent_ind2 = queue2.pop(0)
        node_ind2 = len(nodes22)
        queue2.extend([(child, node_ind2) for child in node2['children']])
        children22.append([])
        if parent_ind2 > -1:
            children22[parent_ind2].append(node_ind2)
        if node2['node'].find('NameExpr') >= 0:
            nodes22.append(embeddings['NameExpr'])
        else:
            nodes22.append(embeddings[node2['node']])

    children111 = []
    children222 = []
    batch_labels = []
    children111.append(children11)
    children222.append(children22)
    children1 = _pad_nobatch(children111)
    children2 = _pad_nobatch(children222)
    batch_labels.append(label)
    return nodes11, children1, nodes22, children2, batch_labels


def getData_id_type(l, dictt, embeddings):
    nodes11 = []
    children11 = []
    nodes22 = []
    children22 = []
    label = l[2]
    queue1 = [(dictt[l[0]], -1)]
    while queue1:
        node1, parent_ind1 = queue1.pop(0)
        node_ind1 = len(nodes11)
        queue1.extend([(child, node_ind1) for child in node1['children']])
        children11.append([])
        if parent_ind1 > -1:
            children11[parent_ind1].append(node_ind1)
        if node1['node'].find('NameExpr') >= 0:
            nodes11.append(embeddings[node1['node'][9:]])
        else:
            nodes11.append(embeddings[node1['node']])

    queue2 = [(dictt[l[1]], -1)]
    while queue2:
        node2, parent_ind2 = queue2.pop(0)
        node_ind2 = len(nodes22)
        queue2.extend([(child, node_ind2) for child in node2['children']])
        children22.append([])
        if parent_ind2 > -1:
            children22[parent_ind2].append(node_ind2)
        if node2['node'].find('NameExpr') >= 0:
            nodes22.append(embeddings[node2['node'][9:]])
        else:
            nodes22.append(embeddings[node2['node']])

    children111 = []
    children222 = []
    batch_labels = []
    children111.append(children11)
    children222.append(children22)
    children1 = _pad_nobatch(children111)
    children2 = _pad_nobatch(children222)
    batch_labels.append(label)
    return nodes11, children1, nodes22, children2, batch_labels
