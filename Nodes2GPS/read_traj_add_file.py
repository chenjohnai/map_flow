import re
import node2gps

file_name = "../dense_flow/traj_add_sparse_traj_110500.txt"
filename_write = "node_gps_list_s110000.txt"
file = open(file_name, "r")
datalines = file.readlines()
file_write = open(filename_write, "w")

try:
    for line in datalines:
        if line == "\n":
            continue
        linestring = line.split("     ")
        if line[0:3] == "The":
            continue
        if len(linestring) == 1:
            lineraw = re.sub("[\[\]]","",line)
            linestring = lineraw.split(",")
            line_nodes = [long(i) for i in linestring]
            if len(line_nodes) == 1:
                file_write.writelines(str(linestring))
                file_write.writelines("\n")   
            else:                 
                for eachnode in line_nodes:
                    gps_point = node2gps.node_to_gps(eachnode)
                    file_write.writelines(str(gps_point[0]) + "\t" + str(gps_point[1]))
                    file_write.writelines("\n")

        elif len(linestring) == 2:
            continue

except:
    print line    
file_write.close()
    
    
'''
Created on Oct 10, 2014

@author: chen
'''
