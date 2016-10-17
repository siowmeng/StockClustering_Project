The complexity of the clustering algorithm as discussed above is dependent on both $n$ and $k$, where n is the number of firms, and k is the number of iterations. The number of edges/correlations, $e$, is in this case $e=n(n+1)/2$

The main loop is run k times, up to the point where k > m, at which point the algorithm is no longer able to loop through any more correlations.

A few couple of properties of the algorithm are as follows:
* After the $k$th iteration, the maximum number of firms in a cluster is min(k+1,n), as one can simply add a link to a "new" node in every iteration, starting from k=0 where all clusters are of size 1, and one can do this up until all nodes have been connected.
* After the $k$th iteration, the minimum number of clusters is max(1,n-k), which corresponds to the case above.
* After the $k$th iteration, the maximum number of clusters is between n and n-k, in fact the maximum number of clusters is n minus the maximum number that when triangled, is less than or equal to n.

For the below, we are interested in cases where k is <= m.

The complexity of the algorithm is O($n^2logn + nk$):

##George
1. Sort the edges in the graph by their weight (ie the correlation) - O($mlogm$), so O($n^2logn$)
2. Create a single-node set from each node in the graph - O($n$)
3. Repeat k times
    1. Pick the highest-weight edge - O($1$) as the list is sorted.
    2. Check whether the clusters are already in the same set - O($n$) to check whether either  the source or destination nodes are in any of the sets.
    3. Merge the sets containing the source and the destination of the edge - O(length(set1) + length(set2)) which is maximally O($n$) if you are making a union of the set of n nodes with itself.
    4. Repeat from A. with the next-highest weight edge
4. Return the remaining sets - O($1$).

##Louise
1. Sort the edges in the graph by their weight (ie the correlation) - O($mlogm$), so O($n^2logn$)
2. Create a single-node set from each node in the graph - O($n$)
3. Repeat k times
    1. Pick the highest-weight edge - O($1$) as the list is sorted.
    2. Check whether the clusters are already in the same set - O($n$) to check the top and bottom node of the source and destination - sets can be maximally n-nodes long
    3. Merge the sets containing the source and the destination of the edge - O(1)
    4. Repeat from A. with the next-highest weight edge
4. Return the remaining sets - O($n$) by looping through all start nodes and all following nodes to add them each to the set.

##Siow Meng
1. Sort the edges in the graph by their weight (ie the correlation) - O($mlogm$), so O($n^2logn$)
2. Create a single-node set from each node in the graph - O($n$)
3. Repeat k times
    1. Pick the highest-weight edge - O($1$) as the list is sorted.
    2. Merge the sets containing the source and the destination of the edge - O(length(set1) + length(set2)) which is maximally O($n$) if you are making a union of the set of n nodes with itself.
    3. Repeat from A. with the next-highest weight edge
4. Return the remaining sets - O($n^2$) by deduplicating the sets