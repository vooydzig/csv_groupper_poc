import csv_dict
import csv_list

# input data: https://datasource.kapsarc.org/explore/dataset/national-accounts-main-aggregates-database-1970-2014/table/?disjunctive.freq&disjunctive.location&disjunctive.variable

GROUPPING = ['Year', 'FREQ']

dict_data = csv_dict.read_csv_file('sample/big.csv', GROUPPING)
header, list_data = csv_list.read_csv_file('sample/big.csv', GROUPPING)

print(list(csv_list.group_by(list_data, header, GROUPPING)) == list(csv_dict.group_by(dict_data, GROUPPING)))
