import requests
import json
import time
import networkx
import io

table = io.open('sorted.csv', 'r')
result = io.open('pairs.csv', 'a')

tmp_member = 0
tmp_list = []
for line in table:
    #print(line)
    group = line.split(',')[0]
   # print(line)
    member = int(line.split(',')[1])
    if tmp_member != member:
        if len(tmp_list) > 1:
            for i in range(len(tmp_list)-1):
                for j in range(i+1, len(tmp_list)):
                    result.write(str(tmp_list[i])+','+str(tmp_list[j])+'\n')
        tmp_member = member
        tmp_list = [group]
    else:
        tmp_list.append(group)
