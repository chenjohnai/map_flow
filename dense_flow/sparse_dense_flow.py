import sys


def sparse_dense_traj(filename):
#    filename = "dense_traj_test.txt"
    dense_traj = open(filename, "r")
    sparse_filename = "sparse_traj_" + filename[-10:]
    sparse_traj_file = open(sparse_filename, "w")
    sparsing = 0
    for denseline in dense_traj:
        if denseline == "\n":
            continue
        traj_list = denseline.split("\t")
        if len(traj_list) == 1:
            sparsing = 0
            continue
        if sparsing % 5 == 0:
            if sparsing == 0:
                sparse_traj_file.writelines(traj_list[0])
                sparse_traj_file.writelines("\n")
            traj_writeline = denseline
            sparse_traj_file.writelines(traj_writeline)
        sparsing += 1

if __name__ == "__main__":
    filename = "dense_traj_changed_110500.txt"
    sparse_dense_traj(filename)


__author__ = 'John'
