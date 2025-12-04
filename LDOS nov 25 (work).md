Results from random replacement policy test (delete 37.5% of data each time)?
```javascript
/* filesearch */
/* random replacement */
runtimes = [832.43, 820.00, 821.95]
/* MRU (skips top N most recently used to prevent cache pollution - provided) */
runtimes = [746.30, 798.41, 751.06]

/* YCSB */
/* random replacement */
latency = [1.575e8, 1.555e8, 1.596e8]
/* s3fifo */
latency = [1.606e8, 1.555e8, 1.545e8]
/* sampling */
latency = [1.526e8, 1.548e8, 1.535e8]
```

Turns out I made a mistake, those were all `FIFO` and not `random replacement`