#%% Pre-processing Functions for Clustering Algorithm 2
import numpy as np
import networkx as nx
import pandas as pd

def stockReturns(priceDF):
    
    # Method 1: Compute daily returns by parsing the Data Frame as numpy matrix (Fastest)
    compTickers = priceDF.columns[1: ]    
    priceMat = priceDF.loc[ : , compTickers].as_matrix()    
    diffMat = (priceMat[1: ] - priceMat[ :-1]) / priceMat[ :-1]
    
    return pd.DataFrame(data = diffMat, index = priceDF.index[1: ], columns = compTickers)


def calCorrelations(dailyReturn):
    
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