from argparse import ArgumentParser
import pickle


def _load_vocab_from_histogram(path, min_count=0, start_from=0, return_counts=False):
    with open(path, 'r') as file:
        word_to_index = {}
        index_to_word = {}
        word_to_count = {}
        next_index = start_from
        for line in file:
            line_values = line.rstrip().split(' ')
            if len(line_values) != 2:
                continue
            word = line_values[0]
            count = int(line_values[1])
            if count < min_count:
                continue
            if word in word_to_index:
                continue
            word_to_index[word] = next_index
            index_to_word[next_index] = word
            word_to_count[word] = count
            next_index += 1
    result = word_to_index, index_to_word, next_index - start_from
    if return_counts:
        result = (*result, word_to_count)
    return result

def load_vocab_from_histogram(path, min_count=0, start_from=0, max_size=None, return_counts=False):
    if max_size is not None:
        word_to_index, index_to_word, next_index, word_to_count = \
            _load_vocab_from_histogram(path, min_count, start_from, return_counts=True)
        if next_index <= max_size:
            results = (word_to_index, index_to_word, next_index)
            if return_counts:
                results = (*results, word_to_count)
            return results
        # Take min_count to be one plus the count of the max_size'th word
        min_count = sorted(word_to_count.values(), reverse=True)[max_size] + 1
    return _load_vocab_from_histogram(path, min_count, start_from, return_counts)


def save_dictionaries(dataset_name, word_to_count):
    save_dict_file_path = '{}/dict.c2v'.format(dataset_name)
    with open(save_dict_file_path, 'wb') as file:
        pickle.dump(word_to_count, file)
        print('Dictionaries saved to: {}'.format(save_dict_file_path))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-wvs", "--word_vocab_size", dest="word_vocab_size", default=1301136,
                        help="Max number of origin word in to keep in the vocabulary", required=False)
    parser.add_argument("-wh", "--word_histogram", dest="word_histogram",
                        help="word histogram file", metavar="FILE", required=True)
    parser.add_argument("-o", "--output_dir", dest="output_dir",
                        help="output name - the base name for the created dataset", metavar="FILE", required=True,
                        default='data')
    args = parser.parse_args()

    _, _, _, word_to_count = load_vocab_from_histogram(args.word_histogram, start_from=1,
                                                                  max_size=int(args.word_vocab_size),
                                                                  return_counts=True)

    save_dictionaries(dataset_name=args.output_dir, word_to_count=word_to_count)
