import numpy as np


def read_forest():
    forest = np.genfromtxt("Excercises/08/input.txt", delimiter=1, dtype="uint8")
    return forest


def is_tree_visible(forest, coord_x, coord_y):
    # treeline without the tree we care about
    treelines = (np.flip(forest[: coord_x, coord_y]),
                 forest[coord_x + 1:, coord_y],
                 np.flip(forest[coord_x, : coord_y]),
                 forest[coord_x, coord_y + 1:]
                 )
    score = calc_scenic_score(treelines, forest[coord_x, coord_y])
    for treeline in treelines:
        if 0 in treeline.shape or forest[coord_x, coord_y] > np.max(treeline):
            return True, score
    return False, score


def calc_scenic_score(treelines, treehouse):
    score = 1
    for row in treelines:
        if len(row) == 0:
            return 0
        for count, tree in enumerate(row, start=1):
            if tree >= treehouse:
                score *= count
                break
        else:
            score *= count
    return score


def main():
    trees_visible = 0
    highest_score = 0
    forest = read_forest()
    len_x, len_y = forest.shape
    for coord_x in range(len_x):
        for coord_y in range(len_y):
            tree_vis, scenic_score = is_tree_visible(forest, coord_x, coord_y)
            if tree_vis:
                trees_visible += 1
            if scenic_score > highest_score:
                highest_score = scenic_score
    print(trees_visible)
    print(highest_score)


if __name__ == "__main__":
    main()
