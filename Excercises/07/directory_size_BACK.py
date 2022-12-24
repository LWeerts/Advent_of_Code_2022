def main():
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
                current_dir = current_dir[line.split[-1]]
            elif line.startswith("$ ls"):
                continue
            elif line.startswith("dir"):
                current_dir[line.split[-1]] = {}
            else: 
                current_dir[line.split[-1]] = int(line.split[0])

# bla 
if __name__ == "__main__":
    main()
