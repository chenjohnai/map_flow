import os

file_path = "g:\\car2.0\\"
folder_list = os.listdir(file_path)
for folder in folder_list:
    cur_folder = file_path + folder + "\\"
    file_list = os.listdir(cur_folder)
    filenumber = len(file_list)
    print file_list[filenumber - 1]
    for i in range(0,filenumber - 1):
        file = file_list[i]
        file_read_name = cur_folder + file
        file_write_name = cur_folder + "changed_" + file
        file_write = open(file_write_name,"w")
        file_read = open(file_read_name)
        traj_string = file_read.readlines()
        if len(traj_string) == 0: continue
        file_write.writelines(traj_string[0].split('\t')[0])
        file_write.writelines("\n")
        for i in range(0,len(traj_string) - 1):
            traj_list = traj_string[i].split("\t")
            traj_list_next = traj_string[i + 1].split("\t")
            file_write.writelines(traj_string[i])

            if(traj_list[0] != traj_list_next[0]):
                file_write.writelines(traj_list_next[0])  
                file_write.write("\n")
        file_write.writelines(traj_string[-1])
        file_write.close()
        print folder + "   " + file
'''
Created on Aug 11, 2014

@author: chen
'''
