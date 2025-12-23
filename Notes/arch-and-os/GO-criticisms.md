## Random GO PL things


### Exceptions
if we always have the code

```
x, err = foo()
if err != nil {
    return nil, err
}
```

Then we occupy a space in the branch prediction table with each layer of error handling, so this is a bad idea (exceptions are better)

If a goroutine panics, the behavior is poorly defined so we want to pass errors of coroutines through other ways.

### Cleanup

`defer` is like a destructor except it is function-level instead of scope-level, which isn't very intuitive

### Concurrency

Split stack: a linked list of stacks that we traverse through when the stack grows too large(?). Usually the first slice of the stack is small enough and does well

### Guarded Command

```
select {
    case x <- ch1
    case y <- ch2
}
```
Only runs one of these when it can and blocks if nothing can run