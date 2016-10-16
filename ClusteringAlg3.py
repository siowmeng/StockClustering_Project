# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 08:50:11 2016

@author: louisefallon
"""
import ClusteringAlg3Helpers as nh

#%%
# Create the function that performs the clustering algorithm
def ClusteringAlg3(firm_set, ord_list, k = 5):
    '''
    Description:
        - Clusters the firm_set, based on k iterations of a clustering algorithm
        based on sequential merging of sets, based on a rank value that is found
        in the first place of the ord_list, and links two elements from the firm_set.
    Input:
        - firm_set: A set of strings (expected to be a set of firm stock ticker strings)
        - ord_list: An ordered list of items with:
            - A ranked value (expected to be stock correlations)
            - An element from the set (expected to be a firm stock ticker string)
            - Another element from the set (expected to be a firm stock ticker string)
        - k: An integer, which determines the number of iterations
    Output:
        - A list of sets (clusters), the sets contain strings of firm names.
    '''
    
    ##change the firm_set into a dictionary which has
    ##a key - which is the firm name
    ##a list - including
    ##    a "prev" firm name
    ##    and a "next" firm name
    firmdict = {}
    for firm in firm_set:
        firmdict[firm] = [firm, firm]
    setOfStartNodes = set(firm_set)
    
    ##complete the loop k times
    for i in range(0,k):
        
        #take an item from the ordered list
        coritem = ord_list.pop(0)
        
        ##error handling - check that both the source and destination
        ##elements are in the list of firms
        if(coritem[1] not in firm_set or coritem[2] not in firm_set):
            return("The ordered list must contain elements from the set")
        
        ##check if the firms are already in the same "set"
        ##i.e. have the same bottom node
        lastnodefromsource = nh.findBottomNode(coritem[1],firmdict)
        lastnodefromdest = nh.findBottomNode(coritem[2],firmdict)
        if (lastnodefromsource == lastnodefromdest):
            pass
        
        else:
        ## Otherwise, get the top node of the destination
            firstnodefromdest = nh.findTopNode(coritem[2],firmdict)
        ## set the bottom node of the source to have a
        ## "next" pointer to the top node of the destination       
            firmdict[lastnodefromsource][1] = firstnodefromdest
        ## & visa versa set the "prev" pointer of the top node of the
        ## destination to the bottom node of the source
        ## i.e. join the sets such that there is only one "line"
        ## from start to finish
            firmdict[firstnodefromdest][0] = lastnodefromsource
        ## Remove the start node of the destination from start nodes
        ## as it now has a previous node, and is not a start.
            setOfStartNodes.remove(firstnodefromdest)

    return (nh.ReturnClusters(firmdict, setOfStartNodes))
    

    