import argparse
import os
# import sys


def hold_check_info(path=None):
    if path is None:
        print("Directory is not specified")

    file_f = input("Enter file format:")

    print("size sorting options:\n1. Descending\n2. Ascending")
    while True:
        sorting = int(input("Enter a sorting option:"))
        if sorting == 1 or sorting == 2:
            break
        else:
            print("Wrong option")
            continue
    sorting = [True if sorting == 1 else False]
    return file_f, sorting


def not_file_f(sorting, direction):
    dict_1 = {}
    for root, dirs, names in os.walk(direction):
        for nam in names:
            path = os.path.join(root, nam)
            size = os.path.getsize(path)

            if size in dict_1.keys():
                file_list = dict_1.get(size)
                file_list.append(path)
                dict_1.update({size: file_list})
            else:
                dict_1.update({size: [path]})

    dict_2 = {}  # farklı pathlardaki aynı boyutlu dosyaları, patha göre değil de boyutlara göre sıralamak amacıyla dict_1 üzerinden dict_2 oluşturuldu
    for key, value in dict_1.items():
        if key in dict_2.keys():
            file_list2 = dict_2.get(key)
            file_list2.append(v for v in value)
            dict_2.update({key: file_list2})
        else:
            dict_2.update({key: value})

    sorted_keys = sorted(dict_2.keys(), reverse=sorting[0])
    for key in sorted_keys:
        print(key, " bytes")
        val = dict_1.get(key)
        for va in val:
            print(va)

    return dict_2


def with_file_f(file_format, direction):
    dict_3 = {}
    for root, dirs, names in os.walk(direction):
        for name in names:
            if name.endswith(file_format):
                path = os.path.join(root, name)
                size = os.path.getsize(path)

                if size in dict_3.keys():
                    file_list = dict_3.get(size)
                    file_list.append(path)
                    dict_3.update({size: file_list})
                else:
                    dict_3.update({size: [path]})

    for size in dict_3.keys():
        path = dict_3.get(size)
        if len(path) > 1:
            print(size, " bytes")
            for i in path:
                print(i)
    return dict_3


def print_hold_dir(file_format, sorting, direction):
    if len(file_format) == 0:
        return not_file_f(sorting, direction)

    else:
        return with_file_f(file_format, direction)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?")
    args = parser.parse_args()
    directory_ = args.directory

    file_format_, sorting_num_ = hold_check_info(directory_)
    dict_ = print_hold_dir(file_format=file_format_, sorting=sorting_num_, direction=directory_)

