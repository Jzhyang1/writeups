# Max Flow

**Given**: a graph with two designated vertices source ($s$) and sink ($t$), and associated capacities along each edge ($c(e)$), and the constraints: 

- flow values along each edge such that inflow = outflow for each vertex other than $s$ and $t$
- the flow along each edge is $0\le f(e)\le c(e)$. 

**Find**: the flow values that maximize outflow from $s$ = inflow to $t$

#### Runtime

- $O(n^3)$ for some algorithms
- $O(mf^*)$ for Ford Fulkerson

#### Ford Fulkerson

1. Choose a path $P$ from $s$ to $t$ via BFS (visit only edges not $c(e)=0$). 
2. Increase each flow $f(e\in P)$ by the minimum residual capacity ($f_c(P)$). 
3. Create a residual graph to have $c'(e\in P) = c(e) - f_c(P)$ and $c'(e^T) = c(e^T) + f_c(P)$. 
4. Repeat the process on the residual graph until no more paths can be found.

This is bounded for integer weights by $O(mf^*)$ where $m=|E|$ and $f^*$ is the actual maximum flow.

#### Max-flow Min-cut

If we create a partition/cut of the graph such that $s,t$ are not in the same set and the capacities of cut edges are minimized, then the sum of the capacities is the maximum flow.

**Proof**:
We have that the flow of the graph is equal to the net flow across the cut, thus it is less than or equal to the minimum capacity of a cut.

The entire capacity of the min cut can be filled. For contradiction, if the max flow is less than the min-cut, then we will have a residual graph in which there is some path that connects $s$ to $t$ and we can augment the flow with that path.

#### Reductions:

**Maximum bipartite matchings**: get the maximum number of pairings of vertices of a graph. We introduce new vertices $s,t$ that connect to all vertices in each of the colorings. Set all edges to capacity 1, and via Ford Fulkerson we can get $O(|E|\min(|L|,|R|))$

# Linear Programming

A more general form of constraint satisfaction where we have some set of linear equations/inequalities and an objective to maximize. 

The solution is to maximize the objective over all vertices of the convex shape created by all the constraints.

Max-flow is a special case of linear programming where the constraints are: $f(e)<c(e)$ and that the sum of $f(e)$ into and out of each vertex is 0. The objective is the sum of $f(s,u)-f(u,s)$