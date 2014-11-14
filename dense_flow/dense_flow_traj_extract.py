import os
import re
path = os.curdir
dir_list = os.listdir(path)
data_file_list = []
for filename in dir_list:
    if filename[0:7] == "changed":
        data_file_list.append(filename)

for file_cur in data_file_list:
    print "filechanged!!"
    file_dir = path + "\\" + file_cur
    data_file = open(file_dir, "r")
    write_traj_file_name = path + "\\dense_traj_" + file_cur
    traj_file = open(write_traj_file_name, "w")
    content = data_file.readlines()
    count = 0
    traj_tmp = []
    number_count = 0
    for dataline in content:
        dataline_re = re.sub("[\n]", "", dataline)
        dataline_list = dataline.split("\t")
        if len(dataline_list) == 1:
            if count > 20:
                number_count += 1
                print count
#                print traj_tmp
                traj_file.writelines(str(count))
                traj_file.writelines("\n")
                traj_file.writelines(traj_tmp)
                traj_file.writelines("\n")
            count = 0
            traj_tmp = []
            continue
        else:
            count += 1
            traj_tmp.append(dataline)
    traj_file.writelines(str(number_count))


__author__ = 'John'
