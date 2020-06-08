from igraph import *
import random
import csv


g = Graph.Read('azer.graphml', format='graphml')
# print(g.vs['name'])
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

Multi = g.community_multilevel( return_levels=False)
LPM = g.community_label_propagation()
Walk = g.community_walktrap(steps=4)
info = g.community_infomap(vertex_weights=None, trials=10)
Leiden = g.community_leiden(objective_function='modularity', resolution_parameter=1.0, beta=0.01,  initial_membership=None, n_iterations=2, node_weights=None)
Walktrap = Walk.as_clustering()

def print_cluster_count():
    print('Count of clusters')
    print('Louvain: ', len(Multi))
    print('LPM: ', len(LPM))
    print('WalkTrap: ', len(Walktrap))
    print('Infomap: ', len(info))
    print('Leiden: ', len(Leiden))

# print_cluster_count()

Q = []
def print_modularity():
    Q_M = g.modularity(Multi)
    Q_L = g.modularity(LPM)
    Q_W = g.modularity(Walktrap)
    Q_Info = g.modularity(info)
    Q_Leiden = g.modularity(Leiden)
    Q.extend([toFixed(Q_M, 5), toFixed(Q_L, 5), toFixed(Q_W, 5), toFixed(Q_Info, 5), toFixed(Q_Leiden, 5)])
    return Q

