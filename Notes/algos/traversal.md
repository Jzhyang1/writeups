### BFS

We assume undirected graph without disconnected components.

BFS visits each vertex once in non-decreasing order of min-distance to root.

#### Formulation
```Python
let G(V,E)
let dist[v in V] <- -1
let s in V

# to iterate through all verticies in
# increasing order of min distances to s
L <- {s}
dist[s] <- 0
while not empty(L):
    R <- {}
    for v* in L:
        for v in E[v]:
            if dist[v] == -1:
                dist[v] = dist[v*] + 1
                R.add(v)
    L <- R
```

Invariants about `while`:
1. All $v\in L$ have the same minimum distance to $s$, say $d$
2. All $v\in V$ `dist[v]` equals the minimum distance from $v$ to $s$ if `dist[v] != -1`
3. All $v\in V$ `dist[v] == -1` iff $d_v>d$
> a better formulation of combined 2 and 3: 
> `dist[v]` satisfies dichotomy
> (a) `dist[v] == -1` if $d_v>d$
> (b) `dist[v] == dv` if $d_v<=d$

Base case:
1. $L=\{s\}$, thus all $v\in L$ have $d=0$, and $d$ increases 1 between iterations
2. All values in `dist` are $-1$ except for `dist[s]` which is $0=d$
3. We know no vertex can have a distance $d_v\le0$ except for itself with $d_v=0$

Maintenence:
1. At the end of each iteration, $L=R$. There exists a path of distance $d'+1$ from any $v\in R$ to $s$ for all $d'$ equal to the distance from some $v'\in E[v]$ to $s$. Therefore the minimum distance from any $v\in R$ to $s$ satisfies $d_v\le d'+1$ for any $d'$. In the `for` loop, we add $v$ to $R$ iff `dist[v] == -1`; by invariant 3, this implies that $d_v>d$. Furthermore, since $v^*$ has an edge to $v$, $d_v\le d+1$, thus $d_v=d+1$ for all $v$ added to $R$, and in turn, all $v\in L$ will have $d:=d+1$.
2. We always set `dist[v]` at the same time as when we insert $v$ to $R$, and the value we set it to is `dist[v*]+1`. We enforce $v^*\in L$ by the outer for-loop; by invariant 1, $d_{v^*}=d$; by invariant 3, `dist[v*] != -1`; by invariant 2, `dist[v*] == d`. We've shown that $d+1$ is the minimum distance from $v$ to $s$, thus the value we set it to is correct when we do set a value.
3. Invariant 3 will have ensured `dist[v']` iff $d_{v'}>d$. We simply show that at the end of the iteration, all vertex of $d+1$ are marked with their distance. We loop through all $v\in E[v^*]$. Any $v\ne s$ with $d_v=d+1$ must have an edge between $v$ and some $v^*$ where $d_{v^*}=d$. Since we iterate through all $v^*$, we will certainly reach such $v^*$ and thus reach such $v$.

#### Properties of BFS
* Verticies reached by BFS are visited in increasing min-distance order; this is apparent through invariant 1, where d is strictly increasing
* All verticies are visited once; this is given by the termination condition since only iff there are no $v$ with distance to $s$ greater than or equal to $d$ will there be no $v$ with $d_v=d$. $L$ is empty iff there is no $d$. Invariant 3 implies there will be no nodes marked $-1$; combined with invariant 2, all $v$ will be marked with $d_v\ne d$.

#### Runtime
$L$ will contain, throughout all iterations, each $v\in V$ exactly once because invariant 1 and the fact that $v$ can only have exactly one minimum distance to $s$. We traverse through each edge from $v$ so we have runtime $\mathcal{O}(n+m)$ where $n,m=|V|,|E|$.

### DFS

Once again, assume a single connected component.

DFS visits all vertices once in reverse topological-sorted order.

An undirected DFS tree will have only forward an back edges (ancestor to descendant or vice versa) no cross edges.

**Parenthesis theorem**: a descendant of a vertex will have its preorder time and postorder time sandwiched by the ancestor's preorder and postorder time.

#### Formulation
```python
let G(V,E)
mark[v in V] <- False
let r in V

#  d[v in V]   # stores pre-order
#  f[v in V]   # stores post-order
#  i <- 0

def DFS(G,v*):
    mark[v*] <- True
    #begin preorder
    #  d[v*] <- i
    #  i <- i + 1
    #end preorder
    for v in E[v*]:
        if not mark[v]:
            DFS(G,v*)
    #begin postorder
    #  f[v*] <- i
    #  i <- i + 1
    #end postorder

DFS(G,r)  # call with root
```

#### Correctness
DFS is called on all $v\in V$ exactly once.

Proof by contradiction:
1. First, note that `mark[v] == True` iff DFS is called on $v$. Assume for contradiction there exists some $v$ that is not visited by DFS. There must be a path $v,v_{(1)},v_{(2)},...v_{(d)},r$. $v_{(1)}$ cannot be marked otherwise when checking adjacent edges, it would have seen $v$ is not visited and called DFS on $v$, the same logic can be applied to induce that $r$ cannot be marked, which forms a contradiction with the initial call on $r$.
2. No node can be visited more than once because DFS is only called when `marked[v]` is False, but once DFS is called, there are no calls to DFS before `marked[v]` is set to True, and there does not exist anywhere that `marked[v]` is set to False, thus DFS cannot be called a second time.

#### Properties of DFS

* A spanning tree can be constructed by connecting every $v$ to the parent $v*$ it is called from; there are n nodes that will be visited, and each node visited except for $r$ will have exactly 1 parent, thus we may get a directed tree, which implies an undirected tree.

These concern with directed graphs:
* **Parenthesis theorem** `d[u]<d[v]<f[v]<f[u]` iff $v$ is a descendant of $u$.
* A DAG can be sorted by DFS using decreasing `f[v]` (back-edge order) because no `f[v]` can be set unless all `f[v']` are set where `v'` is a child of `v` (See DAGs)
* A strongly connected graph can be verified in $\mathcal{O}(n)$ by checking connectivity from one vertex, then taking the transpose of the edges (reversing directions) and checking again from that vertex.
* Cut-edges are edges that when removed form multiple connected components

#### Runtime
Since the eventual effect is that every node is visited exactly once, we observe only the logic within a single iteration to achieve that effect. The for-loop goes through each edge stemming from $v$ ($\mathcal{O}(\alpha(m))$), then the logic is conditionally handed off to another DFS ($\mathcal{O}(1)$); the post-handoff logic is handled via the same analysis, thus we get $\mathcal{O}(\sum_n\alpha(m)+n)=\mathcal{O}(m+n)$.


### Cut Edges

An edge is a cut edge if it goes between two sets of vertices. In trees, this refers to an edge that is the only edge between two connected components.