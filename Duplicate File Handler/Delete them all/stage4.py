import argparse
import os
import hashlib
import sys

BUF_SIZE = 65536  # lets read stuff in 64kb !
i = 1


def delete_file(answ, ls, num):
    ask_list = []  # gelen listeler içindeki kumeleri tek bir listede toplamak için
    num_ = []  # gelen dosya numaralarını kullanıcının girdiği numaralarla daha kolay karşılaştırmak için ayrıca alınıp tek bir listeye dahil edildi
    total_byte = 0
    if answ == "yes":
        for i in ls:
            for j in i:
                ask_list.append(j)

        for i in num:
            for j in i:
                num_.append(str(j))

        krl = True  # döngünün geçerli bir değer almasını sağlamak için
        while True:
            print("Enter file numbers to delete:")
            for_del = input()
            for_del_ = for_del.split()  # kullanıcıdan girilen boşluklu girdileri boşluktan arındırmak için kullanıldı
            if len(for_del) == 0:
                print("Wrong format")
                krl = False
            else:
                for i in for_del_:
                    if not(i in num_):
                        print("Wrong format")
                        krl = False
            if krl is True:  # krl değişmemiş ise geçerli bir değer girilmiş demektir
                break

        byte = []  # silinen dosyaların baytlarını biriktirip toplayacağız
        pat = []  # silinmesi gereken dosyaların pathlarını burada toplayacağız
        for i in for_del_:
            k = int(i)
            for j in ask_list:
                t = list(j.keys())  # list(j.keys()) şeklinde yazarak değere liste içinde ulaşıyoruz
                if k in t:          # yoksa dict_keys([1]) şeklinde değer dönüyor
                    dic = j.values()
                    for m in list(dic):
                        byte.append(list(m.keys()))
                        pat.append(list(m.values()))

        for i in pat:
            for j in i:
                os.remove(j)
        for i in byte:
            for j in i:
                total_byte += j
        print(f"Total freed up space: {total_byte} bytes")

    else:
        sys.exit()


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
    global i
    l = []
    n = []
    print(f"{byte} bytes")
    for hash_, lst in dictionary.items():
        if len(lst) > 1:
            print(f"Hash: {hash_}")
            for j in lst:
                print(f"{i}. {j}")
                l.append({i: {byte: j}})
                n.append(i)
                i += 1
    return l, n


def get_hash_dict(dictionary, dup_state, sort):
    if dup_state == "yes":
        for_deleting = []
        for_deleting_num = []
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
            l, n = print_with_hash(byte, dict_4)
            for_deleting.append(l)
            for_deleting_num.append(n)
        return for_deleting, for_deleting_num

    elif dup_state == "no":
        sys.exit()


def ask_delete_file():
    print("Delete files?")
    answ = input()
    while True:
        if answ == "yes" or answ == "no":
            return answ
        else:
            print("Wrong option")
            continue


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
    lfd, nfd = get_hash_dict(dict_, check_for_dup(), sorting_num_)  # list for deleting, num for deleting
    delete_file(ask_delete_file(), lfd, nfd)
