Our goal is to improve run-time complexity

# Divide and Conquer

Given some problem with a straightforward polynomial solution, can we get it faster (e.g. poly-log or loglinear) via recurrence?

1. Divide the problem
2. recurse on a smaller problem
3. combine the results into a solution to the current problem

## Time complexity of recurrence relations

**Simplified Master Theorem**: for time complexities given by $T(n)=aT(n/b)+\Theta(n^k)$, the closed form time complexity is:

$$
\begin{align*}
&n^{\log_b(a)}&\text{ if }k<\log_b(a)\\
&n^k\log(n)&\text{ if }k=\log_b(a)\\
&n^k&\text{ if }k>\log_b(a)\\
\end{align*}
$$

**Substitution Method**: try to find $T(n)=f(n)$ with a guess for the closed form of $f(n)$ with explicit constants (e.g. $f(n)=an^2+bn$) and finding the constants in $f(n)$ to solve $T(n)=f(n)$ for all $n$.

It can also work to find $T(n)<f(n)$ and $T(n)>g(n)$ but also have $\Theta(f(n))=\Theta(g(n))$.

**Harmonic Numbers**: $\sum_{k=1}^n\frac1k=\log(n)+\Theta(1)$

## Time complexity of sorting

There are $n!$ different permutations an arbitrary array can be in. We must gain knowledge of the relative ordering of all elements in order to sort it. We can get only 2 cases with any compare operation, so we have a binary tree. Thus the height of the tree is at least $\log(n!)=\Theta(n\log n)$, or we can say comparison-based sorting is $\Omega(n\log n)$

## Amortization

Move costs around so that a sequence of operations will finish in $O(f(n))$ even when the operations themselves may have worst-case time complexities that suggest greater.

- Aggregate method
- Accounting method
- Potential method

## Examples

Famous examples:
- Merge sort
- Straussen Matrix Multiply
- $O(n)$ element selection (slower than quickselect in practice)
- Closest pair of points

### Minimum number of inversions to sort an array

**Base case**: 1 element has 0 inversions
**Divide**: split the array in half to $L,R$
**Conquer**: count number of inversions in $L,R$ independently while sorting
**Combine**: merge together $L,R$ and accumulate $|L|$ at each time an element of $R$ is chosen.