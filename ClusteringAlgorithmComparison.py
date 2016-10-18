# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 08:50:11 2016
"""

#%% Clustering Algorithm 1
def clusteringAlg1(cor_list, k = 0):
    """
    Input:  
    list: The list of tuples which include the
              correlations between firms and the firms themselves
    k: The number of iterations for the clustering algorithm
    Output: 
    A list of sets where each set represents an individual 
    cluster
    """
    #Order the list
    ord_list = sorted(cor_list, reverse = True)


    # Initialize the list of sets. Each set represents a cluster
    # which initialy includes only one firm
    sets = []
    for i in range(len(ord_list)): #O(n^2), n = number of companies,
        if not({ord_list[i][1]} in sets): #O(n)
            sets.append({ord_list[i][1]})
        if not({ord_list[i][2]} in sets): #O(n)
            sets.append({ord_list[i][2]}) 
    
    # Repeat the algorithm k times
    # In each iteration we check the k-th tuple of correlations list
    # and whether the 2 firms in that tuple are already in the same
    # set. If they do, we move on to the next tuple, otherwise we merge
    for j in range(min(k, len(ord_list))): #O(k) or O(n^2), depends on which is larger
        nd1 = ord_list[j][1]
        nd2 = ord_list[j][2]
        fl1, fl2 = False, False    
        for i in range(len(sets)): # O(n), as each node is “checked” twice
            if (nd1 in sets[i]) and fl1 == False:
                idx1 = i
                fl1 = True
            if (nd2 in sets[i]) and fl2 == False:
                idx2 = i
                fl2 = True
        if idx1 != idx2:
            sets[idx1] = sets[idx1].union(sets[idx2]) # O(len(set(a)) + len(set(b))) = O(n) in worst case since the biggest possible set is the set with all n companies
            sets.remove(sets[idx2]) # O(n)
    # Return the final list of sets
    return sets
    # The main loop chunks time-complexity = O(kn), given k < len(ord_list)

#%% Clustering Algorithm 2

def clusteringAlg2(graph, k):
            
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


#%% Helper Functions for Clustering Algorithm 3
def findBottomNode(input_firm, firmDict):
    '''
    Description:
        - Finds the bottom node of a doubly-linked list of nodes
    Input:
        - input_firm: a string that identifies the node to start searching from
        - firmDict: a dictionary that contains:
            - keys that refer to firms, one of which should be the input firm
            - values of 2-length lists, where:
                - the first value is a string refering to the "previous" firm
                - the second value is a string referring to the "next" firm
    Output:
        - a string referring to the firm at the end of the doubly linked list
        in which the start node (input_firm) belongs.
    '''
    if (firmDict[input_firm][1] == input_firm):
        return input_firm
    else:
        return(findBottomNode(firmDict[input_firm][1],firmDict))
        
def findTopNode(input_firm, firmDict):
    '''
    Description:
        - Finds the top node of a doubly-linked list of nodes
    Input:
        - input_firm: a string that identifies the node to start searching from
        - firmDict: a dictionary that contains:
            - keys that refer to firms, one of which should be the input firm
            - values of 2-length lists, where:
                - the first value is a string refering to the "previous" firm
                - the second value is a string referring to the "next" firm
    Output:
        - a string referring to the firm at the start of the doubly linked list
        in which the start node (input_firm) belongs.
    '''
    if (firmDict[input_firm][0] == input_firm):
        return input_firm
    else:
        return(findTopNode(firmDict[input_firm][0],firmDict))

def ReturnClusters(firmdict, setOfStartNodes):
    '''
    Description:
        - Clusters the firm_set, based on k iterations of a clustering algorithm
        based on sequential merging of sets, based on a rank value that is found
        in the first place of the ord_list, and links two elements from the firm_set.
    Input:
        - A set of strings (expected to be a set of firm stock ticker strings)
        - An ordered list of items with:
            - A ranked value (expected to be stock correlations)
            - An element from the set (expected to be a firm stock ticker string)
            - Another element from the set (expected to be a firm stock ticker string)
        - An integer, which determines the number of iterations
    Output:
        - A list of sets (clusters), the sets contain strings of firm names.
    '''
    startnodes = set(setOfStartNodes)
    listofsets = []
    while (len(startnodes) != 0):
        currentnode = startnodes.pop()
        currentset = set()
        currentset.add(currentnode)
        while (firmdict[currentnode][1] != currentnode):
            currentnode = firmdict[currentnode][1]
            currentset.add(currentnode)
        listofsets.append(currentset)
    return listofsets

#%% Clustering Algorithm 3
# Create the function that performs the clustering algorithm
def clusteringAlg3(cor_list, k = 5):
    '''
    Description:
        - Clusters the firm_set, based on k iterations of a clustering algorithm
        based on sequential merging of sets, based on a rank value that is found
        in the first place of the ord_list, and links two elements from the firm_set.
    Input:
        - firm_set: A set of strings (expected to be a set of firm stock ticker strings)
        - cor_list: An unordered list of items with:
            - A ranked value (expected to be stock correlations)
            - An element from the set (expected to be a firm stock ticker string)
            - Another element from the set (expected to be a firm stock ticker string)
        - k: An integer, which determines the number of iterations
    Output:
        - A list of sets (clusters), the sets contain strings of firm names.
    '''

    ##Create a new list, so that it can be popped without updating the original.
    ord_list = list(cor_list)
    #Order the list in ascending order, so pop() will take the highest correlation.
    ord_list = sorted(ord_list)

    ##Creating a set of firms that are in the ordered list, in either position
    ##(source or destination)
    firm_set = set()
    for i in range(len(ord_list)): # O(n^2), n = number of companies
            firm_set.add(ord_list[i][1])
            firm_set.add(ord_list[i][2])
    ##change the firm_set into a dictionary which has
    ##a key - which is the firm name
    ##a list - including
    ##    a "prev" firm name
    ##    and a "next" firm name
    firmdict = dict()
    for firm in firm_set: # O(n)
        firmdict[firm] = [firm, firm]
    setOfStartNodes = set(firm_set)
    
    ##complete the loop k times
    for i in range(0,k): #O(k)
        
        #take an item from the ordered list
        coritem = ord_list.pop() # O(1)
        
        ##check if the firms are already in the same "set"
        ##i.e. have the same bottom node
        lastnodefromsource = findBottomNode(coritem[1],firmdict) # O(n), worst case = the path contains all companies
        lastnodefromdest = findBottomNode(coritem[2],firmdict) # O(n), worst case = the path contains all companies
        if (lastnodefromsource == lastnodefromdest):
            pass #O(1)
        
        else:
        ## Otherwise, get the top node of the destination
            firstnodefromdest = findTopNode(coritem[2],firmdict) # O(n), worst case = the path contains all companies
        ## set the bottom node of the source to have a
        ## "next" pointer to the top node of the destination       
            firmdict[lastnodefromsource][1] = firstnodefromdest #O(1)
        ## & visa versa set the "prev" pointer of the top node of the
        ## destination to the bottom node of the source
        ## i.e. join the sets such that there is only one "line"
        ## from start to finish
            firmdict[firstnodefromdest][0] = lastnodefromsource #O(1)
        ## Remove the start node of the destination from start nodes
        ## as it now has a previous node, and is not a start.
            setOfStartNodes.remove(firstnodefromdest) #O(n)

    return (ReturnClusters(firmdict, setOfStartNodes)) #O(n) as each firm is handled once
    

    