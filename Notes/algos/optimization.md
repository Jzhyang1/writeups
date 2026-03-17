Our problem is to find an optimal solution

# Greedy

We first find a "greedy choice" on each optimal partial solution ($\exists S_{opt}. S_t\subseteq S_{opt}$) that satisfies an "exchange argument" i.e. the addition of the greedy selection element can still be part of an optimal solution ($\exists S_{opt}.S_{t+1} = S_t\cup\{e_t\}\subseteq S_{opt}$).

The base case is usually a simple 1-element selection. Only "feasible solutions" i.e. partial solutions that satisfy the constraints are considered.

Think of this as induction.

### Interval Scheduling

Given tasks $0,1,...n-1$ each with start and end time $s_i, e_i$ find the largest set of tasks that doesn't overlap.

**Feasible solutions**: All sets of jobs where no set of jobs overlap

**Greedy choice**: the earliest deadline task that doesn't overlap.


#### Correctness

**Base case**: The empty set will always be a partial solution of an optimal schedule

**Exchange argument**: Assuming we have an optimal solution $S_{opt}$, Selecting the earliest deadline element $t_0$ that doesn't overlap will always be an optimal partial solution because if there exists an optimal solution $S_{opt}\cup{t_1}$ that doesn't contain $t_0$, then $t_1$ overlaps with $t_0$ otherwise $S_{opt}\cup\{t_0,t_1\}$ is more optimal; thus there exists an optimal solution $S_{opt}-\{t_1\}+\{t_0\}$ containing the same number of scheduled tasks and also containing $t_0$.

### Interval Partitioning

Given tasks $0,1,...n-1$ each with start and end time $s_i, e_i$ find the minimum set of non-overlapping schedules to schedule each task once.

**Solution**: start a new schedule when the minimum start-time task can not be scheduled into an existing schedule, otherwise put the task into any existing schedule it does not overlap with.

### SSSP all positive

Given a graph of non-negative edge weights $w(u,v)$, find the minimum distance path from a source vertex $s$ to all other vertices

