# Measuring efficiency: count the work, then watch how it grows

 

Two functions can return the same correct answer while doing very different amounts of work. These lessons connect ideas you already know—recursion, function attributes, dictionaries, and higher-order functions—to measuring that difference. Start with exact counts on small inputs; then ask how the work changes as inputs get larger.

 

[1. Count calls](#efficiency-count)[2. Remember answers](#efficiency-memo)[3. Reduce the work](#efficiency-power) 

 | Your video | What to understand 

 | [Measuring Efficiency](https://www.youtube.com/watch?v=DWhsOSHjY98) | Repeated Fibonacci work, counting wrappers, cumulative attributes 

 | [Memoization](https://www.youtube.com/watch?v=IB8VSP9EZQs) | Cache by argument, pure functions, wrapper order and cache hits 

 | [Exponentiation](https://www.youtube.com/watch?v=spi6J9L_01E) | Repeated squaring, timings, input growth and operation counts 

## 1. A wrapper can count function calls

 

Tree-recursive Fibonacci repeats subproblems. Computing fib(5) needs fib(3) and fib(4), and both eventually need fib(2). A small function can count calls without changing the answer:

 

```python
def count(f):
    def counted(n):
        counted.call_count += 1
        return f(n)
    counted.call_count = 0
    return counted

def fib(n):
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)

fib = count(fib)
fib(5)                    # 5
fib.call_count            # 15
fib(5)                    # 5
fib.call_count            # 30
```

 

`count` receives a function and returns another function. The returned wrapper increments its own attribute, then calls the original f and returns its result. Functions are objects too, so they can hold an attribute such as call_count.

 

The count is cumulative: it does not automatically reset between experiments. Set `fib.call_count = 0` before measuring a fresh total, or subtract the earlier count afterward. The count includes the top-level call and base-case calls.

 

The reassignment matters. Inside the original fib body, recursive calls look up the name fib when they run. After `fib = count(fib)`, that name refers to the wrapper, so recursive calls pass through it too. Merely assigning `measured = count(fib)` while leaving fib unchanged would count the outer measured call but not recursive calls through fib.

 

Self-check: would putting call_count = 0 inside counted measure a cumulative total?

No. It would reset the attribute every time the wrapper is entered, including during recursion. Initialize once when building the wrapper, outside its body.

 

## 2. Memoization reuses answers to repeated arguments

 

A cache is a dictionary mapping an argument to the result already computed for it. On a cache miss, call the original function and store its answer. On a hit, return the stored answer without recomputing it.

 

```python
def memo(f):
    cache = {}
    def memoized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memoized
```

 

The cache is created once per call to memo, then retained by that returned function. Creating it inside memoized would forget previous calls. Separate calls to memo create separate caches.

 

Check whether the argument is a key, not whether the saved answer is truthy. A correct cached result might be 0, False, or an empty collection. Those still deserve cache hits. This one-argument version requires hashable arguments, such as integers; a list cannot be used directly as a dictionary key.

 

Memoization preserves the intended behavior when the answer depends only on the argument and recomputing has no side effects that callers require. Caching a function that prints, reads changing external state, or returns a mutable object can change observable behavior. In particular, repeated hits return the same cached object rather than fresh independent objects.

 

Self-check: can an argument whose answer is zero be cached?

Yes. For example, fib(0) should be stored under key 0. Membership of that key distinguishes a saved zero from an absent answer.

 

### Two counters can measure different things

 

Start with a fresh Fibonacci definition, then place one counter inside the cache and another outside it:

 

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)

computed = count(fib)
fib = count(memo(computed))
fib(5)                    # 5
fib.call_count            # 9
computed.call_count       # 6
fib(5)                    # 5
fib.call_count            # 10
computed.call_count       # 6
```

 

The path is outer counter → cache → inner counter → original function. The outer counter sees every request, including cache hits. The inner counter sees only cache misses that actually compute an answer. There are six distinct arguments from 0 through 5. A repeated fib(5) increases the request count by one but performs no new original-function computation.

 

Rebinding fib again ensures recursive requests enter the complete wrapped function, including its cache. Keeping the name computed lets you inspect the inner wrapper's attribute. Swapping wrapper order changes what a counter observes, even if the numerical result stays the same.

 

Self-check: does resetting the outer counter also empty the cache?

No. The counter attribute and the enclosed dictionary are different pieces of state. A warm-cache experiment measures something different from a fresh-cache experiment.

 

## 3. Make the problem shrink faster

 

One exponentiation strategy multiplies by b and decreases n by one. Repeated squaring takes a shortcut for even exponents: compute the half-power once, then square that answer. Here n is a nonnegative integer.

 

```python
def slow_power(b, n):
    if n == 0:
        return 1
    return b * slow_power(b, n - 1)

def fast_power(b, n):
    if n == 0:
        return 1
    if n % 2 == 0:
        half = fast_power(b, n // 2)
        return half * half
    return b * fast_power(b, n - 1)

slow_power(3, 6)           # 729
fast_power(3, 6)           # 729
fast_power(5, 0)           # 1
```

 

Store half! Writing two recursive half-power calls would repeat the very work you meant to avoid. For exponent 16, the fast call chain follows 16 → 8 → 4 → 2 → 1 → 0. The slow version visits every exponent from 16 down to 0. Odd exponents need a subtraction before another halving, explaining some jaggedness in call-count plots.

 

The important comparison is growth. Repeated subtraction needs work proportional to n. Repeated halving needs far fewer recursive steps: doubling n adds only a small number of steps. Function-call counts are a useful model, though they are not exact seconds; operations on larger integers can also cost more.

 

For actual timing, the standard-library timeit function measures repeated execution:

 

```python
from timeit import timeit
elapsed = timeit(lambda: fast_power(3, 40), number=100)
average_seconds = elapsed / 100
```

 

The lambda takes no arguments and runs the expression when called. elapsed measures all 100 executions, not one. Multiply average seconds by 1,000,000 to express the same time in microseconds. If samples contains repeated total-second measurements with the same repetition count, the fastest per-call microseconds is `min(samples) / repetitions * 1_000_000`.

 

Exact timings vary with hardware and other activity. Compare representative input sizes, repeat measurements, and keep cache conditions comparable. The video takes the fastest repeated measurement to reduce interference from unrelated work; a single unusually slow run is weak evidence.

 

Self-check: does a faster timing prove a function is correct?

No. Check equal outputs and boundary cases first. Then compare how much work or time the correct versions need as inputs grow.

 

Count what you mean to measure, distinguish cache hits from computation, and compare growth across inputs rather than memorizing one machine's stopwatch result.

 

Sources: the three supplied videos, with all available English captions retrieved and read (the exponentiation video's captions are auto-generated), plus [Python 3.12 timeit](https://docs.python.org/3.12/library/timeit.html) for measurement semantics. All deterministic code outcomes here were checked under Python 3.12. Exact time values are intentionally not prescribed.

 

## Practice map

Switch to Practice above. Each task targets a different decision; the expandable hints are there when you need them.

- Count calls without changing the result — measuring efficiency
- Remember an answer, including zero — memoization
- Measure cache lookups and actual work — wrapper order
- Power by repeated squaring — exponentiation
- Interpret repeated timing measurements — timing and growth
