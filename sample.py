import collections

lst=[99.0,98.0,99.0,98.0]


data = collections.Counter(lst)
data_list = dict(data)
max_value = max(list(data.values()))
mode_val = [num for num, freq in data_list.items() if freq == max_value]
mode = ', '.join(map(str, mode_val))

print("%s"%mode)
