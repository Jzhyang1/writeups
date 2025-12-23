### Notes on things to do
* ~~Create ORCID/do linkedin etc~~
* ~~Meet with Saurabh tomorrow 10 am (Done today at 7:30pm)~~
    * Prepare some project ideas by tomorrow
    * Discuss project proposal (ideas + scoping): Send to Jane and CC Hollie
    * ~~Finalize recurring meetings~~
* Expect Slack invitation by next Thursday
* ~~Get access to Cloudlab: ldos-UT~~
* Review LDOS Slides schedules
* door code: 7635#

### Random ideas
1. Generate a shallow NN and force it to produce a policy
2. Use that to train a VAE to generate a latent space that somehow enforces the policy is functional
3. Use the VAE to generate further policies that are learned/traversed during training/live
4. Consider diffusion conditioning

1. Expressing a program's intent as syscalls with special language

### Questions
* What expresses/characterizes a "policy" (Generalized framework)

### Notes while reading
* High level: they created a "runtime library" where you can simply register handlers and call functions to handle cache policies. **Plus**: more dynamic policies lead to more cache hits. **Minus**: more overhead per page operation
* They design an eBPF framework, not stuff running on it
* ~~Is developer customization a syscall? What are the args?~~
* ~~How does the framework address interference between policies?~~
    * ~~Limit the eviction policy to within cgroups - follow up: how does kernel balance the allocations/evictions between cgroups~~
* What is insufficient about LRU for multi-core applications?
    * Range scans are because the newly read pages won't be re-read but the old data that they page out might
* What is `sched_ext`?
* Would including predefined policies be faster?
* Would using memory space to encode desired replacement behavior be better for security and speed? (anything allocated in range A is LRU, B is MRU, C is dynamic, etc? Maybe with syscalls to set the types of each)
* Why should accessing a page in another cgroup's allocation update its position in the list (is it simply because it is easier to track than not track using the 'dirty' bit)?
    * What if one cgroup has a lot of pages frequently accessed by other cgroups but not itself?
    * They mention that a critical page could be managed by another `cgroup` but the situation is "probably rare" - maybe we should test this?
* Limitations: they focus on `read` over `mmap` and focus on the singular page-size allocations in their workflows - very rare for non-page allocations
* ~~The user-defined policy function is also run on every access to a page!? Maybe it's run each PageTable scan by kernel every few preemptions for pages with the accessed bit(?)~~
* Why only linked lists? It wouldn't be hard to add an additional pointer and obtain a binary tree by introducing list_add_to_left and list_add_to_right (can be used to impl heaps and stuff, tree-pLRU is an example) - Maybe BPF limitation(?)
* How do they have bpf_map insert/update/remove implemented efficiently here?
* How little is "minimal overhead" of the pointer security check?
* For the misbehaving kernels section: why would a kernel ask for 10 pages to be evicted at once? Can the return of `cache_ext` also suggest pages to page-in? How to ensure that other resources (not folios) are cleaned up? Does `cache_ext` ever forcibly remove misbehaving policies like `sched_ext`?
* Overhead of `kfuncs` checks (they wouldn't have to be done if using kernel-provided policies)?
* Why not implement more things with the built-in FIFO struct when possible (i.e. use case can be approximated by it)? - Maybe they do that already but few cases actually are well-approximated by the FIFO struct semantics
* How does moving to the end of the small queue in S3 prevent it from being considered until removed? Does it go from:
    * (A)-B-C-(D) where (X) is pointed to by head and tail to
    * (B)-C-(D)-A? or
    * (B)-C-D-(A)?
    * If it is the second, how does that help? If it is the first, why keep it in the list?
* LHD approximation performance compared to normal floating-point LHD?
* How does a process get assign to GET or SCAN?
* Can SMT greatly impact performance?
* added maps: {memaddr:exists}, {threadId:memAccessType}
---
* Need to look more in-depth at how the current API works (try using it first)
* How are `struct_ops` and `kfuncs` created and loaded into the kernel?
* Pointers seem like the most direct analog of PIDs (comparing memory to processes)
---
* Focuses of OS functionality: security against user defined policies + efficiency
* eBPF is interesting. How does it do verification and can that be used on the user-space program in general for understanding other parts of it e.g. file or memory access patterns?
* (1) Shows that choosing the good replacement strategy is good
---
* S3-FIFO has 3 FIFOs: Main (active), Small (inactive), and Ghost; it is suitable for key-value stores. It does quick eviction of 1-hit wonders
* CLOCK PRO has 2 hands for hot and cold; it is suitable for general workloads
* Multi-Generational LRU (MGLRU): Stores *generations* (recency) and *tiers* (frequency) that then informs eviction by least recent first. Uses special PID controller
* Least Hit Density (LHD): Conditional Probabilities given by hit density * runtime adjusted parameter
