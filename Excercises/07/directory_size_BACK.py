def generate_filetree():
    filetree = {"/": {}}
    parent_dir = []
    current_dir = filetree["/"]
    with open("input.txt") as file:
        for line in file:
            if line.startswith("$ cd .."):
                current_dir = parent_dir.pop()
            elif line.startswith("$ cd /"):
                pass
            elif line.startswith("$ cd"):
                parent_dir.append(current_dir)
                current_dir = current_dir[line.split()[-1]]
            elif line.startswith("$ ls"):
                continue
            elif line.startswith("dir"):
                current_dir[line.split()[-1]] = {}
            else:
                current_dir[line.split()[-1]] = int(line.split()[0])
    return filetree


def calc_dir_size(current_dir_name, current_dir, small_dir_list):
    total_size = 0
    for name, dir_or_size in current_dir.items():
        if type(dir_or_size) == dict:
            total_size += calc_dir_size(name, dir_or_size, small_dir_list)
        else:
            total_size += dir_or_size
    if "size" not in current_dir.keys():
        current_dir["size"] = total_size
    if total_size <= 100000:
        small_dir_list.append((current_dir_name, total_size))
    return total_size


def calc_total_size(small_dir_list):
    total_size = 0
    for name, size in small_dir_list:
        total_size += size
    return total_size


def find_del_dir(dir, big_folder_list, threshold):
    for name, dir_or_size in dir.items():
        if type(dir_or_size) == dict:
            if dir_or_size["size"] >= threshold:
                big_folder_list.append(dir_or_size["size"])
            find_del_dir(dir_or_size, big_folder_list, threshold)


def main():
    filetree = generate_filetree()
    small_dir_list = []
    total_bytes_stored = calc_dir_size("/", filetree["/"], small_dir_list)
    total_of_small_dirs = calc_total_size(small_dir_list)
    print(total_of_small_dirs)
    big_folder_list = []
    threshold = 30_000_000 - (70_000_000 - total_bytes_stored)
    find_del_dir(filetree["/"], big_folder_list, threshold)
    print(min(big_folder_list))



if __name__ == "__main__":
    main()
