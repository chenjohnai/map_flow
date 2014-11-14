import re
import node2gps

file_name = "../dense_flow/dense_traj_changed_110500.txt"
filename_write = "node_gps_list_den_110500.txt"
file = open(file_name, "r")
datalines = file.readlines()
file_write = open(filename_write, "w")
start = 1
try:
    for i in range(len(datalines)):
        datalinestring = re.sub("\[\]","",datalines[i])
        if datalinestring == "\n":
            continue
        dataline_list = datalinestring.split("\t")
        if len(dataline_list) == 1:
            start = 0
    
        else:
            if start == 0:
                carID = dataline_list[0]
                file_write.writelines("\n")
                file_write.writelines(str(carID))
                file_write.write("\n")
                start = 1
            print i
            print dataline_list
            GPSID = long(dataline_list[4])
    
            gps_point = node2gps.node_to_gps(GPSID)
            file_write.writelines(str(gps_point[0]) + "\t" + str(gps_point[1]))
            file_write.writelines("\n")        
            
            GPSID2 = long(dataline_list[4])
            gps_point2 = node2gps.node_to_gps(GPSID2)
            file_write.writelines(str(gps_point2[0]) + "\t" + str(gps_point2[1]))
            file_write.writelines("\n")
except:
    print "somgthing wrong"
    file_write.close()        
        
'''
Created on Oct 10, 2014

@author: chen
'''
