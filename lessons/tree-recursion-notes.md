# Tree recursion, call order, and partitions

These notes follow your four unique videos. The Tree Recursion link was included twice, so it is covered once. Read the lessons below in this order: call order → inverse cascade → tree recursion → counting partitions. That order builds the harder ideas from smaller ones.

You do not need to hold every call in your head at once. At each step, ask: **What is this call responsible for, and what is it waiting for?**

## Your video map

| Video | What you will learn | Helpful timestamps |
|---|---|---|
| [Order of Recursive Calls](https://www.youtube.com/watch?v=VYYkJ1OLXBw) | Why work before and after a recursive call happens in different orders. | 0:10 waiting for a call; 0:28 cascade; 2:00 frames; 5:20 shorter implementation |
| [Example: Inverse Cascade](https://www.youtube.com/watch?v=uK3KrG8qxPg) | Build a growing pattern, print its center, then shrink it. | 0:09 target output; 0:31 helper functions; 1:00 functions as arguments; 1:52 solution explanation |
| [Tree Recursion](https://www.youtube.com/watch?v=ls0GsJyLVLw) | One call can depend on more than one smaller call. | 0:00 definition; 1:39 Fibonacci; 3:09 execution order; 6:19 tracing; 8:59 repeated work |
| [Example: Counting Partitions](https://www.youtube.com/watch?v=DvgT4dnSMVM) | Count possibilities by splitting them into non-overlapping groups. | 0:27 meaning of a partition; 2:45 two choices; 6:46 code; 7:58 base cases; 8:45 worked example |

The explanations, diagrams, and extra examples below are written for you. The coding workbook adds transfer exercises beyond the exact examples shown in the videos.

## 1. The one rule that explains call order

**When a function calls another function, it waits for that call to finish before continuing to its next statement.** Recursion follows the same rule.

Imagine each call leaving a bookmark at the line where it paused. The smaller call runs. When that call finishes, the earlier call resumes from its bookmark. This is an analogy for the call frames Python keeps.

```python
def example(n):
    print("before", n)
    if n > 0:
        example(n - 1)
    print("after", n)
```

Calling `example(2)` prints:

```text
before 2
before 1
before 0
after 0
after 1
after 2
```

Here is what the three calls are doing:

| Call | First action | What it waits for | Last action |
|---|---|---|---|
| `example(2)` | Print `before 2` | All of `example(1)` | Print `after 2` |
| `example(1)` | Print `before 1` | All of `example(0)` | Print `after 1` |
| `example(0)` | Print `before 0` | No recursive call | Print `after 0` |

The `n` in the original call is still 2 when it resumes. The smaller calls have their own local variables; they do not overwrite the original call's `n`.

### Printing and returning do different jobs

- `print(x)` displays something on the screen.
- `return x` sends a value to the caller and ends the current call.
- A function with no explicit `return` still finishes: it returns `None`.

For a printing exercise, `None` is usually the intended return value. You can produce all the correct printed lines without returning a number.

```python
def announce():
    print("hello")
```

`announce()` prints `hello` and returns `None`. `print(announce())` prints **two lines**: `hello`, then `None`. The outer `print` displays the returned value.

**Quick self-check:** In `print("A"); helper(); print("B")`, does B happen when `helper` starts or when it finishes? It happens when `helper` finishes.

## 2. Cascade: shrink, then grow

The cascade of `123` is:

```text
123
12
1
12
123
```

Think of it as three jobs: print the current number, let a smaller call print the middle, then print the current number again.

```python
def cascade(n):
    if n < 10:
        print(n)
    else:
        print(n)          # Before the smaller call.
        cascade(n // 10)  # This prints the entire middle.
        print(n)          # After the smaller call finishes.
```

For these examples, `n` is a nonnegative integer. The video describes positive inputs; treating zero as a one-digit input is a small extension used in the workbook.

`n // 10` removes the last decimal digit. For example, `123 // 10` is `12`.

### Follow just one call

To understand `cascade(123)`, temporarily trust that `cascade(12)` works:

```text
The outer call prints:       123
The smaller call prints:    12
                            1
                            12
The outer call resumes:     123
```

The outer call is responsible for only the first and last lines. This is the recursive leap of faith in a printing problem.

### Why the smallest line appears only once

The base case prints once and stops. If you print on both sides of the recursive call even in the base case, the center gets duplicated.

A shorter equivalent implementation is:

```python
def cascade(n):
    print(n)
    if n >= 10:
        cascade(n // 10)
        print(n)
```

The boundary must include **10**. It is a two-digit number, so it still needs the recursive step.

**Important distinction:** Cascade prints on both sides of a call, but each non-base invocation makes only **one recursive call**. It is not tree recursion.

## 3. Inverse cascade: grow, then shrink

An inverse cascade of `1234` prints:

```text
1
12
123
1234
123
12
1
```

Break this into three easy pieces:

| Piece | Responsibility for input 1234 |
|---|---|
| `grow(1234)` | Print `1`, `12`, `123` |
| `print(1234)` | Print the center once |
| `shrink(1234)` | Print `123`, `12`, `1` |

The helpers exclude the full input. This avoids printing the center three times.

```python
def inverse_cascade(n):
    grow(n)
    print(n)
    shrink(n)
```

### Start with plain helper functions

To print the shorter prefixes from smallest to largest, recurse **before** printing:

```python
def grow(n):
    if n >= 10:
        grow(n // 10)
        print(n // 10)
```

For `grow(1234)`, the calls reach `grow(1)`, which prints nothing. As they return, the waiting print statements display `1`, then `12`, then `123`.

To print prefixes from largest to smallest, print **before** recursing:

```python
def shrink(n):
    if n >= 10:
        print(n // 10)
        shrink(n // 10)
```

The placement of `print` changes the order even though both helpers remove one digit each time.

### Now the video's higher-order version

A higher-order function accepts a function as an argument, returns a function, or both. Here we only need the first possibility.

```python
def f_then_g(f, g, n):
    if n:
        f(n)
        g(n)
```

Read this as: **if n is nonzero, do f(n), wait for it to finish, then do g(n).** For these integer inputs, zero is false in an `if` condition.

The helper takes the function itself: `print`, not `print(n)`. Passing `print(n)` would run `print` too early and pass its returned `None` instead of a function.

With that helper, grow and shrink become:

```python
def grow(n):
    f_then_g(grow, print, n // 10)

def shrink(n):
    f_then_g(print, shrink, n // 10)
```

| Helper | First function passed | Second function passed | Result |
|---|---|---|---|
| `grow` | `grow` | `print` | Smaller prefixes finish printing first. |
| `shrink` | `print` | `shrink` | The largest remaining prefix prints first. |

The lecture uses compact lambda expressions for this idea. A lambda is just a short expression that creates a function; it does not introduce a different execution rule. The `def` versions above make the order easier to see.

If this version feels difficult, return to the plain helpers first. Once you can explain them, the higher-order version is simply packaging their two operations.

## 4. Tree recursion: one answer needs two smaller answers

In ordinary linear recursion, each call continues through at most one recursive child. In tree recursion, an invocation can make multiple recursive calls, so the work branches.

Having two call expressions in different `if` branches is not enough if only one ever executes per invocation. The branching is about the work actually performed.

### Fibonacci numbers

The sequence starts with 0 and 1. After that, each number is the sum of the two before it.

| Position n | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fibonacci number | 0 | 1 | 1 | 2 | 3 | 5 | 8 | 13 | 21 |

The input is a **position**, not a value to look up in the sequence. For example, `fib(6)` is 8.

```python
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 2) + fib(n - 1)
```

This matches the call order used in the video: `n - 2` first, then `n - 1`.

### Draw the work for a small input

```text
fib(4)
├── fib(2)
│   ├── fib(0) → 0
│   └── fib(1) → 1
│   returns 1
└── fib(3)
    ├── fib(1) → 1
    └── fib(2)
        ├── fib(0) → 0
        └── fib(1) → 1
        returns 1
    returns 2

fib(4) returns 1 + 2 = 3
```

The tree describes dependencies. It does **not** mean the branches run simultaneously.

Python evaluates the left operand of `+` first. It completely finishes `fib(2)`, then completely finishes `fib(3)`, then adds their answers.

The order in which calls **start** is:

```text
4, 2, 0, 1, 3, 1, 2, 0, 1
```

There are nine calls but the answer is three. **Number of calls** and **returned value** measure different things.

### Why naive Fibonacci becomes slow

In the tree above, `fib(2)` is computed twice. A plain function call does not automatically remember an earlier result. Larger inputs repeat many more subproblems.

For this exact implementation:

- `fib(4)` returns 3 and makes 9 total calls.
- `fib(5)` returns 5 and makes 15 total calls.
- Total work grows exponentially, while maximum active stack depth grows linearly with n.

That last distinction is supplemental: the whole tree contains all calls made over time, but only one active root-to-leaf path is on the stack at once. Completed branches are not all active together.

Remembering computed answers is called **memoization**. The video points ahead to this idea; you do not need to implement it for these exercises. Tree recursion itself is not always inefficient—repeated subproblems are the issue in this Fibonacci implementation.

Keep experimental Fibonacci inputs small, roughly 0–15, while learning to trace them.

## 5. Counting partitions: turn a difficult count into two choices

A partition of an integer is a way of writing it as a sum of positive integers, where the order does not create a new partition.

For example, `2 + 4` and `4 + 2` represent the same partition. We write the parts in nondecreasing order so duplicates are easy to recognize. Repeated parts are allowed: `2 + 2 + 2` is valid.

### What the two inputs mean

```text
count_partitions(n, m)

n = the amount still left to make
m = the largest part size you are allowed to use
```

The function returns a **count**. It does not return the actual list of partitions.

For `count_partitions(6, 4)`, all nine possibilities are:

```text
1 + 1 + 1 + 1 + 1 + 1
1 + 1 + 1 + 1 + 2
1 + 1 + 2 + 2
2 + 2 + 2
1 + 1 + 1 + 3
1 + 2 + 3
3 + 3
1 + 1 + 4
2 + 4
```

`1 + 5` is excluded because 5 is larger than the allowed maximum 4.

### Ask one yes-or-no question

**Does the partition use at least one part of size m?**

Every valid partition belongs to exactly one of these groups:

| Group | What you decide | Smaller problem |
|---|---|---|
| Use at least one m | Choose one m now; fill the remaining amount. | `count_partitions(n - m, m)` |
| Use no m | Keep the same amount; ban m from now on. | `count_partitions(n, m - 1)` |

For `(6, 4)`:

```text
All partitions of 6 with parts at most 4
├── Uses a 4: fill the remaining 2, with parts at most 4
│   1 + 1 + 4
│   2 + 4
│   → 2 ways
└── Uses no 4: fill all 6, with parts at most 3
    the other seven partitions
    → 7 ways

Total: 2 + 7 = 9
```

We add the counts because the groups cover all possibilities and do not overlap. They do not need to be equal in size.

### Difficult point: why keep m in the first branch?

Using one m does not forbid using another. For example, building 6 with parts up to 3 must allow `3 + 3`.

After choosing the first 3, there is still an amount of 3 to fill and 3 is still permitted. If you lower m in that branch, you accidentally solve a different problem: using each size at most once.

### Difficult point: why keep n in the second branch?

You have not chosen a part. You have only banned a size. The amount left to fill has not changed.

### The three stopping situations

| Situation | Meaning | Returned count |
|---|---|---:|
| `n == 0` | The choices made so far form an exact partition. | 1 |
| `n < 0` | You overshot the target. | 0 |
| `m == 0` and n is positive | No positive sizes remain. | 0 |

**Why does zero remaining return one?** There is one way to complete an already finished selection: add nothing. This is one successful completion, not an additional part of size zero.

For example, after choosing `2 + 4` to make 6, the remaining amount is zero. That branch must contribute one to the total, or the algorithm would discard a valid partition.

Check `n == 0` before checking `m == 0`. The state `(0, 0)` is still one completed selection.

### Put the reasoning into code

```python
def count_partitions(n, m):
    if n == 0:
        return 1
    if n < 0 or m == 0:
        return 0
    with_m = count_partitions(n - m, m)
    without_m = count_partitions(n, m - 1)
    return with_m + without_m
```

Use nonnegative integers for the initial n and m. Recursive calls can make n negative; the failure base case handles that deliberately.

### A complete tiny example: `(3, 2)`

```text
P(3, 2)
├── Choose a 2 → P(1, 2)
│   ├── Choose another 2 → P(-1, 2) = 0
│   └── Ban 2 → P(1, 1)
│       ├── Choose a 1 → P(0, 1) = 1
│       └── Ban 1 → P(1, 0) = 0
│       returns 1
│   returns 1
└── Ban 2 → P(3, 1)
    only ones can succeed → returns 1

Total: 2 partitions, namely 1 + 2 and 1 + 1 + 1
```

The abbreviated all-ones branch still follows the same rules; it is shortened here so the decision is easier to see.

### Why the recursion ends

In a non-base state, n and m are positive. The first branch decreases n by at least one. The second decreases m by one. So the positive quantity `n + m` decreases until a stopping case is reached. A branch that makes n negative stops immediately.

### Why it does not count different orders twice

Once a branch bans a size, it never brings it back. The decisions concern how many parts of each size to use, rather than which order to arrange them in. There is one decision path for each valid combination of part sizes.

## 6. A short guide to the common confusions

| If you are thinking… | Try this instead |
|---|---|
| “Two branches must run at the same time.” | Finish the first call completely, then begin the second. |
| “The smaller call changes my original n.” | Each invocation has its own local n. |
| “Printing the correct number is the same as returning it.” | Ask whether the caller needs a value or the viewer needs a line of output. |
| “The center of the cascade should print twice.” | A one-digit base case prints only once. |
| “A partition of zero should count as zero.” | Zero remaining means one completed choice sequence. |
| “After using m, reduce both n and m.” | Only reduce m if you intend to prohibit using that size again. |
| “Changing the order of Fibonacci's two calls changes the answer.” | The numerical sum stays the same; traces and side effects can change order. |
| “If the program is recursive, it must be slow.” | Examine how much work is repeated and how many calls are made. |

## How to use the coding workbook

1. Begin with the call-order exercises, even if they look easy. They prepare you for the later trees.
2. Write a prediction for a tiny input before running it.
3. Use **Run input** to try calls and temporary print statements.
4. Use **Test code** to run editable doctests plus the core checks.
5. When a test fails, use the hint to change one thing at a time. Remove extra debugging prints before testing a function whose output must match exactly.

For doctests, type a call after `>>>`, then its expected output below it. A function that prints multiple lines needs those lines in the same order. A function that returns `None` does not need a line saying `None` in a bare-call doctest.

```text
>>> print("first"); print("second")
first
second
```

Do not memorize the full call tree. Aim to explain one frame, one smaller problem, and why the returned or printed pieces combine correctly. Once you can do that, the tree is many repetitions of the same rule.