**Solution (Djikstra's)**: 
- keep 2 sets $S$ and $Q$ containing all vertices that have found their minimum distance from $s$ and those who have not, respectively. Begin with all vertices in $Q$
- store the upper-bound distance from $s$ to $v$ as $d[v]$. Begin with $d[s]=0$ and $d[v\ne s]=\infty$
- Until $Q$ is empty, move the vertex $q\in Q$ with the minimum value of $d[q]$ to $S$ and update vertices $u$ adjacent to $q$ to $\min(d[u], d[q]+w(q,u))$

**Correctness**: The observation is that if all weights are non-negative, then the distance of the optimal path from $s$ to $v$ is at least as large as any sub-path. Since we considered all paths going through the vertices in $S$, we have that all vertices in $Q$ have a lower-bound distance of $\min(d[q\in Q])$, so the minimum distance of $q\in Q$ is fixed.

**Runtime**: With matrix and no priority queue, we have $O(n^2)$. With priority queue we have $O((n+m)\log n)$. With fibonacci heap we have amortized $O(m+n\log n)$. Where $n,m$ is the number of vertices and edges, respectively

### Minimum Spanning Tree

Given a weighted connected undirected graph, find a tree that uses all vertices with the minimum sum of edge weights.

**Solution (DJK/Prim's)**:
- keep 2 sets $S$ and $Q$ containing all vertices in the "built tree" and those who are not, respectively. Begin with an arbitrary vertex in $S$ and all other vertices in $Q$.
- Until $Q$ is empty, move the vertex $q\in Q$ with the minimum value of $w(s\in S, q)$ for any $s$ to $S$.

**Solution (Kruskal's)**: repeatedly take the minimum weight edge $e$ between two disconnected components and joining those disconnected components together via $e$. Implementation-wise, we traverse the edges sorted by weight and join components together with union-find.

# Dynamic Programming

Recursively solve subproblems of the same form to build up to the full solution. This is done by finding the "optimal substructure" i.e. we solve $f(t)$ by finding a few potential components of the solution at $f(t-i)$ for some $i$(s) and choose the best solutions to build $f(t)$.

There's "memoization" (caching) and bottom-up DP.

This is equivalent to strong induction whereas Greedy is normal induction.

### Weighted Interval Selection

maximize the sum of weighted tasks $0,1,...n-1$ with intervals $s_t,e_t$ such that no tasks overlap.

**Optimal substructure**: For all tasks in increasing order of end time, we consider $f(t-1),f(t-k)$ (where $t-k$ is the latest non-overlapping task to $t$) such that one of the following:

- $f(t)=f(t-k)\cup\{t\}$
- $f(t)=f(t-1)$

Depending on which one is better. Implementation-wise, we keep track of the sum of weights at $f(t)$ and choose the option that gives a larger weight.

### Knapsack

maximize the sum of values constrained by total weight $W$ given one of each item $0,1,...N-1$ with weights $w_i$ and values $v_i$.

**Optimal substructure**: We can have 1 item, 2 items, etc, and the 2-items will depend on chosing the 1-items. We also have that we shouldn't choose $i>k$ if we choose $k$ in $f(n)$ to prevent duplicates (an we will overcount if we consider both $i>k$ and $i<k$ for $f(n,k)$). Thus we have induction on 2 variables:

- $f(n,k)=f(n-1,k-1)\cup\{k\}$
- $f(n,k)=f(n-1,k-2)\cup\{k\}$
- ...
- $f(n,k)=f(n-1,n-1)\cup\{k\}$

Implementation-wise, we will fill in all $f(n,i)$ with the maximumizing value for each $i\in\{0,1,...N-1\}$ and each $n\in\{0,1,...W\}$ (only $W$ items can be gotten because of integer weights).

### All Pair Shortest Path (APSP)

Given a graph containing no negative-weight loops, find the shortest path between all pairs of points.

**Solution (Floyd-Warshall)**: DP on $d_k[u, v]$ the minimum distance between $u,v$ using only edges passing through vertices in $0,1,...k-1$.

- $d_k[i,j] = d_{k-1}[i,j]$
- $d_k[i,j] = d_{k-1}[i,k]+d_{k-1}[k,j]$

Implementation-wise, initialize all $d_0[i,j]$ to $w(i,j)$ and iterate through all $n^2$ pairs of vertices $i,j$ for each value of $k$.

This is correct because either $k$ is in the path or it isn't, and we check both cases for each $i,j$ to expand the set from $0...k-1$ to $0...k$.

### SSSP with negative

**Solution (Bellman-Ford)**: We repeat path relaxation

- $d_k[v]=d_{k-1}[v]$
- $d_k[v]=d_{k-1}[u]+w(u,v)$ for any adjacent $u$

where $k$ is the number of edges considered for the shortest path.

Implementation-wise, initialize the same as Djikstra's and run $n$ iterations of path relaxation on all vertices.

### Longest Common Subsequence

Given two strings $X,Y$, find the longest string $Z$ such that some indices of $X$ can be removed to form $Z$ and possibly different indices of $Y$ can be removed to form $Z$. 

**Solution**: Consider indicies $i,j$ for $X,Y$ respectively
- $f(i,j)=f(i-1,j-1)\cup\{X_i\}$ if $X_i=Y_j$
- One of the following otherwise:
    - $f(i,j)=f(i-1,j)$
    - $f(i,j)=f(i,j-1)$

Top-down DP is good here

### Matmul Ordering

Given matrices $0,1,...N-1$ that need to be multiplied together with dimensions $p_i\times q_i$, find the order to perform the multiplication to minimize the number of element-wise operations.

**Solution**: Consider all matrices $n\in\{i,...i+k-1\}$, we find the optimal solution to the subproblems where $k=1,...N$.
- $f(i,k)=f(i,1)+f(i+1,k-1)$
- $f(i,k)=f(i,2)+f(i+2,k-2)$
- ...
- $f(i,k)=f(i,k-1)+f(i+k-1,1)$

This boils down to filling in a pyramid or upper left triangular matrix.