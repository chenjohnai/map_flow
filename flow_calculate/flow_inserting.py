# this file is used for adding nodes from start node to end node.
# this file will find the 
import psycopg2
import os
import thread
from time import sleep

def find_node_pos(node_id):
    node_ret = {}
    node_query = "SELECT lat, lon FROM public.planet_osm_nodes WHERE planet_osm_nodes.id = %d;"
    osm_cursor.execute(node_query% int(node_id))
    node_lat_lon_pair = osm_cursor.fetchall()[0]
    node_ret[str(node_id)] = node_lat_lon_pair
    return node_ret
            

def find_next_ways(way, end_node, end_node_ways):
    way_query = "SELECT ways_index.ways_index FROM public.ways_index WHERE id = %d"
    way_find = []
    node_to_find = []
    way_list = []
    node_cursor.execute(way_query% way[0])
    linkingways = node_cursor.fetchall()[0][0]
    linkingways = linkingways.replace("[","")
    linkingways = linkingways.replace("]","")
    linkingways = linkingways.replace("L","")
    way_list = linkingways.split(",")
    for i in range(0,len(way_list)):
        way_list[i] = long(way_list[i])
    node_far = []
    end_node_dic = find_node_pos(end_node)
    for way in way_list:
        node_id_query = "SELECT planet_osm_ways.nodes FROM public.planet_osm_ways WHERE id = %d"
#        print node_id_query% long(way)
        osm_cursor.execute(node_id_query% long(way))
        way_connect = list(osm_cursor.fetchall()[0])[0]
        node_far.append(way_connect[0])
        node_far.append(way_connect[-1])

    node1 = find_node_pos(node_far[0])
    dist = distance(node1, end_node_dic, node_far[0], int(end_node))
    optimal_node_dist = dist
    optimal_node_id = node_far[0]
    
    for node in node_far:
        node_dic = find_node_pos(node)
        dist = distance(node_dic, end_node_dic, node, int(end_node))
        if optimal_node_dist > dist:
            optimal_node_dist = dist
            optimal_node_id = node
    
    optimal_way_query = "SELECT node_index.index_road FROM public.node_index WHERE node_id = %d"
    node_cursor.execute(optimal_way_query% int(optimal_node_id))
    temp_way = node_cursor.fetchall()[0][0]
    temp_way = temp_way.replace("[","")
    temp_way = temp_way.replace("]","")
    temp_way = temp_way.replace("L","")
    temp_way = temp_way.split(",")
    for temp in temp_way:
        if long(temp) in way_list:
            break

    return (long(temp), way_list)


def distance(node_dic1, node_dic2, dic1, dic2):
    pos_1 = list(node_dic1[str(dic1)])
    pos_2 = list(node_dic2[str(dic2)])
    dist = (pos_1[0] - pos_2[0]) * (pos_1[0] - pos_2[0]) + (pos_1[1] - pos_2[1]) * (pos_1[1] - pos_2[1])
    return dist
    
    

