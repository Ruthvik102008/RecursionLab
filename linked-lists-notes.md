# Linked lists: let each node handle one item

Your five-video set starts with tuples and container type hints. Those prepare the empty representation and recursive contract used by the linked-list lessons. These notes and new practice problems follow that sequence.

[1. Tuples](#tuples) · [2. Container hints](#container-hints) · [3. Linked lists](#links) · [4. Processing](#processing) · [5. Map and filter](#mapping)

| Your video | Useful moments | Practice |
| --- | --- | --- |
| [Tuples](https://www.youtube.com/watch?v=LbqHl278hcQ) | 0:21 sequences · 1:29 dictionary keys · 1:58 empty/singleton · 2:21 multiple assignment | 1–4 |
| [Container Type Hints](https://www.youtube.com/watch?v=qD9Ov87O7D8) | 0:08 list items · 0:45 dictionaries · 1:03 tuples · 1:48 recursive nesting | 5–8 |
| [Linked Lists](https://www.youtube.com/watch?v=7JNuEvE4M7Y) | 0:22 first/rest · 0:50 empty tuple · 2:42 Link dataclass · 4:38 access · 5:05 prepend | 9–12 |
| [Linked List Processing](https://www.youtube.com/watch?v=IqVO5QR8bBY) | 0:04 empty guards · 1:30 indexing · 4:23 building · 5:51 extension · 7:26 sum · 9:25 range | 13–16 |
| [Example: Linked List Comprehension](https://www.youtube.com/watch?v=IlnVbhKxWBw) | 0:12 filter/map pipeline · 2:10 mapping · 3:28 filtered rest · 4:49 composition | 17–20 |

<a id="tuples"></a>

## 1. Tuples bundle values

```python
pair = (7, 'north')
pair[0]                          # 7
pair[1:]                         # ('north',)
empty = ()
one = (7,)                       # a tuple
grouped = (7)                    # just the integer 7
```

The comma makes a tuple. A function that appears to “return two values” actually returns one tuple containing two elements. Multiple assignment unpacks that tuple.

```python
left, right = 4, 9
left, right = right, left
# The right side was (9, 4) before either name changed.
# Now left is 9 and right is 4.
```

Tuples are immutable at the level of their slots. A tuple can still contain a mutable list, so immutability does not imply that every object reachable inside it is immutable. A tuple of integers can be a dictionary key, while a tuple containing a list cannot because the list is unhashable.

**Self-check: does ([]) make an empty tuple?**

No. It groups an empty list expression. () is the empty tuple; ([],) is a one-element tuple containing an empty list.

<a id="container-hints"></a>

## 2. Describe what is inside

| Hint | Meaning |
| --- | --- |
| `list[int]` | A list of integers; no particular length |
| `list[list[int]]` | A list whose direct items are lists of integers |
| `dict[str, list[int]]` | String keys, integer-list values |
| `tuple[str, int]` | Exactly two positions: text, then integer |
| `tuple[int, ...]` | Any number of integer positions |
| `tuple[()]` | The empty tuple |

A fixed number of nested list annotations cannot describe arbitrary depth. A recursive alias refers back to itself:

```python
# Python 3.12+:
type Nested = int | list[Nested]
example: Nested = [8, [4, [], [2]]]
```

Read it as “an integer, or a list of more values following this same rule.” The recursion belongs to the description; the example remains an ordinary runtime list. An annotation alone does not inspect the contents or reject a string hidden inside. Practice 8 separately asks you to implement that inspection.

**Self-check: does list[int | list] forbid ['wrong'] deep inside?**

No. Bare list permits unspecified contents. To constrain every depth, the element rule must refer to the same recursive rule again.

<a id="links"></a>

## 3. A linked list is empty or first plus rest

In these lessons a nonempty linked list is a `Link` instance. The empty linked list is `()`. Each Link stores one item in `first`, and another *whole linked list* in `rest`.

```python
from dataclasses import dataclass

@dataclass
class Link[T]:
    first: T
    rest: 'Link[T] | tuple[()]' = ()

s = Link(8, Link(4, Link(2)))
s.first                          # 8
s.rest.first                     # 4
s.rest.rest.first                # 2
s.rest.rest.rest                 # ()
```

| Object | first | rest represents |
| --- | --- | --- |
| s | 8 | The sequence 4, 2 |
| s.rest | 4 | The sequence 2 |
| s.rest.rest | 2 | Empty |

The default rest lets `Link(2)` end a chain. A conceptual alias is `type LinkedList[T] = Link[T] | tuple[()]`; a Link is always nonempty, while a LinkedList may be empty. The scaffold uses the equivalent direct union inside a quoted forward reference.

`Link(6, s)` creates one new head and shares the existing s as its tail. It does not copy s. Rest should be a Link or (), rather than a number, an ordinary list, or None. The annotations alone do not enforce this invariant.

**Self-check: in Link(8, Link(4)), is the rest 4?**

No. The rest is the whole one-item linked list Link(4). Its first is 4, and its rest is ().

The editor supplies the Link class and a to_list display helper. Use to_list only in your tests/custom inputs. Each exercise starts independently, so needed helpers must be in that editor.

<a id="processing"></a>

## 4. Give the smaller call a precise job

A useful worked example is counting nodes. It counts neither item values nor function calls: it counts one node per Link.

```python
def length_link(s):
    if not isinstance(s, Link):
        return 0
    return 1 + length_link(s.rest)
```

| Call | Responsibility | Return |
| --- | --- | --- |
| length_link(()) | Count no nodes | 0 |
| length_link(Link(2)) | Current node plus empty tail | 1 + 0 = 1 |
| length_link(Link(4, Link(2))) | Current node plus the whole tail | 1 + 1 = 2 |
| length_link(s) | Current node plus the whole tail | 1 + 2 = 3 |

The smaller call has already counted *every* node in rest. The parent adds only its own one node, matching the “each call counts itself” reasoning from your recursion practice. A numeric sum has a different contribution: add the current value rather than 1.

Check emptiness before reading first/rest. The empty tuple has neither attribute. A loop can instead use a local cursor: advancing with `cursor = cursor.rest` changes a local name, while `cursor.rest = ...` mutates the chain.

### Returning a new linked list

When the result is a chain, an empty result is (), and a nonempty result needs a Link. The recursive result can be its rest. For extension, once the first input ends, the second input already is the required final suffix.

For an ascending range 4 through 6, the eventual structure is `Link(4, Link(5, Link(6)))`. Python must evaluate the inner rest before constructing its outer head. Recursive calls descend from 4 to 5 to 6, but the nodes are constructed as those calls return: 6, then 5, then 4. Iteratively prepending 4, then 5, then 6 would reverse the result.

**Self-check: should every base case return zero?**

No. A count or sum may need zero; a chain builder needs (); a search may need False or a fallback; an extension may need the second input. Choose the identity/result required by the contract.

<a id="mapping"></a>

## 5. Filter selects; map transforms

Think of three separate stages on the sequence -3, 2, 5:

| Stage | Items | Job |
| --- | --- | --- |
| Input | -3, 2, 5 | Visit original values |
| Keep odd items | -3, 5 | Selection |
| Square survivors | 9, 25 | Transformation |

Mapping returns one output item for every input item. Filtering returns zero or one output item for each input item. Both must return linked lists, including () for empty results.

For a filter call, give the processed rest a name. If the current item passes, place it in front of that filtered rest; if it fails, return that filtered rest directly. Returning the original rest would allow rejected tail items back into the result.

Test the predicate on the current *item*, not on rest. If the predicate expects an integer, giving it a Link is a type mismatch. Also distinguish a predicate’s True/False result from the item that passed it: the filter keeps the original item.

Practice 19 asks you to combine your own map/filter implementations. Practice 20 transfers the idea to one traversal, with a transform that may fail on rejected values. Selection must happen before transformation for each value. Here, only output order is prescribed; no side-effect call order is required.

**Self-check: why can “transform everything, then filter” fail?**

If you only want reciprocals of nonzero numbers, transforming zero first raises an error. Even when transformations are safe, a predicate on transformed values may express a different selection rule.

Before coding, say what the function returns: a number, an item, a truth value, or a linked list. Then make every branch return that kind of result.