with open('Modularity.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(print_modularity())

#сообщества для сравнения
# GT_Louvain = g.community_multilevel(weights = 'weight', return_levels=False)
# GT_Leiden = g.community_leiden(objective_function='modularity', weights= 'weight', resolution_parameter=1.0, beta=0.01,  initial_membership=None, n_iterations=2, node_weights=None)

GT_Louvain = Multi
GT_Leiden = Leiden
#массвы получившихся значений мер
NMILouvain = []
NMILeiden = []
ARILouvain = []
ARILeiden = []
SJD = []
SJD1 = []
def print_NMI_Louvain():
    NMI_Louvain = compare_communities(Multi.membership, GT_Louvain.membership, method = 'nmi')
    NMI_LPM = compare_communities(LPM.membership, GT_Louvain.membership, method = 'nmi')
    NMI_WalkTrap = compare_communities(Walktrap.membership, GT_Louvain.membership, method='nmi')
    NMI__Info = compare_communities(info.membership, GT_Louvain.membership, method='nmi')
    NMI_Leiden = compare_communities(Leiden.membership, GT_Louvain.membership, method='nmi')
    NMILouvain.extend([toFixed(NMI_Louvain, 5), toFixed(NMI_LPM, 5), toFixed(NMI_WalkTrap, 5), toFixed(NMI__Info, 5), toFixed(NMI_Leiden, 5)])
    return NMILouvain
    # print(NMI_Louvain)
    # print(NMI_LPM)
    # print(NMI_WalkTrap)
    # print(NMI__Info)
    # print(NMI_Leiden)
def print_NMI_Leiden():
    NMI_Louvain = compare_communities(Multi.membership, GT_Leiden.membership, method = 'nmi')
    NMI_LPM = compare_communities(LPM.membership, GT_Leiden.membership, method = 'nmi')
    NMI_WalkTrap = compare_communities(Walktrap.membership, GT_Leiden.membership, method='nmi')
    NMI__Info = compare_communities(info.membership, GT_Leiden.membership, method='nmi')
    NMI_Leiden = compare_communities(Leiden.membership, GT_Leiden.membership, method='nmi')
    NMILeiden.extend([toFixed(NMI_Louvain, 5), toFixed(NMI_LPM, 5), toFixed(NMI_WalkTrap, 5), toFixed(NMI__Info, 5), toFixed(NMI_Leiden, 5)])
    return NMILeiden

    # print(NMI_Louvain)
    # print(NMI_LPM)
    # print(NMI_WalkTrap)
    # print(NMI__Info)
    # print(NMI_Leiden)

def print_SJD_Louvain():
    SJD_Louvain = compare_communities(Multi.membership, GT_Louvain.membership, method = 'split-join')
    SJD_LPM = compare_communities(LPM.membership, GT_Louvain.membership, method='split-join')
    SJD_WalkTrap = compare_communities(Walktrap.membership, GT_Louvain.membership, method='split-join')
    SJD_Info = compare_communities(info.membership, GT_Louvain.membership, method='split-join')
    SJD_Leiden = compare_communities(Leiden.membership, GT_Louvain.membership, method='split-join')
    SJD.extend([SJD_Louvain, SJD_LPM, SJD_WalkTrap,SJD_Info, SJD_Leiden])
    return SJD
    # print(SJD_Louvain)
    # print(SJD_LPM)
    # print(SJD_WalkTrap)
    # print(SJD_Info)
    # print(SJD_Leiden)
def print_SJD_Leiden():
    SJD_Louvain = compare_communities(Multi.membership, GT_Leiden.membership, method = 'split-join')
    SJD_LPM = compare_communities(LPM.membership, GT_Leiden.membership, method='split-join')
    SJD_WalkTrap = compare_communities(Walktrap.membership, GT_Leiden.membership, method='split-join')
    SJD_Info = compare_communities(info.membership, GT_Leiden.membership, method='split-join')
    SJD_Leiden = compare_communities(Leiden.membership, GT_Leiden.membership, method='split-join')
    SJD1.extend([SJD_Louvain, SJD_LPM, SJD_WalkTrap, SJD_Info, SJD_Leiden])
    return SJD1
    # print(SJD_Louvain)
    # print(SJD_LPM)
    # print(SJD_WalkTrap)
    # print(SJD_Info)
    # print(SJD_Leiden)

def print_ARI_Louvain():
    ARI_Louvain = compare_communities(Multi.membership, GT_Louvain.membership, method='adjusted_rand')
    ARI_LPM = compare_communities(LPM.membership, GT_Louvain.membership, method='adjusted_rand')
    ARI_WalkTrap = compare_communities(Walktrap.membership, GT_Louvain.membership, method='adjusted_rand')
    ARI_Info = compare_communities(info.membership, GT_Louvain.membership, method='adjusted_rand')
    ARI_Leiden = compare_communities(Leiden.membership, GT_Louvain.membership, method='adjusted_rand')
    ARILouvain.extend([toFixed(ARI_Louvain, 5), toFixed(ARI_LPM, 5), toFixed(ARI_WalkTrap, 5), toFixed(ARI_Info, 5), toFixed(ARI_Leiden, 5)])
    return ARILouvain
    # print(ARI_Louvain)
    # print(ARI_LPM)
    # print(ARI_WalkTrap)
    # print(ARI_Info)
    # print(ARI_Leiden)
def print_ARI_Leiden():
    ARI_Louvain = compare_communities(Multi.membership, GT_Leiden.membership, method = 'adjusted_rand')
    ARI_LPM = compare_communities(LPM.membership, GT_Leiden.membership, method='adjusted_rand')
    ARI_WalkTrap = compare_communities(Walktrap.membership, GT_Leiden.membership, method='adjusted_rand')
    ARI_Info = compare_communities(info.membership, GT_Leiden.membership, method='adjusted_rand')
    ARI_Leiden = compare_communities(Leiden.membership, GT_Leiden.membership, method='adjusted_rand')
    ARILeiden.extend([toFixed(ARI_Louvain, 5), toFixed(ARI_LPM, 5), toFixed(ARI_WalkTrap, 5), toFixed(ARI_Info, 5), toFixed(ARI_Leiden, 5)])
    return ARILeiden
    # print(ARI_Louvain)
    # print(ARI_LPM)
    # print(ARI_WalkTrap)
    # print(ARI_Info)
    # print(ARI_Leiden)


def print_measures():
    with open('array.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(print_SJD_Louvain())
        wr.writerow(print_NMI_Louvain())
        wr.writerow(print_ARI_Louvain())
        wr.writerow(print_SJD_Leiden())
        wr.writerow(print_NMI_Leiden())
        wr.writerow(print_ARI_Leiden())

print_measures()

