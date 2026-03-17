# Decision Problems

There are functions/algorithms $f(x)\rightarrow \{0,1\}$ over some input of bits $x\in X\subseteq \{0,1\}^*$

For some "language" $L$, the set $X$ is specified.

- $f$ decides $L$ if $f(x\in L)=1$ and $f(x\not\in L)=0$.
- $f$ accepts $L$ if $f(x\in L)=1$.

Instead of outputting $0,1$ there are also programs that output other things or do not terminate.

### Undecidability

- Universal problem: $X$ is all inputs $(p,w)$ where $p(w)=1$
- Acceptance problem: $X$ is all inputs $(p,w)$ where $p(w)=1$; we also guarantee that $p(w)$ halts. We can construct $(A^C,A^C)$ where $A$ decides the Acceptance problem. This input makes it impossible for $A$ to give a non-contradictory output.
- Halting problem: $X$ is all inputs $(p,w)$ where $p$ halts on $w$

We can prove most undecidable languages via reduction i.e. if we can decide $L$ then we can decide the halting problem.

**All-halt**: Given some program, decide if it halts on all inputs. If we can decide all-halt with program $A$, then we can construct $B$ to decide halting by taking the inputs $(p,w)$ to construct program $p_w$ that ignores its input and performs $p(w)$, then deciding all-halt will be deciding the halting problem.