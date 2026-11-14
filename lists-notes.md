# Lists & sequences, one idea at a time

A list lets one name refer to several values. The next question is how to work with those values: select one, test whether one is present, visit each one, build a new list, or solve a smaller version of the same problem.

These notes follow all six of your John DeNero videos. The explanations and extra examples are written for this workbook. Practice problems include new applications beyond the videos. Read one section, try its exercises, then move on.

[1. Lists](#lists) · [2. Containers](#containers) · [3. For loops](#loops) · [4. Ranges](#ranges) · [5. Comprehensions](#comprehensions) · [6. List recursion](#recursion)

| Your video | Focus and useful moments | Practice |
| --- | --- | --- |
| [Lists](https://www.youtube.com/watch?v=-Q45UcQ2XJk) | 0:19 indexing · 1:42 expressions · 2:21 combining lists · 2:51 nested lists | 1–4 |
| [Containers](https://www.youtube.com/watch?v=TgeU-nYxdlE) | 0:21 membership · 1:30 whole elements · 2:01 nesting depth | 5–7 |
| [For Statements](https://www.youtube.com/watch?v=nMbXYJE8Xos) | 0:45 while version · 2:56 for version · 3:56 execution · 5:26 unpacking | 8–11 |
| [Ranges](https://www.youtube.com/watch?v=XPHeaItep-Y) | 0:50 endpoints · 2:03 list constructor · 2:30 one argument · 4:28 repetitions | 12–14 |
| [List Comprehensions](https://www.youtube.com/watch?v=HH8Dugs8tTc) | 0:39 transform · 1:21 filter · 2:22 combine · 2:42 divisors | 15–18 |
| [Lists, Slices, & Recursion](https://www.youtube.com/watch?v=cZGDdkfSrBQ) | 0:19 first/rest · 2:00 sum_list · 3:47 best sublist · 5:16 take/skip · 7:34 remaining limit | 19–24 |

<a id="lists"></a>

## 1. Lists: values with positions

A list literal uses square brackets. Commas separate its elements. In `scores = [12, 7, 19]`, the name `scores` refers to one list containing three numbers.

| Index (position) | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Element (value) | 12 | 7 | 19 |

`scores[1]` gives `7`. The index is an **offset from the beginning**: zero steps means the first element. `len(scores)` gives `3`, so the last valid nonnegative index is `len(scores) - 1`, which is 2.

```python
scores = [12, 7, 19]
scores[0]           # 12
scores[len(scores) - 1]  # 19
scores[3]           # IndexError: there is no fourth element
```

**An index is not the value stored there.** If `i = 1`, then `i` is 1 while `scores[i]` is 7. An empty list `[]` has length zero and no first element.

### Expressions can go inside the brackets

```python
odds = [1, 3, 5, 7]
odds[odds[3] - odds[2]]
# Work inside out:
# odds[3] - odds[2] = 7 - 5 = 2
# odds[2] = 5
```

Python first evaluates the expression producing the list, then the index expression, then selects that element. List elements can also be computed: `[2 + 3, 4 * 2]` creates `[5, 8]`. The video also shows `operator.getitem(s, i)`, which selects the same element as `s[i]`.

### Adding and multiplying lists

```python
[2, 7] + [1, 8]  # [2, 7, 1, 8]
[1, 8] * 3       # [1, 8, 1, 8, 1, 8]
[1, 8] * 0       # []
```

List `+` joins sequences; it does not add corresponding numbers. List `*` repeats the sequence; it does not multiply each number. To add a single value to a new list, wrap it: `[2, 7] + [9]`. `[2, 7] + 9` is a type error.

### A nested list is still one element

```python
rows = [[10, 20], [30, 40]]
len(rows)   # 2: two inner lists
rows[1]     # [30, 40]
rows[1][0]  # 30: first select the row, then its element
```

`[rows[1]]` is `[[30, 40]]`, a list containing one list. `rows[1]` is `[30, 40]`, a list containing two numbers. The brackets change the structure.

**Check your understanding: what is len([[], [4, 5], 9])?**

3. The outer list has three elements: an empty list, a two-element list, and a number. Length does not count everything inside nested lists.

<a id="containers"></a>

## 2. Membership: “Is this a whole element?”

A container holds values. `x in s` asks whether an element of `s` equals `x`. It returns `True` or `False`. It does not return an index or a count.

```python
digits = [1, 8, 2, 8]
8 in digits       # True, even though it occurs twice
5 not in digits   # True
'1' in digits     # False: text '1' does not equal number 1
[1, 8] in digits  # False: no element is the list [1, 8]
```

Read `in` as **“equal to one of these top-level elements”**. Do not read it as “somewhere inside all these brackets.”

| Expression | Result | Reason |
| --- | --- | --- |
| `[1, 8] in [[1, 8], 2]` | True | The first whole element matches. |
| `1 in [[1, 8], 2]` | False | The top-level elements are a list and the number 2. |
| `[1, 8] in [[[1, 8]]]` | False | The only outer element is [[1, 8]], one layer too deep. |

`x not in s` is equivalent to `not (x in s)`. To check two values, write two checks, such as `a in s and b in s`. The expression `a and b in s` does not perform both membership checks.

**Check: is [2, 3] in [1, 2, 3]?**

False. The elements are the numbers 1, 2, and 3. Consecutive elements do not automatically become one list element.

<a id="loops"></a>

## 3. For loops: visit each value

A `for` loop repeatedly binds a name to the next element and runs the indented body. That name refers to an **element**, not automatically to its index.

```python
for value in [4, 9, 2]:
    print(value)
# Prints 4, then 9, then 2 on separate lines.
```

The iterable expression is evaluated once when the loop starts. The body runs once per element unless control flow ends it early. An empty list produces zero iterations. A for statement does not create a new function call frame.

### Keep a running result

Here is a worked example: count how many temperatures are below 10.

```python
def cold_days(temperatures):
    total = 0
    for temperature in temperatures:
        if temperature < 10:
            total += 1
    return total
```

| Step for [8, 12, 5] | Condition | total afterward |
| --- | --- | --- |
| Before loop | Nothing seen yet | 0 |
| temperature = 8 | True | 1 |
| temperature = 12 | False | 1 |
| temperature = 5 | True | 2 |
| After loop | Return accumulated result | 2 |

For this numeric counter, `total += 1` means `total = total + 1`. Initialize it **before** the loop. Resetting it inside the loop would discard earlier work. Put the final return **after** the loop; a return inside would end the function during an early iteration.

### Why this is simpler than a while loop

```python
# These visit the same list elements:
i = 0
while i < len(s):
    value = s[i]
    print(value)
    i += 1

for value in s:
    print(value)
```

The for loop handles advancing through the sequence. You do not need to increment an index when the task only needs values.

### Unpacking pairs

```python
points = [[2, 5], [7, 1]]
for x, y in points:
    print(x + y)
# First iteration: x = 2, y = 5; prints 7
# Second iteration: x = 7, y = 1; prints 8
```

One outer element is unpacked on each iteration. Here each must contain exactly two values. A pair of variable names cannot unpack a three-element list without a different unpacking pattern.

**Check: what does cold_days([]) return?**

0. Initialization still runs; the loop body runs zero times; the return still runs. This is why the initial accumulator matters.

<a id="ranges"></a>

## 4. Ranges: include the start, exclude the stop

`range(start, stop)` represents increasing integers beginning with start and stopping **before** stop. It is a sequence, but it is not a list. Use `list(...)` to see its elements as a list.

```python
list(range(3, 7))   # [3, 4, 5, 6]
list(range(4))      # [0, 1, 2, 3]
list(range(-2, 2))  # [-2, -1, 0, 1]
list(range(5, 5))   # []
list(range(5, 2))   # [] with the default positive step
```

One argument means `range(0, stop)`. For the step-1 ranges in these videos, length is `max(0, stop - start)`. When an index is valid, element i equals `start + i`.

### Values, indices, and repetitions are different jobs

```python
for value in [8, 3]:
    print(value)             # 8, then 3

s = [8, 3]
for i in range(len(s)):
    print(i, s[i])           # 0 8, then 1 3

for _ in range(3):
    print('Go!')             # exactly three lines
```

The underscore is just a normal name used by convention when its value is unneeded. A range can be iterated directly; converting it to a list is not required for a loop.

If you need to include n, your stop often needs to be n + 1. If you need valid indices for s, use range(len(s)): the excluded stop is exactly the first invalid index.

**Check: how many iterations does range(2, 6) produce?**

Four: 2, 3, 4, 5. The last value is 5, but the number of values is 4. Last value and length are different quantities.

<a id="comprehensions"></a>

## 5. List comprehensions: build a new list

A comprehension describes what each output element should be. Read the `for` part first, then an optional filter, then the expression at the front.

```python
[expression for name in sequence if condition]
```

In plain English: **“For each value in the sequence, keep it if the condition passes, then compute the output expression.”** The `if` part is optional.

```python
numbers = [2, 5, 8]
[x + 10 for x in numbers]          # [12, 15, 18]
[x for x in numbers if x > 3]       # [5, 8]
[x + 10 for x in numbers if x > 3]  # [15, 18]
```

| x | Does x > 3 pass? | Output x + 10 |
| --- | --- | --- |
| 2 | No | Nothing added |
| 5 | Yes | 15 |
| 8 | Yes | 18 |

The condition uses the original x, not the transformed result. A rejected element contributes **no element**, not a zero or a None. Order and duplicates are preserved unless your expression changes the values. These examples leave the input list unchanged.

### Comprehension variable versus index

```python
letters = ['a', 'b', 'c', 'd']
[letters[i] for i in [3, 1, 1]]  # ['d', 'b', 'b']
```

Here the input sequence contains positions, so i is an index. In `[x + 1 for x in [10, 20]]`, x is a number to transform. The loop variable's role comes from the sequence you iterate over.

### Divisibility and the video's helper

`n % x == 0` means dividing n by x leaves no remainder. Do not try x = 0. The video's helper uses `[1] + [x for x in range(2, n) if n % x == 0]`. For n > 1, it lists positive divisors smaller than n. It returns `[1]` for n = 1 because 1 is inserted explicitly.

Exercise 18 uses the strict definition “positive divisors smaller than n,” so its answer for 1 is `[]`. The prompt calls out this intentional difference. Always let the function's specified contract decide boundary cases.

**Check: what is [x * 2 for x in [1, 4, 5] if x < 5]?**

[2, 8]. The filter keeps original values 1 and 4. Only then are those values doubled. It does not reject 4 because its doubled result is 8.

<a id="recursion"></a>

## 6. List recursion: first element + rest

You already learned to make a number smaller with `n - 1` or `n // 10`. For list problems, the smaller input is often the list without its first element.

```python
s = [2, 4, 1]
s[0]   # 2: one element (here, a number)
s[1:]  # [4, 1]: a list containing the rest
s      # [2, 4, 1]: unchanged

[9][1:]  # []
[][1:]   # []
# But [][0] raises IndexError.
```

A slice makes a new outer list. It does not remove anything from s. This is a shallow copy: nested elements are still shared objects, which matters later when you learn mutation. These exercises do not require changing any input list.

### Worked example: sum a list

```python
def sum_list(s):
    if s == []:
        return 0
    return s[0] + sum_list(s[1:])
```

What does one call promise? **“Give me a list, and I will return its sum.”** Trust the smaller call to fulfill exactly the same promise.

```python
sum_list([2, 4, 1])
= 2 + sum_list([4, 1])
= 2 + (4 + sum_list([1]))
= 2 + (4 + (1 + sum_list([])))
= 2 + (4 + (1 + 0))
= 7
```

The first call contributes only 2. It does not manually process 4 and 1; that is the smaller call's job. Notice the types: `s[1:]` is a list, but `sum_list(s[1:])` is a number. We add two numbers.

### When the returned result is a list

Some functions return a list instead of a number. If a smaller call returns `[6, 8]` and you want to put 4 in front, use `[4] + [6, 8]`, producing `[4, 6, 8]`. `4 + [6, 8]` is invalid. `[[4], [6, 8]]` creates a different nested structure.

Before combining results, ask: “What type does this recursive call return?” A count returns an integer; a selected sublist returns a list. Similar-looking problems can need different combining operations.

### Tree recursion: choose an item or skip it

The last video asks for the selection with the largest sum that does not exceed a limit. A “sublist” here can skip elements while preserving their order; it does not have to be one contiguous slice. Each position can be used at most once.

Suppose the input is `[4, 2, 6]` and the limit is 8. Focus only on the first item, 4:

| Choice | List still available | Limit still available | Result of this branch |
| --- | --- | --- | --- |
| Take 4 | [2, 6] | 8 − 4 = 4 | The best remaining selection is [2]; together: [4, 2], sum 6. |
| Skip 4 | [2, 6] | 8 | The best remaining selection is [2, 6], sum 8. |

Skipping 4 wins. Taking a number merely because it fits can prevent a better combination later. Tree recursion explores both choices and compares the results.

### Why the arguments change differently

 **Both branches move to the rest of the list.** You have decided what to do with this position, so it is no longer available.**Taking spends some of the limit.** Choosing 4 from a budget of 8 leaves 4.**Skipping spends nothing.** The budget stays 8.**If the first value exceeds the limit, it cannot be taken.** With positive values, adding more items cannot undo that excess. 

This is related to your partition exercises, with one crucial change: a list position is not reusable. The partition problem could keep the same allowed size after taking it. Here taking an item must still move on to the rest.

### Three related questions, three meanings

| Task | Returned value | How choices combine |
| --- | --- | --- |
| Count exact selections | Number of successful choices | Add the counts of take and skip. |
| Find the best achievable sum | A total value | Keep the larger valid total. |
| Return the best selection | A list of chosen items | Compare candidate sums, then return a candidate list. |

Do not add 1 just because a function was called. That made sense for `fib_calls`, whose job was to count calls. Here you count valid selections or optimize their value.

### Base cases follow the question

For an exact-selection count, reaching target 0 is one completed choice. An empty list with a positive target has zero choices. Because these exercises use positive values, an overshoot cannot be repaired. With repeated values, positions remain distinct: `[2, 2]` has two ways to select a total of 2.

For a best-sublist problem with a nonnegative limit, an empty available list gives `[]`. If nothing fits, `[]` is still a valid selection of sum zero. For a best-sum problem, return the number `0` instead.

There is no universal “return zeros before ones” rule. Python stops at the first return it reaches. Write conditions so that overlapping cases get the result required by the contract.

### Compare sums and decide ties explicitly

Python's comparison of two lists is not a comparison of their sums. For example, `[4, 2] > [2, 6]` is True because the first differing elements are 4 and 2, even though 6 < 8. Compare `sum(candidate)` values when the task is about totals.

The capstone makes ties deterministic: choose the skip-first candidate whenever both sums match. For `[2, 3, 5]` and limit 5, both `[2, 3]` and `[5]` reach 5; the stated rule selects `[5]`. Neither is mathematically worse, but a precise rule makes output tests consistent.

**Check: after taking 3 from [3, 7, 2] with a limit of 8, what remains?**

The available list is [7, 2] and the limit is 5. After skipping 3, the available list is still [7, 2], but the limit remains 8.

These take/skip examples can explore roughly twice as many branches each time another item is added. Slicing also copies the outer list. Use small inputs while learning; a correct naive solution can still be slow on large lists. Later techniques can reuse repeated work.

## How to use the practice

Open **Practice** and work through the 24 problems in order. Write code, press **Check work**, and use the hint to revise. Editable doctests let you add cases, while fixed core checks still verify the task. The input box lets you run one call or print intermediate values.

Before checking, predict an ordinary case, an empty or smallest case, and a case with duplicates. If a test fails, trace the smallest failing input. Your work saves in this browser on this device; each lesson set keeps its own progress.
