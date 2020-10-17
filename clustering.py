# modified on sanada's code

from argparse import ArgumentParser
import itertools


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


def print_result(cell_map, composed_list):
    clusters = cell_map.keys()
    #print('CLUSTER NUM: {}'.format(len(clusters)))

    sample = None
    correct_num = 0
    all_num = 0
    for i, cluster_id in enumerate(clusters):
        #print_chunk_id(cluster_id, composed_list)
        chunks = collect_chunks(cluster_id, composed_list)
        if i == 0:
            sample = chunks[0].split('_')[0]
            corrects = [c for c in chunks if c.split('_')[0] == sample]
        elif i == 1:
            corrects = [c for c in chunks if c.split('_')[0] != sample]
        correct_num += len(corrects)
        all_num += len(chunks)

        # print('======================')

    if all_num // correct_num >= 2:
        correct_num = all_num - correct_num
    # print('ACCURACY {}/{}={}'.format(correct_num, all_num, correct_num / all_num))
    print('{}'.format(correct_num / all_num))


def collect_chunks(cluster_id, composed_list):
    chunks = []
    if '_' in cluster_id:
        return [cluster_id]
    else:
        chunk_id1, chunk_id2 = composed_list[int(cluster_id)]
        return collect_chunks(chunk_id1, composed_list) + collect_chunks(chunk_id2, composed_list)


def execute_clustering(input_file):
    cell_map = {}
    for line in input_file:
        strs = line.split('\t')
        answer = strs[0]
        pair = strs[1], strs[2]
        value = strs[3].replace('[', '')
        value = value.replace(']', '')
        value = value.replace('\n', '')
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
    while True:
        # print_cell_map(cell_map)
        max_cell = {'value': 0}
        for row in cell_map.values():
            for cell in row.values():
                if max_cell['value'] < cell['value']:
                    max_cell = cell

        if len(cell_map.keys()) <= 2:
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
            strong_cell = removed_cell1 if removed_cell1['value'] > removed_cell2['value'] else removed_cell2
            new_cell = {
                'pair': (chunk_id, new_chunk_id),
                'value': strong_cell['value']
            }
            row[new_chunk_id] = new_cell
            new_row[chunk_id] = new_cell

        cell_map[new_chunk_id] = new_row

    print_result(cell_map, composed_list)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', dest='input_path', required=True)
    args = parser.parse_args()

    with open(args.input_path, 'r') as input_file:
        execute_clustering(input_file)
