from __future__ import division
import re
import math
import os


def read_node(filename):
#    node_file_name = "beijing_osm_nodes.txt"
    node_file_name = filename
    node_file = open(node_file_name, "r")
    nodes_info = node_file.readlines()
    node_list = []
    nodes_lat = []
    nodes_lon = []
    for node_string in nodes_info:
        node = node_string.split("\t")
        node_id = long(node[0])
        node_lat = long(node[1])
        node_lon = long(node[2])
        node_list.append(node_id)
        nodes_lat.append(node_lat)
        nodes_lon.append(node_lon)
    returntuple = (node_list, nodes_lat, nodes_lon)
    return returntuple

def y2lat(a):
    l = a/6378137
    m = math.exp(l)
    t = math.atan(m)
    return 180.0/math.pi*(2.0*t-math.pi/2.0)

def lat2y(a):
    return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))

def x2lon(a):
    return a/(math.pi/180)/6378137

def lon2x(a):
    return a*(math.pi/180)*6378137

# nodes_flow = [0 for x in range(len(nodes_list))]
def node_count_for(file):
#    "traj_add_changed_000500.txt"
    file_open_traj = file
    traj_open = open(file_open_traj, "r")
    node_tuple = read_node("beijing_osm_nodes.txt")
    nodes_list = node_tuple[0]
    nodeslat = node_tuple[1]
    nodeslon = node_tuple[2]
    nodes_count = [0 for i in range(len(nodes_list))]
    traj_lines = traj_open.readlines()
    start_node = 0
    end_node = 0
    count_day = 0
    for traj in traj_lines:
        if traj == "\n":
#            print "skip"
            continue
        elif traj[0] != "[":
#            print traj[0:5]
            if traj[0:6] == "201111":
                file_write_txt = "traj_" + file[-10:-4] + "_for_" + str(count_day) + ".txt"
                print file_write_txt
                filecount = open(file_write_txt, "w")
                for i in range(len(nodes_count)):
    #                print str(nodes_list[i]) + "\t" + str(y2lat(nodeslat[i]/100))\
    #                + "\t" + str(x2lon(nodeslon[i]/100)) + "\t" + str(nodes_count[i])
                    filecount.writelines(str(nodes_list[i]) + "\t" + str(y2lat(nodeslat[i]/100))\
                                         + "\t" + str(x2lon(nodeslon[i]/100)) + "\t" + str(nodes_count[i]))
                    filecount.write("\n")
                nodes_list = node_tuple[0]
                nodes_count = [0 for i in range(len(nodes_list))]
                filecount.close()
                count_day += 1
                print "day_switching"
                continue
            else:
#                print "not a trajectory"
                continue
        else:
            traj_s = re.sub(r'[\[\] ]', '', traj)
            traj_list_s = traj_s.split(",")
            traj_list = [long(i) for i in traj_list_s]
            if len(traj_list) == 1:
                if traj_list[0] != start_node:
                    node_pos = nodes_list.index(traj_list[0])
                    nodes_count[node_pos] += 1
                    start_node = traj_list[0]
                    end_node = traj_list[0]
                    continue
                else:
                    continue
            if traj_list[0] == start_node and traj_list[1] == end_node:
                continue
            for traj_node in traj_list:
                try:
                    node_pos = nodes_list.index(traj_node)
                except:
                    continue
                nodes_count[node_pos] += 1
            start_node = traj_list[0]
            end_node = traj_list[-1]
    file_write_txt = "traj_" + file[-10:-4] + "_for_" + str(count_day) + ".txt"
    print file_write_txt
    filecount = open(file_write_txt, "w")
    for i in range(len(nodes_count)):
    #                print str(nodes_list[i]) + "\t" + str(y2lat(nodeslat[i]/100))\
    #                + "\t" + str(x2lon(nodeslon[i]/100)) + "\t" + str(nodes_count[i])
        filecount.writelines(str(nodes_list[i]) + "\t" + str(y2lat(nodeslat[i]/100))\
                                         + "\t" + str(x2lon(nodeslon[i]/100)) + "\t" + str(nodes_count[i]))
        filecount.write("\n")
    filecount.close()
    return 0


path_cur = ".\\traj_add"
file_list = os.listdir(path_cur)
for file in file_list:
#    print path_cur + "\\" + file
    node_count_for(path_cur + "\\" + file)

__author__ = 'John'
