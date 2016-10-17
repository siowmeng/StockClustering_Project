# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:25:21 2016

@author: louisefallon
"""


#%%
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