def file_manipulate(path_cur, csv_file):
            file_write = path_cur + "traj_add_" + csv_file
            file_traj_add = open(file_write,"w")
    
            filename = path_cur + csv_file
            traj_file = open(filename, "r")
            line = traj_file.readlines()
            end_node = 0
            next_start_node_way = 0
            node_change = False
    #    In file, the list are write as:
    #    ['13301104012', '116.418137', '39.878758', '2', '734570373', '734571100', '20111104000147', '000', '30\n']
    #    only column 4, 5, 6 are useful to us
            for i in range(0, len(line) - 1):
    #            print line[i].split("\t")
                if i % 1000 == 0:
                    print i
                if len(line[i].split("\t")) == 1 :
                    node_id = line[i]
                    continue
                if len(line[i + 1].split("\t")) == 1 :
                    continue
                traj_i = line[i].split("\t")
                traj_i1 = line[i + 1].split("\t")
    
                if node_change == False:
                    start_node = traj_i[5]
                    another_start_node = traj_i[4]
                else:
                    start_node = end_node
                    another_start_node = next_start_node_way
                
                node_change = False
    
                sql_query = "SELECT * FROM public.planet_osm_ways WHERE %d = ANY (planet_osm_ways.nodes);"
                osm_cursor.execute(sql_query% int(start_node))
                start_node_index = osm_cursor.fetchall()
                
                end_node = traj_i1[4]
                sql_query = "SELECT * FROM public.planet_osm_ways WHERE %d = ANY (planet_osm_ways.nodes);"
                osm_cursor.execute(sql_query% int(end_node))
                try:
                    end_node_index = osm_cursor.fetchall()
                except Exception:
                    end_node_index = []
            
                end_node_d = find_node_pos(end_node)
                start_node_d = find_node_pos(start_node)
                #get start node way
                # compute the start node way linking to n ways
                # compute the linked way's linked out nodes, 
                # compete nodes
                # select a better nodes, reaching for the linking roads
                # if the end road way is in the set, return pass ways
                
                temp = []            
                start_node_ways = []
    
                for index in start_node_index:
                    temp.append(index[0])
                #temp are way ids.
                start_node_ways = temp
                if len(start_node_ways) > 1:
                    start_temp = long(another_start_node)
    
                    sql_query = "SELECT * FROM public.planet_osm_ways WHERE %d = ANY (planet_osm_ways.nodes);"
                    osm_cursor.execute(sql_query% long(start_temp))
                    start_temp = osm_cursor.fetchall()
                    start1_way = []
                    for start1_ways in start_temp:
                        start1_way.append(start1_ways[0])
                    temp_start_set = set(start1_way) & set(start_node_ways)
                    start_node_way = list(temp_start_set)
    
                else:
                    start_node_way = start_node_ways
    
                    
                end_ways = []
                
                for index in end_node_index:
                    end_ways.append(index[0])
                
                if start_node_way == []:
                    file_traj_add.writelines("shows negative in startnodes")
                    file_traj_add.writelines("Can be wrong nodes")
                    file_traj_add.writelines("\n")
                    print "start node way is null!!!"
                    continue
                way_traj = []
    
                current_way = start_node_way
                way_traj.append(current_way[0])
                
                if start_node_way[0] in end_ways:
                    search_node_query = "SELECT nodes FROM public.planet_osm_ways WHERE id = %d"
                    osm_cursor.execute(search_node_query% start_node_way[0])
                    start_node_way = osm_cursor.fetchall()[0][0]
                    pos_start = start_node_way.index(long(start_node))
                    pos_end = start_node_way.index(long(end_node))
                    single_traj = start_node_way[pos_start: pos_end + 1]
                    file_traj_add.writelines(str(str(start_node) + str(end_node)))
                    file_traj_add.writelines(str(single_traj))
                    file_traj_add.writelines("\n")
                    continue
                count = 0
                while True:
                    way_tuple = find_next_ways(current_way, end_node, end_ways)
                    ways_list = list(way_tuple[1])
                    next_way = way_tuple[0]
                    same_set = set(ways_list) & set(end_ways)
                    if len(same_set)!= 0 or way_tuple[0] in end_ways:
                        temp_list = []
                        temp_list.append(next_way)
                        temp_list.extend(way_tuple[1])
                        same_set1 = set(temp_list) & set(end_ways)
                        way_traj.extend(list(same_set1))
                        node_change = False
                        break        
                    else:
                        current_way = [next_way]
                        if current_way[0] in way_traj:
                            end_nodes_looking_query = "SELECT planet_osm_ways.nodes FROM public.planet_osm_ways WHERE id = %d"
                            osm_cursor.execute(end_nodes_looking_query% long(current_way[0]))
                            end_nodes_list = osm_cursor.fetchall()[0][0]
                            temp_end_node = end_nodes_list[0]
                            node_d = find_node_pos(end_nodes_list[0])
                            distance_end = distance(node_d, end_node_d, end_nodes_list[0], long(end_node))
    
                            
                            for i in range(1,len(end_nodes_list)):
                                node_d = find_node_pos(end_nodes_list[i])
                                distance1 = distance(node_d, end_node_d, end_nodes_list[i], long(end_node))
                                if distance1 < distance_end:
                                    temp_end_node = end_nodes_list[i]
                                    distance_end = distance1
                            end_node = temp_end_node
                            node_change = True;
                            cway_pos = way_traj.index(current_way[0])
                            way_traj = way_traj[0:cway_pos + 1]
                            break
                        way_traj.extend(current_way) 
                        count = count + 1
                    if count > 15:
                        break
                
                if count > 15:
                    file_traj_add.writelines(str(str(start_node) + "     " + str(end_node) + "\n"))
                    file_traj_add.writelines("Can be wrong nodes")
                    file_traj_add.writelines("\n")
                    print "can be wrong nodes"
                    continue
                    
                    
                if len(way_traj) == 1:
                    search_node_query = "SELECT nodes FROM public.planet_osm_ways WHERE id = %d"
                    osm_cursor.execute(search_node_query% way_traj[0])
                    start_node_way = osm_cursor.fetchall()[0][0]
                    pos_start = start_node_way.index(long(start_node))
                    pos_end = start_node_way.index(long(end_node))
                    single_traj = start_node_way[pos_start: pos_end + 1]
                    file_traj_add.writelines(str(str(start_node) + "     " + str(end_node) + "\n"))
                    file_traj_add.writelines(str(single_traj))
                    file_traj_add.writelines("\n")
                    continue
                single_traj = []
                start_node = long(start_node)
                search_node_query = "SELECT nodes FROM public.planet_osm_ways WHERE id = %d"
                osm_cursor.execute(search_node_query% way_traj[0])
                start_traj = osm_cursor.fetchall()[0][0]
                pos = start_traj.index(start_node)
    #            print start_node_index
    #            print end_node_index
    
    #            print way_traj
                osm_cursor.execute(search_node_query% way_traj[1])
                traj_2 = osm_cursor.fetchall()[0][0]
                set_middle_node = set(traj_2) & set(start_traj)
                pos_m = start_traj.index(list(set_middle_node)[0])
                if pos_m == 0:
                    insert = start_traj[pos_m : pos + 1]
                    insert.reverse()
                    single_traj.extend(insert)
                else:
                    single_traj.extend(start_traj[pos:pos_m + 1])
    
                for i in range(1, len(way_traj) - 2):
                    osm_cursor.execute(search_node_query% way_traj[i])
                    nodes_in_way = osm_cursor.fetchall()[0][0]
                    single_traj.extend(nodes_in_way)
                
                end_node = long(end_node)
                osm_cursor.execute(search_node_query% way_traj[-1])
                end_traj = osm_cursor.fetchall()[0][0]
                pos = end_traj.index(end_node)
                
                osm_cursor.execute(search_node_query% way_traj[-2])
                traj_1 = osm_cursor.fetchall()[0][0]
                set_middle_node = set(traj_1) & set(end_traj)
                pos_m = end_traj.index(list(set_middle_node)[0])
                next_start_node_way = end_traj[pos - 1]
    
                
                if pos_m == 0:
                    insert = end_traj[pos_m : pos + 1]
                    single_traj.extend(insert)            
                else:
                    insert = end_traj[pos : pos_m + 1]
                    insert.reverse()
                    single_traj.extend(insert)  
                file_traj_add.writelines(str(str(start_node) + "     " + str(end_node) + "\n"))
                file_traj_add.writelines(str(single_traj))
                file_traj_add.writelines("\n")
    
            file_traj_add.close()
            print "file " + csv_file + "finished"
                
                
