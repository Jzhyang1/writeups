# Union find

- `make-set(x:any)` returns representative `repr{parent:self,value:x}`
- `link(a:repr,b:repr)` returns either `a` or `b` depending on the algorithm. WLOG say it returns `a`, then `b.parent=a`
- `union(a,b)` returns a representative that contains both `a,b`
- `find-set(a)` returns the representative of the set of `a` (traverses parent pointers)

We can make the `find-set` operation $O(\log n)$ by storing the height of every representative and make the shorter one the child when linking.

We can make the `find-set` operation $O(\log^*n)$ by performing path compression on every find, where $\log^*n$ is the inverse Ackerman function.