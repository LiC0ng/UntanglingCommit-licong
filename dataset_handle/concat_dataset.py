from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--source_dir", dest="source_dir", required=True)
    parser.add_argument("--dest_dir", dest="dest_dir", required=True)
    args = parser.parse_args()
    # get stream of write files
    total_untangled = args.dest_dir + '/untangled.txt'
    total_tangled = args.dest_dir + '/tangled.txt'
    total_dataset = args.dest_dir + '/dataset.txt'
    total_untangled_file = open(total_untangled, 'a')
    total_tangled_file = open(total_tangled, 'a')
    total_dataset_file = open(total_dataset, 'a')
    # get stream of write files
    source_untangled = args.source_dir + '/untangled.txt'
    source_tangled = args.source_dir + '/tangled.txt'
    source_untangled_file = open(source_untangled, 'r')
    source_tangled_file = open(source_tangled, 'r')
    source_untangled_data = source_untangled_file.read()
    source_tangled_data = source_tangled_file.read()
    # write datas
    total_untangled_file.write(source_untangled_data)
    total_tangled_file.write(source_tangled_data)
    total_dataset_file.write(source_untangled_data)
    total_dataset_file.write(source_tangled_data)
    # close stream
    total_tangled_file.close()
    total_tangled_file.close()
    total_dataset_file.close()
    source_tangled_file.close()
    source_untangled_file.close()
