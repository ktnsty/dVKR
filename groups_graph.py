import requests
import json
import time
import networkx
import collections
import re
import io
import matplotlib.pyplot as plt
import community.community_louvain as community
import collections
import matplotlib.colors as mcolors

group_file = io.open('islamskie.txt', 'r')

namecount = io.open('namecount_islamskie.csv', 'r', encoding='utf8')

token = open('token.txt')
for line in token:
    token = line
ACCESS_TOKEN = token
group_get_count = "https://api.vk.com/method/groups.getById?group_id={}&fields=members_count&v=5.103&access_token={}"


namecount_arr = []
for line in namecount:
    name = line.split(',')[0].replace('\n', '')
    count = int(line.split(',')[-1].replace('\n', ''))
    namecount_arr.append([name, count])


group_list = []
for line in group_file:
    group = line.split('/')[3].split('\n')[0].replace(' ', '')
    if re.fullmatch(r'club\d+', group):
        group = group[4:]
    if re.fullmatch(r'public\d+', group):
        group = group[6:]
    group_list.append(group)

group_file.close()

g = networkx.Graph(directed=False)

for i in range(len(group_list)):                # добавление группы, как узла
    named = namecount_arr[i][0]
    counted = namecount_arr[i][1]
    if named != 'error':
        g.add_node(group_list[i], name=named, count=counted)

pairs_file = io.open('pairs.csv', 'r')

for line in pairs_file:                   #создание узлов между ними
    (g1, g2) = line.split(',')
    g1 = g1.replace('\n', '')
    g2 = g2.replace('\n', '')
    if g.has_edge(g1, g2):
        g.edges[g1, g2]['weight'] += 1
    else:
        g.add_edge(g1, g2, weight=1)

# g.remove_nodes_from(list(networkx.isolates(g)))
g.remove_edges_from(list(networkx.selfloop_edges(g)))

print(g.number_of_nodes())
print(g.number_of_edges())

# networkx.draw(g)
# networkx.draw(g, pos = networkx.spectral_layout(g), nodecolor='r',edge_color='b')
# plt.show()
# plt.savefig('graph.png')
# plt.close()


# part = community.best_partition(g)
# partition = community.best_partition(g)
# pos = community_layout(g, partition)
# networkx.draw(g, pos, node_color=list(partition.values()));
# plt.show()
# plt.savefig('graph.png')
# mod = community.modularity(part, g)
# print("modularity:", mod)






# bet_centr = networkx.betweenness_centrality(g)
# clo_centr = networkx.closeness_centrality(g)
# eig_centr = networkx.eigenvector_centrality(g)
#
# print(bet_centr)
# print(clo_centr)
# print(eig_centr)
#
#
networkx.write_graphml(g, 'islamskie.graphml')






#------------------------------------------------------------------------------ Получение экстремистов ололо
# extr = io.open('extrimist.txt', 'r')
#
# namecount_ex = io.open('namecount_extrimist.csv', 'r', encoding='utf8')
# namecount_extr = []
#
# for line in namecount_ex:
#     name_ex = line.split(',')[0].replace('\n', '')
#     count_ex = int(line.split(',')[-1].replace('\n', ''))
#     namecount_extr.append([name_ex, count_ex])
#
#
# extrimists = []
# for line in extr:
#     group = line.split('/')[3].split('\n')[0].replace(' ', '')
#     if re.fullmatch(r'club\d+', group):
#         group = group[4:]
#     if re.fullmatch(r'public\d+', group):
#         group = group[6:]
#     extrimists.append(group)
#
# print(extrimists)
# extr.close()
#
# new_graph = networkx.Graph(directed=False)
#
# i = 0
#
# print(len(networkx.get_node_attributes(g, "name")))
# print(networkx.number_of_nodes(g))
#
# for groupId in extrimists:
#     named_ex = namecount_extr[i][0]
#     counted_ex = namecount_extr[i][1]
#     i += 1
#     new_graph.add_node(groupId, name = named_ex, count = counted_ex)
#     for neighbor in g.neighbors(groupId):
#         name_n = networkx.get_node_attributes(g, 'name')[neighbor]
#         count_n = networkx.get_node_attributes(g, 'count')[neighbor]
#         new_graph.add_node(neighbor, name = name_n, count = count_n)
#
# for v in new_graph.nodes():
#     for u in new_graph.nodes():
#         if g.has_edge(v, u):
#             new_graph.add_edge(v, u)
#             new_graph.edges[u, v]["weight"] = g.edges[u, v]["weight"]
#             print(new_graph.edges[u, v]["weight"])
#
# new_graph.remove_nodes_from(list(networkx.isolates(new_graph)))
# new_graph.remove_edges_from(list(networkx.selfloop_edges(new_graph)))
#
# networkx.write_graphml(new_graph, 'extrimist20_erkin_qaraqalpaqstan.graphml')
#
#
# clearing all files