# Containers: structure, selection, and aggregation

These five sections follow your five requested videos. The examples and exercises are written for this workbook. Work in groups of four, paying attention to the shape and type of each result.

[1. Boxes and pointers](#boxes) · [2. Slicing](#slicing) · [3. Aggregation](#aggregation) · [4. Strings](#strings) · [5. Dictionaries](#dictionaries)

| Your video | Useful moments | Practice |
| --- | --- | --- |
| [Box-and-Pointer Notation](https://www.youtube.com/watch?v=aSqOiUZg7kQ) | 0:08 closure property · 1:09 list slots · 1:52 nesting | 1–4 |
| [Slicing](https://www.youtube.com/watch?v=Y4L-4q52prk) | 0:46 slice notation · 1:17 omitted bounds · 1:55 new outer lists | 5–8 |
| [Sequence Aggregation](https://www.youtube.com/watch?v=omcBjDT6588) | 0:31 sum · 2:35 max · 3:24 key functions · 4:32 all | 9–12 |
| [Strings](https://www.youtube.com/watch?v=FvSXDUUTbgE) | 1:48 quotation styles · 2:48 escapes · 3:16 indexing · 4:03 substring membership | 13–16 |
| [Dictionaries](https://www.youtube.com/watch?v=sflkoII6Sgs) | 0:25 pairs · 1:02 lookup · 2:10 values · 4:12 key restrictions · 6:09 comprehensions · 8:10 index example | 17–20 |

<a id="boxes"></a>

## 1. Draw an object for each list

A list can contain lists, whose elements can be lists again. This “combine the results again” property lets you express a hierarchy. A drawing needs both slots and connections: a name points to an outer list, and some slots refer to inner objects.

```python
row = [6, 8]
shared = [row, row]
separate = [row[:], row[:]]
```

| Name | Outer slot 0 refers to | Outer slot 1 refers to |
| --- | --- | --- |
| shared | The original row | The same original row |
| separate | A new copy | A different new copy |

Both outer lists initially display `[[6, 8], [6, 8]]`. Equal displayed contents do not tell you whether objects are shared. `shared[0] is shared[1]` is True; the same expression for separate is False. `==` asks about equality; `is` asks about identity.

Appending 10 to row changes both displayed entries in shared because both refer to row. It changes neither copy in separate. Appending another row to shared changes only its outer structure.

**Self-check: how many outer elements are in [[[]], [1, 2]]?**

Two. Each inner list occupies one outer slot. Work one nesting level at a time.

<a id="slicing"></a>

## 2. A slice selects a range of positions

```python
s = [10, 20, 30, 40, 50]
s[1:4]                           # [20, 30, 40]
s[:2]                            # [10, 20]
s[3:]                            # [40, 50]
s[:]                             # same elements, new outer list
s[4:2]                           # []
```

The start is included and the stop is excluded. An omitted start means the beginning; an omitted stop means the end. A slice may be empty. Indexing one missing position raises IndexError, while slicing beyond an endpoint clips to what is available.

A list slice creates a new **outer list**, preserving references to inner elements. It is a shallow copy. In `rows = [[2], [9]]; copied = rows[:]`, `copied is rows` is False, but `copied[0] is rows[0]` is True. Replacing an outer slot differs from changing the inner object that slot refers to.

**Self-check: why does s[-0:] return everything?**

-0 equals 0, so the slice starts at the beginning. A function requesting the last zero items must handle that case explicitly.

Practice 5–8 checks both contents and the copy behavior requested in each prompt.

<a id="aggregation"></a>

## 3. Many values become one result

| Operation | Example | Empty input |
| --- | --- | --- |
| sum | `sum([3, 7], 20)` → 30 | Returns the start (default 0) |
| max/min | `max([3, 7])` → 7 | Raises ValueError unless an iterable-call default is supplied |
| all | Every condition is truthy | True |
| any | At least one condition is truthy | False |

Compare `all([-2, 4])`, which is True because both numbers are nonzero, with `all(x > 0 for x in [-2, 4])`, which is False. Aggregate the *condition* when the question concerns a condition.

```python
names = ['oak', 'willow', 'pine']
max(names, key=len)               # 'willow', not 6
all(len(name) >= 3 for name in names)  # True
```

A key function computes comparison scores. max returns an original item, using the first encountered item when scores tie. Concatenating lists with `sum(rows, [])` is a useful teaching example; it repeatedly copies growing intermediate lists, so it is not a good large-data flattening method.

**Self-check: why is all([]) True?**

There is no element violating the rule. By contrast, any([]) is False because there is no element satisfying it.

<a id="strings"></a>

## 4. Text is a sequence with its own rules

Single and double quotes create the same kind of string. Triple quotes can span lines. An escape such as `\n` represents one newline character. A string that looks numeric remains text until explicitly converted.

```python
message = 'sun\nrain'
len(message)                     # 8: 3 + 1 newline + 4
message[0]                       # 's': still a string
message[:3]                      # 'sun'
'un' in message                  # True: a substring
'un' in ['sun', 'rain']           # False: no whole element 'un'
float('2.75') + 1                # 3.75
```

`repr(message)` shows quote and escape notation, while `print(message)` displays the actual line break. Returning a string and printing it are different contracts. In doctests, a bare string expression displays its representation; print displays its characters without surrounding quotes.

String indexing returns a one-character string. Membership checks contiguous substrings, including the empty substring. Strings are immutable: changing a character requires constructing new text rather than assigning to `text[i]`. A string containing Python code is still data unless explicitly executed; none of these exercises needs exec.

**Self-check: is 'ct' in 'cat'?**

False. Those letters occur, but not consecutively. Membership does not ask about a scattered subsequence.

<a id="dictionaries"></a>

## 5. Keys choose values

```python
stock = {'paper': 12, 'ink': 0}
stock['paper']                   # 12
'ink' in stock                   # True, even though its value is zero
12 in stock                      # False: membership checks keys
list(stock)                      # ['paper', 'ink']
sum(stock.values())              # 12
```

A dictionary is a mapping and an iterable of keys; it is not a position-indexed sequence like a list. Its values may themselves be lists or dictionaries. Each key has one associated value. Assigning the same key again replaces that value; representing several associated items requires storing a collection as the value.

Keys must be hashable. Strings and integers work; lists and dictionaries do not. A tuple works only if its elements are hashable too. A missing bracket lookup raises KeyError. `d.get(key, fallback)` returns fallback only if the key is absent, preserving stored falsy values.

```python
lengths = {word: len(word) for word in ['elm', 'maple']}
# {'elm': 3, 'maple': 5}

# A separate list for each key:
groups = {letter: [word for word in ['elm', 'ash', 'alder']
                   if word.startswith(letter)]
          for letter in ['a', 'e', 'z']}
# {'a': ['ash', 'alder'], 'e': ['elm'], 'z': []}
```

The outer comprehension chooses the key. The inner one creates its matching-value list. Even a key with no matches gets an empty list. Dictionary iteration preserves insertion order.

**Self-check: why is d[key] or fallback a flawed lookup?**

A present value such as 0 would be replaced by fallback, and an absent key would raise an error before or could help. Check presence or use get.
