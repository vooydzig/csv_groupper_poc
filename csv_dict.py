import csv
import os
from operator import itemgetter

import psutil


def get_mem_usage(label=''):
    process = psutil.Process(os.getpid())
    b = process.memory_info().rss
    mb = b // (1024 * 1024)
    print(f'{label} - {b}  ({mb} MB)')

GROUPPING = ['Year', 'FREQ']

def main():
    get_mem_usage('main start')
    data = read_csv_file('sample/big.csv', GROUPPING)
    print(len(list(group_by(data, GROUPPING))))
    get_mem_usage('main end')


def group_by(data, keys):
    get_mem_usage('group_by')
    record = {}
    for r in data:
        base = get_sub_dict(r, keys)
        if not record:
            record.update(base)
            record['items'] = [get_complementary_sub_dict(r, keys)]
        else:
            if base == get_sub_dict(record, keys):
                record['items'].append(get_complementary_sub_dict(r, keys))
            else:
                get_mem_usage('yield')
                yield record
                record = {}
                record.update(base)
                record['items'] = [get_complementary_sub_dict(r, keys)]


def get_sub_dict(data, keys):
    return {k: data[k] for k in keys}

def get_complementary_sub_dict(data, keys):
    return {k: data[k] for k in data if k not in keys}


def read_csv_file(path, keys):
    get_mem_usage('open file')
    with open(path) as f:
        reader = csv.DictReader(f, delimiter=';')
        get_mem_usage('end reader')
        return [r for r in sorted(reader, key=itemgetter(*keys))]


if __name__ == '__main__':
    main()
