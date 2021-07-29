import argparse
import os
import hashlib
import sys

BUF_SIZE = 65536  # lets read stuff in 64kb !
i = 0  # siralama icin gerekli


# gelen her dosyanin iceriğine göre hash degeri gönderiyor
def find_hash(file):
    md5 = hashlib.md5()
    with open(file, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def print_with_hash(byte, dictionary):
    global i  # i'nin her defasında sifilanmamasi icin global etiketi ekledim
    print(f"{byte} bytes")
    for hash_, lst in dictionary.items():
        if len(lst) > 1:
            print(f"Hash: {hash_}")
            for j in lst:
                print(f"{i + 1}. {j}")
                i += 1


def get_hash_dict(dictionary, dup_state, sort):
    if dup_state == "yes":
        sortie = sorted(dictionary.keys(), reverse=sort[0])
        for byte in sortie:
            lst = dictionary.get(byte)
            dict_4 = {}
            for dsy in lst:
                hash_ = find_hash(dsy)
                if hash_ in dict_4.keys():
                    file_list = dict_4.get(hash_)
                    file_list.append(dsy)
                    dict_4.update({hash_: file_list})
                else:
                    dict_4.update({hash_: [dsy]})
            print_with_hash(byte, dict_4)
    elif dup_state == "no":
        sys.exit()


def check_for_dup():
    print("Check for duplicates?")
    dup = input()
    while True:
        if dup == "yes" or dup == "no":
            return dup
        else:
            print("Wrong option")
            continue


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

    dict_2 = {}
    for ke, value in dict_1.items():
        if ke in dict_2.keys():
            file_list2 = dict_2.get(ke)
            file_list2.append(v for v in value)
            dict_2.update({ke: file_list2})
        else:
            dict_2.update({ke: value})

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


def print_return_dir(file_format, sorting, direction):
    if len(file_format) == 0:
        return not_file_f(sorting, direction)

    else:
        return with_file_f(file_format, direction)


def user_info(path=None):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?")
    args = parser.parse_args()
    directory_ = args.directory

    file_format_, sorting_num_ = user_info(directory_)
    dict_ = print_return_dir(file_format=file_format_, sorting=sorting_num_, direction=directory_)
    get_hash_dict(dict_, check_for_dup(), sorting_num_)
