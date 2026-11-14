# Recursion: notes, worked examples, and a mastery practice set

Based on the transcripts of all five videos you supplied. The explanations and practice problems are written for this guide; supplemental material beyond the lectures is labeled. Code uses Python 3.

## The five lessons

| Video | Main idea | Useful review points |
|---|---|---|
| [1. Recursive Functions](https://www.youtube.com/watch?v=B2_8t2jyvX0) | Solve a problem using a smaller version of itself. | 2:37 splitting digits; 3:39 digit sum; 4:34 anatomy of recursion |
| [2. Recursion in Environment Diagrams](https://www.youtube.com/watch?v=8G7a8ANMwzQ) | Each call has its own frame and local variables. | 0:29 factorial; 2:38 return values; 4:44 frame properties; 6:19 iteration |
| [3. Verifying Recursive Functions](https://www.youtube.com/watch?v=gMEQS4kWbL4) | Verify the base case, assume a smaller call works, and justify the combination. | 0:40 verification strategy; 2:08 general principle |
| [4. Mutual Recursion](https://www.youtube.com/watch?v=IhY2cNaFktw) | Two functions can call each other to alternate behaviors. | 0:14 Luhn rule; 0:36 example; 1:50 implementation; 3:43 mutual calls |
| [5. Recursion and Iteration](https://www.youtube.com/watch?v=FVp-kv2DTxo) | State stored in loop variables can become recursive arguments. | 0:24 identifying state; 1:01 loop; 2:14 loop-to-recursion conversion |

## Before you start

You should recognize function calls, parameters, `return`, `if`, and `while`. For the integer examples, inputs are **nonnegative integers**, unless specified otherwise. This domain matters: a function can work correctly on its intended inputs and fail outside them.

Two operations make the digit examples possible:

```python
2013 // 10  # 201: remove the final decimal digit
2013 % 10   # 3: extract the final decimal digit
```

For nonnegative integers, `n == 10 * (n // 10) + n % 10`.

```python
def split(n):
    return n // 10, n % 10
```

`all_but_last, last = split(2013)` binds the names to `201` and `3`.

## 1. Recursive functions

A recursive function calls itself, directly or through another function. The key design move is to express the answer using a **smaller instance of the same problem**.

For example, the digit sum of 2013 equals the digit sum of 201 plus 3. You do not need a new algorithm for 201: it is the same problem with fewer digits.

### The three obligations

1. **Base case:** Solve an easy input directly, with no recursive call.
2. **Reduction:** Make a recursive call on a smaller problem.
3. **Combination:** Use its returned answer to solve the current problem.

“Smaller” means closer to completion. It can mean fewer digits, a shorter list, a smaller tree, or fewer steps remaining. It does not always mean a numerically smaller argument.

### Worked example: sum of digits

```python
def sum_digits(n):
    if n < 10:
        return n
    all_but_last, last = split(n)
    return sum_digits(all_but_last) + last
```

| Design question | Answer |
|---|---|
| What does the function promise? | Return the sum of the decimal digits of `n`. |
| What is immediately solvable? | A single digit, including 0. |
| What is the smaller problem? | Sum the digits of `n // 10`. |
| How do we finish? | Add the removed digit, `n % 10`. |
| Why does it stop? | Each recursive step removes one digit. |

Expansion shows what each call is waiting for:

```text
sum_digits(2013)
= sum_digits(201) + 3
= (sum_digits(20) + 1) + 3
= ((sum_digits(2) + 0) + 1) + 3
= ((2 + 0) + 1) + 3
= 6
```

There are two phases: calls move toward the base case; answers then return through the waiting calls. The expression `+ last` is pending work, performed after the smaller call returns.

### Difficult point: a recursive call is an ordinary function call

`sum_digits(201)` returns a number. Inside the larger call, you use that number exactly as you would use the result of any helper function. Recursion does not restart the whole program or erase the caller's variables.

### Common mistakes

```python
return sum_digits(n) + last       # Same problem again: no progress.
return sum_digits(n // 10)        # Drops the final digit's contribution.
sum_digits(n // 10) + n % 10      # Computes an expression but does not return it.
```

The final version implicitly returns `None` for a multi-digit input. For sufficiently deep inputs, a caller may also fail when it tries to add an integer to `None`.

The lecture connects digit sums to checksums. A checksum detects some input errors; it is not proof that the underlying information is authentic.

## 2. Recursion in environment diagrams

The factorial function is a natural recursive definition:

```text
0! = 1
n! = n × (n − 1)!    for n > 0
```

```python
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)
```

For example, `4! = 4 × 3 × 2 × 1 = 24`. The base case returns 1 because 1 is the identity for multiplication. Returning 0 would make every positive factorial result zero.

### Worked example: the complete execution of `fact(3)`

Each call creates a new frame, containing a separate local binding for `n`.

| Frame | Local `n` | What it must return |
|---|---:|---|
| f1 | 3 | `3 * fact(2)` |
| f2 | 2 | `2 * fact(1)` |
| f3 | 1 | `1 * fact(0)` |
| f4 | 0 | `1` immediately |

When f4 returns, execution resumes where f3 was waiting:

```text
f4 returns 1
f3 returns 1 × 1 = 1
f2 returns 2 × 1 = 2
f1 returns 3 × 2 = 6
```

There are **four total calls**, including the original call and the base case. Three of them were initiated by a recursive call expression.

### Difficult point: the same name can have different values

The `n` in f1 remains 3 when f2 binds its own `n` to 2. Passing `n - 1` does not assign a new value to the caller's `n`.

There is one function definition and multiple active calls to that function. You are not defining a new factorial function every time.

### Environment parent versus caller — supplemental clarification

For this function defined at the top level, each call frame's enclosing environment is the global environment. The caller is where the result returns; it is not automatically the enclosing environment used to look up names. These are different relationships.

```text
Call/return chain:  f1 → f2 → f3 → f4
Enclosing scope:   each of f1, f2, f3, f4 → global
```

### Difficult point: reaching `return` is not returning yet

In `return n * fact(n - 1)`, Python must first evaluate the whole expression. That requires waiting for `fact(n - 1)`, then multiplying, then returning.

This explains why recursive calls can be nested even when the recursive call appears on a line beginning with `return`.

### Iterative factorial

```python
def fact_iter(n):
    total, k = 1, 1
    while k <= n:
        total = total * k
        k = k + 1
    return total
```

Recursion leaves pending multiplications in call frames. Iteration explicitly maintains a running product and a counter. Both compute the same mathematical function.

For `n = 3`, the loop states `(k, total)` are `(1, 1)`, `(2, 1)`, `(3, 2)`, `(4, 6)`. It stops at the last state.

## 3. Verifying recursive functions

The lecture's “recursive leap of faith” means: reason about a smaller call using the function's promised behavior, without tracing every instruction inside it.

It is not permission to assume the entire function is correct. You assume correctness for a **smaller input**, then prove that this is enough to establish correctness for the current input.

### A reusable verification checklist

1. State the input domain and promised result.
2. Verify every base case.
3. Show that recursive calls stay within the input domain.
4. Identify a measure that decreases toward a base case.
5. Assume the smaller call returns the promised result.
6. Show that the surrounding computation produces the promised result for the current input.

Steps 3–4 make termination explicit. Correct combination alone is insufficient if the function never reaches an answer.

### Worked proof: factorial

**Contract:** For every nonnegative integer `n`, return `n!`.

**Base:** If `n == 0`, the function returns 1, which equals `0!`.

**Smaller-call assumption:** For `n > 0`, assume `fact(n - 1)` returns `(n - 1)!`.

**Combination:** The function returns `n * (n - 1)!`, which equals `n!`.

**Termination:** Each recursive step decreases the nonnegative integer `n` by 1. Eventually `n == 0`.

This is the structure of mathematical induction. Testing `fact(4) == 24` is useful, but the argument explains why the function works for every input in its domain, assuming sufficient execution resources.

### Worked proof: digit sum

For `n < 10`, the answer is `n`. Otherwise write `n = 10q + r`, with `q = n // 10` and `r = n % 10`. The digits of `n` are the digits of `q` followed by `r`.

Assume `sum_digits(q)` correctly adds the digits of `q`. Adding `r` therefore gives the digit sum of `n`. Each recursive step removes one digit, so a single-digit input is eventually reached.

### Why the domain matters

`fact(-1)` repeatedly calls `fact(-2)`, `fact(-3)`, and so on. It moves away from zero. A base case existing somewhere in the code does not imply every input can reach it.

Similarly, the digit-sum implementation returns a negative input immediately because `n < 10`. Supporting negative integers would require an explicit design decision, such as applying the function to `abs(n)`.

## 4. Mutual recursion and Luhn's algorithm

Mutual recursion occurs when functions call each other, forming a cycle such as `A → B → A`.

Luhn's algorithm is a useful example because it alternates two jobs while processing digits from right to left:

1. Keep the rightmost digit unchanged.
2. Double the next digit. If doubling produces two digits, add those two digits.
3. Continue alternating unchanged and doubled contributions.
4. Add all contributions. A number passes the Luhn checksum if the total is divisible by 10.

Here, the input includes the check digit at the far right.

### Worked example from the lecture: `138743`

| Digit, displayed left to right | 1 | 3 | 8 | 7 | 4 | 3 |
|---|---:|---:|---:|---:|---:|---:|
| Treatment, anchored at the right | Double | Keep | Double | Keep | Double | Keep |
| Contribution | 2 | 3 | 7 | 7 | 8 | 3 |

Doubling 8 gives 16; its digit sum is `1 + 6 = 7`.

The total is `2 + 3 + 7 + 7 + 8 + 3 = 30`, which is divisible by 10.

**Difficult point:** Start the alternation from the right. Starting from the left without accounting for the number of digits can choose the wrong positions.

### Give each function a precise contract

- `luhn_sum(n)`: sum the remaining digits with the rightmost one **unchanged**.
- `luhn_sum_double(n)`: sum the remaining digits with the rightmost one **doubled and reduced to its digit sum**.

```python
def luhn_sum(n):
    if n < 10:
        return n
    all_but_last, last = split(n)
    return luhn_sum_double(all_but_last) + last


def luhn_sum_double(n):
    all_but_last, last = split(n)
    luhn_digit = sum_digits(2 * last)
    if n < 10:
        return luhn_digit
    return luhn_sum(all_but_last) + luhn_digit
```

Calling the other function switches the treatment of the next digit. Both functions remove a digit before continuing. Both have a base case in this implementation.

### Trace the alternating states

Let `L` mean `luhn_sum` and `D` mean `luhn_sum_double`:

```text
L(138743) = D(13874) + 3
D(13874)  = L(1387) + 8
L(1387)   = D(138) + 7
D(138)    = L(13) + 7
L(13)     = D(1) + 3
D(1)      = 2
```

Return values then build upward: `2, 5, 12, 19, 27, 30`.

Notice that the function name carries information: it tells you whether the current last digit must be doubled. The integer argument alone does not describe the entire state.

### Verifying mutual recursion

Verify both one-digit base cases. Then assume both functions work on shorter numbers:

- `luhn_sum` adds an unchanged final digit and delegates the prefix to the doubled mode.
- `luhn_sum_double` adds a doubled/reduced final digit and delegates the prefix to the unchanged mode.

Both preserve the required alternation, and both shorten the number. This is induction on digit count, proving the two contracts together.

### Useful extensions and limitations

For a digit `d`, the doubled contribution can also be computed as:

```python
doubled = 2 * d
contribution = doubled if doubled < 10 else doubled - 9
```

Why subtract 9? For a doubled value `10 + r`, the digit sum is `1 + r = (10 + r) - 9`. For example, 18 becomes 9.

Passing Luhn means passing this checksum. It does not establish that an account exists or can be used. Luhn catches every single-digit substitution, but not every possible multi-digit mistake.

**Extension: generating a check digit.** If `p` is a prefix without its check digit, compute `s = luhn_sum(10 * p)` and choose `c = (-s) % 10`. Appending zero first puts the prefix in the correct alternating positions. For `p = 13874`, `s = 27`, so `c = 3`.

## 5. Recursion and iteration

The lecture explains loop-to-recursion conversion by identifying the state that survives between iterations. Recursive arguments can carry that state into the next call.

### Convert digit sum to a loop

What must persist?

- `n`: the digits still to process.
- `digit_sum`: the total for digits already processed.

```python
def sum_digits_iter(n):
    digit_sum = 0
    while n > 0:
        n, last = split(n)
        digit_sum = digit_sum + last
    return digit_sum
```

For `2013`:

| Point | Remaining `n` | Running `digit_sum` |
|---|---:|---:|
| Start | 2013 | 0 |
| After processing 3 | 201 | 3 |
| After processing 1 | 20 | 4 |
| After processing 0 | 2 | 4 |
| After processing 2 | 0 | 6 |

For zero, the loop executes no times and returns 0, correctly.

### The invariant explains why the loop works — supplemental

At every loop boundary:

```text
digit_sum + sum of the digits remaining in n
= sum of the digits of the original input
```

Moving the last digit out of `n` and into `digit_sum` preserves this equality. At the end, no digits remain, so `digit_sum` is the whole answer.

An invariant is a fact that remains true as the state changes. It plays a similar role for loops to the smaller-call assumption in recursive proofs.

### Convert that loop into recursion

```python
def sum_digits_rec(n, digit_sum=0):
    if n == 0:
        return digit_sum
    n, last = split(n)
    return sum_digits_rec(n, digit_sum + last)
```

```text
sum_digits_rec(2013, 0)
→ sum_digits_rec(201, 3)
→ sum_digits_rec(20, 4)
→ sum_digits_rec(2, 4)
→ sum_digits_rec(0, 6)
→ 6
```

The helper's precise contract is: return the initial accumulator plus the digit sum of `n`. Thus `sum_digits_rec(24, 10)` returns 16, not 6.

| Loop element | Recursive equivalent |
|---|---|
| Changing state variables | Parameters |
| Stop when loop condition becomes false | Base case |
| Update the state | Compute arguments for the next call |
| Repeat the loop | Call the function again |
| Return after the loop | Return in the base case |

For these nonnegative inputs, the opposite of `n > 0` is `n == 0`. Without the domain restriction, that equivalence would not hold.

### Ordinary recursion versus accumulator recursion

```python
return sum_digits(n // 10) + n % 10  # Addition waits for a return value.
return sum_digits_rec(n // 10, total + n % 10)  # Updated total is passed onward.
```

The second call is in **tail position**: its answer is returned directly with no arithmetic left to do afterward. The first has a pending addition.

**Python-specific supplement:** Python does not eliminate these recursive call frames through tail-call optimization. The accumulator version still uses increasing call-stack space and can hit the recursion limit. For long linear computations in Python, a loop is often the practical choice.

### What “iteration is a special case of recursion” means

A loop that updates a state and repeats can be expressed as a function that passes its updated state to another call. This is a statement about representing computation; it does not mean Python executes loops by secretly making recursive calls.

The reverse conversion can require identifying pending work. These digit-sum and factorial examples need simple accumulators. More complicated recursive algorithms may need an explicit stack.

### Costs — supplemental

Let `d` be the number of decimal digits. Count each arithmetic operation as one step for this introductory comparison; Python's large-integer arithmetic has additional costs.

| Implementation | Work | Maximum active function calls / extra state |
|---|---|---|
| Original recursive digit sum | O(d) steps | O(d) frames |
| Iterative digit sum | O(d) steps | Constant number of variables |
| Accumulator-recursive digit sum | O(d) steps | O(d) frames in Python |
| Recursive factorial | O(n) multiplications/calls | O(n) frames |
| Iterative factorial | O(n) multiplications | Constant number of variables |

“Constant number of variables” does not imply a constant number of bytes: large integer values take more storage.

## How to design your own recursive solution

Before writing code, complete these sentences:

1. “For inputs ___, my function returns ___.”
2. “I can immediately answer the case ___.”
3. “A smaller version of the problem is ___.”
4. “If I already had that smaller answer, I would ___.”
5. “The quantity ___ decreases, so I eventually reach ___.”

Then test a base case, the smallest non-base case, an ordinary input, and a revealing edge case such as an interior zero. Use a trace to debug execution and a proof to justify the general rule.