node_connect = psycopg2.connect(database = "node_index", user = "postgres", port = "5432",)
osm_connect = psycopg2.connect(database = "beijing_osm_old", user = "postgres", port = "5432", )

node_cursor = node_connect.cursor()
osm_cursor = osm_connect.cursor()

file_write = "test1.txt"
file_traj_add = open(file_write,"w")

path = "g:\\car2.0\\"
print path
dir_file = os.listdir(path)
print dir_file
for dir in dir_file:
    path_cur = path + dir + "\\"
    
    print path_cur
    csv_files_in_folder = os.listdir(path_cur)
    
    print csv_files_in_folder
    for i in range(2, len(csv_files_in_folder)):
        thread.start_new_thread(file_manipulate,((path_cur, csv_files_in_folder[i])))
        sleep(3600)
        
    
                
                
                
'''
            for temp_way in start_node_ways:
                node_cursor.execute(node_query% (temp_way))
                way_ids = node_cursor.fetchall()
                ways = find_next_ways(start_node_ways, end_node)
'''
'''
Created on Sep 22, 2014
                
'''
'''            elif(len(start_node_index) != 1 and len(end_node_index) == 1):
                traj_start_nodes = []
                end_node_way = list(end_node_index)[0]
                for ways in start_node_index:
                    traj_start_nodes.append(ways[0])
                find_ways = []
                for traj_start_node in traj_start_nodes:
                    node_query = "SELECT node_index.index_road FROM public.node_index WHERE node_id = %d "
                    print node_query% (traj_start_node)
                    node_cursor.execute(node_query% (traj_start_node))
                    node_road_result = list(node_cursor.fetchall())
                    find_ways.append(node_road_result)
                find_ways = list(set(find_ways))
'''                
'''
                node_far = []
                for way in start_node_ways:
                    node_id_query = "SELECT planet_osm_ways.nodes FROM public.planet_osm_ways WHERE id = %d"
                    osm_cursor.execute(node_id_query% long(way))
                    way_connect = list(osm_cursor.fetchall()[0])[0]
                    node_far.append(way_connect[0])
                    node_far.append(way_connect[-1])
                end_node_dic = find_node_pos(int(end_node))
                    
                node1 = find_node_pos(node_far[0])
                dist = distance(node1, end_node_dic, node_far[0], int(end_node))

                optimal_node_dist = dist
                optimal_node_id = node1

                for node in node_far:
                    node_dic = find_node_pos(node)
                    dist = distance(node_dic, end_node_dic, node, int(end_node))
                    if optimal_node_dist > dist:
                        optimal_node_dist = dist
                        optimal_node_id = node
                optimal_way_query = "SELECT node_index.index_road FROM public.node_index WHERE node_id = %d"
                node_cursor.execute(optimal_way_query% long(optimal_node_id))
                temp_way = node_cursor.fetchall()[0][0]
                for temp in temp_way:
                    if temp in start_node_ways:
                        break
            
                start_node_way = temp
            else:
                start_node_way = start_node_ways


'''
'''
@author: chen
'''
