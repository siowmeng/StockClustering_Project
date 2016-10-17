# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:50:23 2016

@author: siowmeng
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

def stockReturns(priceDF):
    
    # Method 1: Compute daily returns by parsing the Data Frame as numpy matrix (Fastest)
    compTickers = priceDF.columns[1: ]    
    priceMat = priceDF.loc[ : , compTickers].as_matrix()    
    diffMat = (priceMat[1: ] - priceMat[ :-1]) / priceMat[ :-1]
    
    return pd.DataFrame(data = diffMat, index = priceDF.index[1: ], columns = compTickers)
    
    # Method 2: Compute daily returns by perfoming assignment directly on pandas Data Frame (Slowest)
#    dailyDF = pd.DataFrame(index = priceDF.index, columns = priceDF.columns)
#    dailyDF.Date = priceDF.Date
#    
#    for company in compNames:
#        for i in range(1, len(priceDF)):
#            prevPrice = priceDF.loc[i - 1, company]
#            currPrice = priceDF.loc[i, company]
#            dailyDF.loc[i, company] = (currPrice - prevPrice) / prevPrice
#    
#    return dailyDF[1: ]
    
    # Method 3: Compute daily returns by perfoming assignment directly on 2D array (Slower)
#    nrow = priceDF.shape[0] - 1
#    ncol = priceDF.shape[1] - 1
#    dailyReturn = [[0 for x in range(ncol)] for y in range(nrow)]
#    
#    for i in range(0, nrow):
#        
#        j = 0
#        for company in compNames:
#            prevPrice = priceDF.loc[i, company]
#            currPrice = priceDF.loc[i + 1, company]
#            dailyReturn[i][j] = (currPrice - prevPrice) / prevPrice
#            j += 1
#            
#    return dailyReturn

def calCorrelations(dailyReturn):
    
    # Method 1: Pandas built-in function to calculate pairwise correlation (Fastest)
#    return dailyReturn.corr()
    
    # Method 2: Manual calculation of pairwise correlation using numpy matrix (Faster)
    col = dailyReturn.columns
    ncol = len(col)
    corrMat = np.identity(ncol)
    
    G = nx.Graph()
    G.add_nodes_from(col.values)
        
    n = len(dailyReturn)
    k = 0
    for i in range(0, ncol):
        for j in range(i + 1, ncol):
            x = dailyReturn[col[i]]
            y = dailyReturn[col[j]]
            xsum = sum(x)
            ysum = sum(y)
            corrMat[i][j] = (n * sum(x * y) - xsum * ysum) / (np.sqrt(n * sum(x**2) - xsum**2) * np.sqrt(n * sum(y**2) - ysum**2))
            corrMat[j][i] = corrMat[i][j]
            G.add_edge(col[i], col[j], weight = corrMat[i][j])
        k += 1
        
    return pd.DataFrame(data = corrMat, index = col, columns = col), G
    
    # Method 3: Manual calculation of pairwise correlation using numpy matrix (Faster)
#    col = dailyReturn.columns
#    ncol = len(col)
#    corrMat = np.zeros([ncol, ncol])
#        
#    n = len(dailyReturn)     
#    k = 0
#    for i in range(0, ncol):
#        for j in range(i, ncol):
#            x = dailyReturn[col[i]]
#            y = dailyReturn[col[j]]
#            xsum = sum(x)
#            ysum = sum(y)
#            corrMat[i][j] = (n * sum(x * y) - xsum * ysum) / (np.sqrt(n * sum(x**2) - xsum**2) * np.sqrt(n * sum(y**2) - ysum**2))
#        k += 1
#        
#    return pd.DataFrame(data = corrMat, index = col, columns = col)
    
    # Method 4: Manual calculation of pairwise correlation using pandas Data Frame (Slower)
      
#    corrDF = pd.DataFrame(index = dailyReturn.columns, columns = dailyReturn.columns)
#    corrDF.fillna(0)
#
#    k = 0
#    n = len(dailyReturn)
#    for i in corrDF.index:
#        for j in corrDF.index[k: ]:
#            x = dailyReturn[i]
#            y = dailyReturn[j]
#            xsum = sum(x)
#            ysum = sum(y)
#            corr = (n * sum(x * y) - xsum * ysum) / (np.sqrt(n * sum(x**2) - xsum**2) * np.sqrt(n * sum(y**2) - ysum**2))
#            corrDF.loc[i, j] = corr
#        k += 1
#    
#    return corrDF    

def stockClustering(graph, k):
            
    # Method 1: Clustering using dictionary and list
    sortedEdges = sorted(graph.edges(data = True), key = lambda edge: edge[2]['weight'], reverse = True) # O(e log e), e = number of edges = n(n - 1)/2 for dense graph
    
    listSets = dict()    
    for node in graph.nodes(): # O(n), n = number of companies
        listSets[node] = {node}
        
    for i in range(0, k): # Execute k times
        (a, b, data) = sortedEdges[i]
        mergedSet = listSets[a].union(listSets[b]) # O(len(set(a)) + len(set(b))) = O(n) in worst case since the biggest possible set is the set with all n companies
        for node in mergedSet: # O(n)
            listSets[node] = mergedSet
    # The whole chunk above is O(kn + kn) = O(kn)
            
    resultSets = []
    for nodeSet in listSets.values(): # O(n)
        if nodeSet not in resultSets:
            resultSets.append(nodeSet)
        
    return resultSets
    
    # Method 2: Clustering using networkx graph
#    sortedEdges = sorted(graph.edges(data = True), key = lambda edge: edge[2]['weight'], reverse = True)
#    
#    G = nx.Graph()
#    G.add_nodes_from(graph.nodes())
#    
#    for i in range(0, k):
#        (a, b, data) = sortedEdges[i]
#        G.add_edge(a, b)
#        
#    return sorted(nx.connected_components(G))

# KMeans Clustering Algorithm
def stockClusteringKMeans(dailyReturn, num_clusters):
    # Using daily closing price for K-Means
    compTickers = dailyReturn.columns
    dailyReturnArray = dailyReturn.as_matrix().transpose()
    kmeans = KMeans(n_clusters = num_clusters, random_state = 0).fit(dailyReturnArray)
    
    resultSets = [set()] * num_clusters
    i = 0
    
    for l in kmeans.labels_:
        resultSets[l] = resultSets[l].union({compTickers[i]})
        i += 1
    
    return resultSets
    
    # Using standard deviation of each company for K-Means
#    stdDev = dailyReturn.std(axis = 0)
#    compTickers = stdDev.index
#    stdDevArray = np.reshape(stdDev.as_matrix(), (len(stdDev), 1))
#    kmeans = KMeans(n_clusters = num_clusters, random_state = 0).fit(stdDevArray)
#    
#    resultSets = [set()] * num_clusters
#    i = 0
#    
#    for l in kmeans.labels_:
#        resultSets[l] = resultSets[l].union({compTickers[i]})
#        i += 1
#        
#    return resultSets

# Hierachical (Agglomerative) Clustering with Average Linkage
def stockClusteringAgglomerative(corrDF, num_clusters):
    compTickers = corrDF.columns
    # Transform correlation matrix into distance matrix
    affinityMatrix = abs(corrDF.as_matrix() - 1)
    model = AgglomerativeClustering(linkage = 'average', affinity = 'precomputed', n_clusters = num_clusters)
    aggFit = model.fit(affinityMatrix)
    
    resultSets = [set()] * num_clusters
    i = 0
    
    for l in aggFit.labels_:
        resultSets[l] = resultSets[l].union({compTickers[i]})
        i += 1
        
    return resultSets

