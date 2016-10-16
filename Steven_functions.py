# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 18:07:38 2016

@author: Steven
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_clusters(list_of_sets):
    '''
    input: clusters from evaluation of clustering algorithm
    output: extract all clusters longer than 1 for evaluation of clusters
    '''
    
    extracted_sets = []
    
    for item in list_of_sets:
            if len(item) > 1:
                extracted_sets.append(item)
    
    return(extracted_sets)
    
   
   
   
def mean_of_list(list):
    '''
    input: list of numbers
    output: mean of these numbers
    '''
    sum = 0
    
    for item in list:
        sum += item
        
    mean = sum / len(list)
    
    return mean
    
    
def name_columns(dataframe):
    '''
    input: takes dataframe with average means and returns of clusters as input
    output: returns dataframe with 'Cluter 1, Cluster 2,...' names
    '''
    
    colnames = []
    
    for i in range(len(dataframe.columns)):
        name = 'Cluster ' + str(i + 1)
        colnames.append(name)
        
    dataframe.columns = colnames
    return dataframe
    
    
    
def evaluate_clusters(list_of_sets):
    '''
    input: uses a list of clusters
    output: average return and average risk of given cluster
    
    '''
    
    dframe = pd.DataFrame()
    
    count = 0
    
    mean_dframe = dailyReturns.mean()
    sd_frame = dailyReturns.std()
    
    for set in list_of_sets:
        
        iterable_set = list(set)
        
        mean = []
        sd = []        
        
        for stock in iterable_set:
            mean.append(mean_dframe[stock])
            sd.append(sd_frame[stock])
        
        mean_set = mean_of_list(mean)
        sd_set = mean_of_list(sd)
        
        dframe[count] = [mean_set, sd_set]
        
        count += 1
        
    dframe.index = ['Average Return', 'Average Risk']
    name_columns(dframe)
        
    return dframe
        
        
        
def risk_analysis(evaluted_cluster_dframe):
    """ input: table of clusters
        output: plot to asses risk / return of clusters
        note: gets a little crowded with more than 5 clusters
    """

    area = np.pi * 3
    
    plt.figure(figsize = (8,6))
    plt.scatter(evaluted_cluster_dframe.loc['Average Return'], evaluted_cluster_dframe.loc['Average Risk'], s = area)
    plt.xlabel('Expected return')
    plt.ylabel('Risk')
    
    for label,x,y in zip(evaluted_cluster_dframe.columns, evaluted_cluster_dframe.loc['Average Return'], evaluted_cluster_dframe.loc['Average Risk']):
        plt.annotate(
        label,
        xy = (x,y), xytext = (50, 50),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3, rad=0.5'))
        
    
        
    

    