# Iterators: remember where you are, ask for what comes next

 

You already know how to process a list. An iterator adds a position: it remembers which values have been used and which value comes next. These six lessons explain that position, how loops move it, and how lazy built-ins produce values only when requested. The examples below are independent unless a later line continues the same example.

 

[1. Position](#iterator-position)[2. Dictionaries](#iterator-dictionaries)[3. Loops](#iterator-loops)[4. Lazy built-ins](#iterator-lazy)[5. Zip](#iterator-zip)[6. Shared streams](#iterator-sharing) 

 | Your video | What to understand 

 | [Iterators](https://www.youtube.com/watch?v=On-kFyFp8HY) | iter, next, independent positions, remaining values, StopIteration 

 | [Dictionary Iteration](https://www.youtube.com/watch?v=EU_IQkOgkNM) | Keys, values, items, insertion order, live views, mutation hazards 

 | [For Statements](https://www.youtube.com/watch?v=dA5NC8WvNIM) | Reusable containers versus a consumed iterator 

 | [Built-in Iterator Functions](https://www.youtube.com/watch?v=bYtkZGU4h_E) | Lazy map, filter, reversed, and materializing results 

 | [Zip](https://www.youtube.com/watch?v=8fqSlBUHFkI) | Co-indexed tuples, shortest input, comparing sequences 

 | [Using Iterators](https://www.youtube.com/watch?v=p0acHiRp44M) | Passing one current position between cooperating functions 

## 1. An iterable supplies an iterator; an iterator supplies the next value

 

An iterable is something you can pass to `iter`, such as a list, tuple, string, range, or dictionary. An iterator is an object you can pass to `next`. Picture a bookmark: calling next returns the bookmarked value and advances the bookmark. It does not remove the value from the original list.

 

```python
numbers = [6, 9, 12]
it = iter(numbers)
next(it)                  # 6
next(it)                  # 9
numbers                   # [6, 9, 12]
list(it)                  # [12]
list(it)                  # []
```

 

`list(it)` asks for every remaining value. It consumes the iterator as it builds a new list. Calling it a second time gives an empty list because the bookmark is already at the end. To start again, create a new iterator from the original reusable container.

 

Calling `next` after the end raises `StopIteration`. That is the standard end signal, not a special value such as 0 or None: either of those could be a legitimate item. `next(it, default)` is a useful explicit form that returns the supplied default instead of raising when exhausted. Choose a default that cannot be confused with an allowed item.

 

```python
empty = iter([])
next(empty, 'finished')    # 'finished'
next(empty, 'finished')    # 'finished'
```

 

A list is iterable but is not itself an iterator: `next(numbers)` raises TypeError. First call `iter(numbers)`. An iterator is also iterable, but calling `iter(it)` returns the same iterator; it does not rewind or copy its position.

 

```python
values = [10, 20, 30]
a = iter(values)
b = iter(values)           # independent bookmark
alias = a                  # same bookmark as a
next(a)                    # 10
next(alias)                # 20
next(b)                    # 10
iter(a) is a               # True
list(a)                    # [30]
```

 

Self-check: does next flatten a nested list?

No. It returns one top-level item. If the next item is a list, that whole list is returned. Iterating over its contents would require a separate iteration.

 

Track the object and its position separately: two names can share one iterator; two calls to iter on a list create independent iterators.

 

## 2. Dictionary views choose which information you visit

 

Iterating over a dictionary directly visits its keys. `d.keys()`, `d.values()`, and `d.items()` provide iterable views of keys, values, or key/value tuples. A view is not a copied list. Calling iter on a view gives an iterator with its own position.

 

```python
stock = {'tea': 4, 'rice': 8}
list(stock)                # ['tea', 'rice']
list(stock.values())       # [4, 8]
list(stock.items())        # [('tea', 4), ('rice', 8)]
for name, amount in stock.items():
    print(name, amount)
# tea 4
# rice 8
```

 

The two variables unpack each pair: name receives the key and amount receives its associated value. It is one loop, not a loop over all possible key/value combinations. You may instead loop over keys and read `stock[name]`, just as in your earlier dictionary comprehensions.

 

In this workbook's Python 3.12, dictionary order is insertion order. Assigning a new value to an existing key keeps its position; adding a new key puts it at the end. The video's historical comment about older Python versions does not change this workbook's rule. Insertion order became a language guarantee in Python 3.7.

 

```python
prices = {'lamp': 11, 'mat': 7}
view = prices.values()
prices['lamp'] = 13
list(view)                 # [13, 7]
prices['cup'] = 3
list(prices)               # ['lamp', 'mat', 'cup']
```

 

A view reflects its dictionary's current contents. Updating an existing key's value is different from adding or deleting a key. Changing dictionary size while using an existing iterator can raise RuntimeError. Do not build a solution that relies on continuing such an iterator. If keys must be added or removed, first make a snapshot with `list(d)`, then loop over that separate list.

 

Self-check: is list(d.values()) still a live view?

No. It is a newly built list containing the values encountered during consumption. Later dictionary assignments do not replace entries in that list. Mutable objects stored as values can still be shared; materialization is not a deep copy.

 

## 3. A for loop advances an iterator too

 

A for loop obtains an iterator and repeatedly requests its next value until exhaustion. Python handles the StopIteration signal for you. A reusable container supplies a fresh iterator for a later loop; an iterator supplies itself, so a later loop begins at its current position.

 

```python
span = range(2, 5)
list(span)                 # [2, 3, 4]
list(span)                 # [2, 3, 4]
cursor = iter(span)
next(cursor)               # 2
for value in cursor:
    print(value)
# 3
# 4
list(cursor)               # []
```

 

Stopping a loop early leaves the rest available. This is useful when a function should consume only a prefix. Returning from inside a loop ends that function immediately; it does not secretly finish consuming the iterator.

 

```python
cursor = iter([4, 8, 15, 16])
for value in cursor:
    if value == 8:
        break
next(cursor)               # 15
```

 

Notice that 8 was consumed before the loop tested it. Finding a matching value normally consumes that matching value too. A correct return value is only half the contract when the caller also needs the iterator's remaining suffix.

 

Self-check: can if cursor tell whether another item exists?

No. Iterator truthiness does not generally report exhaustion. Use a for loop, next with an appropriate default, or an explicitly taught exception-handling pattern. Do not use list(cursor) merely to check: that consumes everything.

 

## 4. Lazy built-ins delay the work

 

`map(function, source)` returns an iterator of transformed values. `filter(predicate, source)` returns an iterator of original values for which the predicate is true. Creating either pipeline does not run the mapping or filtering callbacks on all its elements. The work happens when a consumer requests results.

 

```python
def announce(x):
    print('using', x)
    return x + 10

mapped = map(announce, [1, 4, 7])  # prints nothing
next(mapped)
# using 1
# 11
list(mapped)
# using 4
# using 7
# [14, 17]
```

 

In this interactive transcript, the last number or list is the expression's returned value; lines beginning with “using” were printed by the callback. A script needs print around an expression to display its return value.

 

One output request may consume several inputs. A filter has to inspect and reject items until it finds its next match. Chaining a filter after a map preserves that on-demand behavior.

 

```python
source = iter([2, 3, 5, 8])
adjusted = map(lambda x: x + 1, source)
selected = filter(lambda x: x % 2 == 0, adjusted)
next(selected)             # 4: consumes 2 (reject 3), then 3 (keep 4)
next(source)               # 5: the pipeline has not touched it yet
list(selected)             # []: 8 becomes 9 and is rejected
```

 

Normally let the pipeline be the sole consumer of its source. The explicit next(source) above demonstrates shared state: taking an item directly removes it from what the pipeline will see later.

 

`list`, `tuple`, and `sorted` consume all remaining inputs to build containers. `sum` also consumes the remainder to compute its answer. They are useful when you need the full result, but using one inside a supposedly lazy function defeats its purpose. An iterator does not promise indexing, length, or rewind.

 

Self-check: does filtering return the predicate's True values?

No. It returns source items whose predicate result is true. Filtering oddness over [4, 5, 7] produces 5 and 7, not True and True.

 

## 5. Zip pairs positions; reversed supplies reverse order

 

`zip(left, right)` returns an iterator of tuples pairing the first items, then the second items, and so on. By default it stops when the shortest input ends. It does not pad missing values or form every possible pair. More than two inputs produce tuples with more fields.

 

```python
pairs = zip(['p', 'q', 'r'], [6, 8])
next(pairs)                # ('p', 6)
list(pairs)                # [('q', 8)]
list(pairs)                # []
list(zip([1, 2], [3, 4], [5]))  # [(1, 3, 5)]
```

 

For reusable input lists, unmatched items remain in the lists unchanged. With input iterators, do not assume zip leaves every unpaired item untouched: it requests inputs left to right while attempting a tuple. A value from an earlier input can be consumed before a later input reports exhaustion. This matters only when the caller inspects leftover iterator state.

 

`reversed(s)` returns a reverse iterator for a suitable sequence; it does not mutate the sequence and does not itself return a list. Comparing an iterator directly with a list does not compare their produced elements.

 

```python
word = [2, 5, 2]
backward = reversed(word)
word == backward           # False
list(backward) == word     # True
list(backward)             # []
```

 

The Zip video checks palindromes by comparing co-indexed forward and backward elements. Converting both sides to lists is another option. If you materialize a reverse iterator, keep that resulting list when you need it again; a second conversion does not replay it.

 

## 6. Pass the same position between functions

 

The final video uses a dealt card deck to show why one shared iterator is useful: different parts of a program request the next card, and all continue from the same place. You do not need the card-game rules to understand the programming idea. The same design works for tickets, readings, or tasks.

 

```python
def read_pair(stream):
    return (next(stream), next(stream))

tickets = iter(['red', 'blue', 'gold', 'green', 'white'])
read_pair(tickets)         # ('red', 'blue')
read_pair(tickets)         # ('gold', 'green')
next(tickets)              # 'white'
```

 

No function needs a separate index. The iterator owns the current position, and every consumer advances that same object. It processes positions once; repeated equal values can still occur if the original source contains duplicates. Keeping a reference to the original container is different: recreating an iterator from that container starts another traversal.

 

When designing an iterator function, state its contract before coding: does it return an iterator or a container? Is the input finite? How many values may it consume? What happens at exhaustion? Should it stop immediately after finding an answer? Tests should check remaining values and callback order as well as the final result.

 

Self-check: why not convert every input to a list first?

That can eagerly consume values the caller still needs, run expensive callbacks early, and prevent bounded work on an unbounded stream. Iterator-based code can work across many representations without requiring random access.

 

An iterator is a shared, advancing position. Laziness decides when values are computed; consumption decides which positions are no longer available.

 

Sources: all six supplied videos, whose available English captions were retrieved and read. Historical ordering details are clarified using [Python 3.12 dictionaries](https://docs.python.org/3.12/library/stdtypes.html#mapping-types-dict); exhaustion defaults and zip consumption are checked against [Python 3.12 built-ins](https://docs.python.org/3.12/library/functions.html). The instructor's [Implicit Sequences](https://composingprograms.com/pages/42-implicit-sequences.html) chapter provides additional context, but its older dictionary-order examples do not describe Python 3.12. Generator definitions with yield are a separate topic and are not required in this section.

 

## Practice map

Switch to Practice above. Each task targets a different decision; the expandable hints are there when you need them.

- Trace shared and independent positions — iterators
- Take exactly n items — bounded consumption
- Stop at the first match — for consumes a stream
- Change dictionary size safely — dictionary iteration
- Return a lazy transform-and-filter pipeline — built-in iterator functions
- Zip aligned pairs — zip
- Pair forward and backward — reversed
- Two callers share one stream — using iterators
