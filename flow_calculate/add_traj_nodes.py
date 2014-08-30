'''
Created on Aug 15, 2014

@author: chen
'''
import csv;
import psycopg2;

node_string_file = open("g:\\sort\\2\\13301104001_sort.csv", "r")
node_string = csv.reader(node_string_file)


conn = psycopg2.connect(database = "node_in_road", user = "postgres", port = "5432", )
cur = conn.cursor()
cur_count = conn.cursor()

for row in node_string:
    print row