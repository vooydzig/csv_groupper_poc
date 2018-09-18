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
    header, data = read_csv_file('sample/big.csv', GROUPPING)
    print(len(list(group_by(data, header, GROUPPING))))
    get_mem_usage('main end')


def group_by(data, headers, keys):
    get_mem_usage('group_by')
    record = {}
    for r in data:
        base = get_base_dict(r, headers, keys)
        if not record:
            record.update(base)
            record['items'] = [get_complementary_sub_dict(r, headers, keys)]
        else:
            if base == get_sub_dict(record, keys):
                record['items'].append(get_complementary_sub_dict(r, headers, keys))
            else:
                get_mem_usage('yield')
                yield record
                record = {}
                record.update(base)
                record['items'] = [get_complementary_sub_dict(r, headers, keys)]


def get_base_dict(data, headers, keys):
    return {k: data[headers.index(k)] for k in keys}


def get_sub_dict(data, keys):
    return {k: data[k] for k in keys}


def get_complementary_sub_dict(data, headers, keys):
    return {headers[i]: data[i] for i in range(len(headers)) if not headers[i] in keys}


def read_csv_file(path, keys):
    get_mem_usage('open file')
    with open(path) as f:
        reader = csv.reader(f, delimiter=';')
        headers = next(reader)
        get_mem_usage('end reader')
        return headers, [r for r in sorted(reader, key=itemgetter(*[headers.index(k) for k in keys]))]


if __name__ == '__main__':
    main()
