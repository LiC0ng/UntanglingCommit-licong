import itertools
import os

MAX = 0

def print_cell_map(cell_map):
    for row_id, (key, row) in enumerate(cell_map.items()):
        text = '{:>15}: '.format(key[-15:])
        for column_id, cell in enumerate(row.values()):
            if row_id == column_id:
                text += '*****  '
            text += '{:>5.3f}  '.format(cell['value'])
        print(text)
    print('---------------------------')

def print_chunk_id(cluster_id, composed_list, depth=0):
    if '_' in cluster_id:
        strs = cluster_id.split('_')
        print('-' * depth + ' {}: {}'.format(strs[0][:6], strs[1].split('/')[-1]))
    else:
        chunk_id1, chunk_id2 = composed_list[int(cluster_id)]
        print('-' * depth + ' |')
        print_chunk_id(chunk_id1, composed_list, depth + 1)
        print_chunk_id(chunk_id2, composed_list, depth + 1)


def print_result(correct_cluster, cell_map, composed_list):
    clusters = cell_map.keys()
    # print('CLUSTER NUM: {}'.format(len(clusters)))

    correct_map = []
    for _ in correct_cluster:
        correct_map.append([])
    all_num = 0
    for _, cluster_id in enumerate(clusters):
        # print_chunk_id(cluster_id, composed_list)
        chunks = collect_chunks(cluster_id, composed_list)
        for i, cluster in enumerate(correct_cluster):
            correct_map[i].append(len([c for c in chunks if c.split('_')[0] == cluster]))
        all_num += len(chunks)

        # print('======================')
    f1 = [False for i in range(len(correct_cluster))]
    f2 = [False for i in range(len(clusters))]
    global MAX
    MAX = 0
    dfs(f1, f2, correct_map, 0)
    # print('ACCURACY {}/{}={}'.format(correct_num, all_num, correct_num / all_num))
    return (MAX / all_num)


def dfs(f1, f2, correct_map, correct_num):
    for i, flag1 in enumerate(f1):
        if flag1 is True:
            continue
        f1[i] = True
        for j, flag2 in enumerate(f2):
            if flag2 is True:
                continue
            f2[j] = True
            dfs(f1, f2, correct_map, correct_num + correct_map[i][j])
            f2[j] = False
        f1[i] = False
    global MAX
    if correct_num > MAX:
        MAX = correct_num



def collect_chunks(cluster_id, composed_list):
    chunks = []
    if '_' in cluster_id:
        return [cluster_id]
    else:
        chunk_id1, chunk_id2 = composed_list[int(cluster_id)]
        return collect_chunks(chunk_id1, composed_list) + collect_chunks(chunk_id2, composed_list)

def execute_clustering(input_file, th):
    cell_map = {}
    correct_cluster = set()
    for line in input_file:
        strs = line.split(',')
        answer = strs[0]
        pair = strs[1], strs[2]
        correct_cluster.add(strs[0].split('_')[0])
        correct_cluster.add(strs[1].split('_')[0])
        value = strs[3]
        cell_data = {
            'pair': pair,
            'answer': int(answer),
            'value': float(value)
        }

        if pair[0] in cell_map:
            cell_map[pair[0]][pair[1]] = cell_data
        else:
            cell_map[pair[0]] = {pair[1]: cell_data}
        if pair[1] in cell_map:
            cell_map[pair[1]][pair[0]] = cell_data
        else:
            cell_map[pair[1]] = {pair[0]: cell_data}

    composed_list = []
    threshold = th
    while True:
        #print_cell_map(cell_map)
        flag = False
        max_cell = {'value':0}
        for row in cell_map.values():
            for cell in row.values():
                if max_cell['value'] < cell['value'] and cell['value'] >= threshold:
                    max_cell = cell
                    flag = True

        if flag is False:
            break

        max_pair = max_cell['pair']
        cell_map.pop(max_pair[0])
        cell_map.pop(max_pair[1])
        composed_list.append(max_pair)
        new_chunk_id = str(len(composed_list) - 1)
        new_row = {}

        for chunk_id, row in cell_map.items():
            removed_cell1 = row.pop(max_pair[0])
            removed_cell2 = row.pop(max_pair[1])
            strong_cell = removed_cell1 if abs(removed_cell1['value'] - 0.5) < abs(removed_cell2['value'] - 0.5) else removed_cell2
            new_cell = {
                'pair': (chunk_id, new_chunk_id),
                'value': (removed_cell1['value'] + removed_cell2['value']) / 2
            }
            row[new_chunk_id] = new_cell
            new_row[chunk_id] = new_cell

        cell_map[new_chunk_id] = new_row

    return print_result(correct_cluster, cell_map, composed_list)

if __name__ == '__main__':

    projects = os.listdir('clustering')
    output_file = open("output.csv", 'a')

    th = 0.4551
    while th <= 0.51:
        result_list = []

        for project in projects:
            file_list = os.listdir('clustering/' + project)
            for file in file_list:
                input_path = 'clustering/' + project + '/' + file
                with open(input_path, 'r') as input_file:
                    result_list.append(execute_clustering(input_file, th))

        SUM = 0
        for result in result_list:
            SUM += result
        AVG = SUM / len(result_list)
        output_file.writelines(str(th) + ',' + str(AVG) + '\n')
        th += 0.001

