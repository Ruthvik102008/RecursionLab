# Mutation: the same object can change

 

These five lessons add a new way to model changing data. Work through one section and its four practice problems at a time. Earlier exercises banned list mutation methods because they had not been introduced; this chapter explicitly teaches them. Follow each problem’s own instructions about changing inputs, returning a value, or making a copy.

 

[1. Changing contents](#mutation-operations)[2. Tuples and inner lists](#mutation-tuples)[3. Identity and defaults](#mutation-identity)[4. Persistent state](#mutation-functions)[5. String interpolation](#mutation-strings) 

 | Your video | Main ideas | Practice 

 | [Mutation Operations](https://www.youtube.com/watch?v=qwO1AMKpKDY) | List methods, replacement, aliases, dictionaries | 1–4 

 | [Tuples are Immutable](https://www.youtube.com/watch?v=ApBGlS9ULkA) | Rebinding versus mutation; mutable elements | 5–8 

 | [Mutation](https://www.youtube.com/watch?v=WlEBqLgSk5o) | Equality, identity, shared default arguments | 9–12 

 | [Mutable Functions](https://www.youtube.com/watch?v=2puVXxcPGgA) | Captured-list state across function calls | 13–16 

 | [String Interpolation](https://www.youtube.com/watch?v=-mvyIRlGFps) | f-strings, conversion, evaluation order | 17–20 

## 1. Change contents without replacing the object

 

A list is mutable: its contents can change while names continue to refer to that same list. Assignment such as `other = supplies` creates another reference, not another list. Mutating through either name affects what both names observe.

 

```python
supplies = ['paper', 'pen']
other = supplies
supplies.append('tape')
other                          # ['paper', 'pen', 'tape']
supplies.extend(['ink', 'ruler'])
taken = supplies.pop()          # taken is 'ruler'
supplies.remove('pen')
supplies                       # ['paper', 'tape', 'ink']
```

 

`append(x)` adds one item, even when x is itself a list. `extend(seq)` adds the sequence’s individual items. Both return `None`. `pop()` removes and returns the last item; the list must be nonempty. `remove(x)` removes the first equal item and returns `None`; that value must be present. Duplicate values make “first” matter. These details agree with [Python’s list documentation](https://docs.python.org/3.12/tutorial/datastructures.html#more-on-lists).

 

Do not write `supplies = supplies.append('glue')`: the method changes the list, then assignment binds supplies to its result, None. A function can call a method on its list parameter and change the caller’s list, even without returning it.

 

Self-check: how do append([4, 5]) and extend([4, 5]) differ?

The first adds one nested list. The second adds two elements. Both mutate the receiving list; neither returns that list.

 

Practice 1–4: distinguish the object’s new contents from the method’s return value. Check an alias to see whether you actually changed the original list.

 

## 2. A fixed outer sequence can contain a changing list

 

A tuple does not support item replacement or append. Concatenation creates a tuple result; rebinding a name to that result does not modify the old tuple. The comma makes a one-element tuple: `(6,)`. Parentheses around `(6)` only group the number.

 

```python
route = ('north', 'west')
old_route = route
route = route + ('south',)
old_route                      # ('north', 'west')
route                          # ('north', 'west', 'south')

bundle = ('tools', [2, 4])
inner = bundle[1]
inner.append(6)
bundle                         # ('tools', [2, 4, 6])
```

 

The tuple still holds the same string and the same list. Only the list’s contents changed. “Immutable tuple” means its direct element references cannot be replaced; it does not freeze every object reachable inside it.

 

If a task requests independent list contents, copying only the tuple is insufficient. A slice such as `inner[:]` creates a new outer list but shares any nested mutable elements. Decide which level must be fresh, then check identity at that level.

 

Self-check: could bundle[1] = [] replace that inner list?

No: that attempts tuple item assignment. Calling bundle[1].append(...) instead changes the existing list, which is mutable.

 

Practice 5–8: separate rebinding a tuple name, mutating a list inside a tuple, and returning a genuinely new inner list.

 

## 3. Same contents and same object are different

 

```python
a = [10]
b = [10]
c = a
a == b                         # True: equal contents
a is b                         # False: distinct lists
a is c                         # True: the same list
c[0] = 12
a                              # [12]
b                              # [10]
```

 

Use `==` for contents and `is` for identity. Use lists when exploring identity; implementation choices about reusing numbers or strings are not a useful test of your understanding. A slice assignment such as `a[:] = [8, 9]` changes the existing list. Assignment `a = [8, 9]` instead changes what that one name refers to.

 

Dictionaries also mutate: `stock['ink'] = 3` either creates that entry or replaces its value. Check membership before reading a potentially absent key. Other entries and aliases remain intact.

 

```python
def remember(value, history=[]):
    history.append(value)
    return len(history)

remember('first')               # 1
remember('second')              # 2: the default list was reused
```

 

A default value is created when the function is defined, not on every call. For independent omitted inputs, use a `None` default and explicitly create a list inside the call. Test `s is None`, not merely `not s`: an explicitly supplied empty list is still a real list whose identity may matter.

 

Self-check: why does changing c affect a but not b?

a and c refer to one object. b refers to another object that initially happened to have equal contents.

 

Practice 9–12: test both contents and identity, mutate slices and dictionary entries deliberately, and avoid shared default state.

 

## 4. A returned function can remember earlier calls

 

A nested function can access a list in its parent frame. If it mutates that list, later calls see the updated contents. Calling the outer factory again creates a separate list and therefore a separate history.

 

```python
def make_switch():
    state = [False]
    def flip():
        state[0] = not state[0]
        return state[0]
    return flip

switch = make_switch()
switch()                       # True
switch()                       # False
another = make_switch()
another()                      # True: separate state
```

 

Each call gets a new local frame, but calls to the same returned function share its parent and captured list. A second name for that function shares its state too. The name state is never rebound here; its list element changes, so `nonlocal` is not required.

 

For a withdrawal or bounded counter, check the request before changing state. A rejected operation should leave the previous state available for the next valid call. One isolated call cannot show whether persistence and rejection behavior work; test a sequence.

 

Source note: captions were unavailable for the supplied Mutable Functions video. These notes use its visible withdrawal slides, including a captured one-element balance list, and the author’s [textbook discussion of local state](https://composingprograms.com/pages/24-mutable-data.html#local-state). The exercises use captured-list mutation; no nonlocal statement is required.

 

Self-check: is another = switch equivalent to another = make_switch()?

No. The first aliases the existing function and its state. The second constructs an independent function with its own list.

 

Practice 13–16: initialize state once in the factory, update it inside the returned function, and test repeated calls plus independent instances.

 

## 5. Build text from expressions

 

The final supplied video teaches f-strings. Put `f` before the quotes and expressions inside braces. Python evaluates those expressions in the current environment and inserts their string form. Without f, the braces remain ordinary text.

 

```python
distance = 12
description = f'Half the distance is {distance // 2}'
description                    # 'Half the distance is 6'
'Half the distance is {distance // 2}'  # unchanged literal text

word = 'hello'
f'{word}'                      # 'hello': str conversion
f'{repr(word)}'                # "'hello'": representation includes quotes
```

 

An f-string is a string value; returning it and printing it are separate choices. Expressions may call functions and have side effects. They evaluate left to right, so a later expression sees mutations performed by an earlier one.

 

```python
numbers = [1, 2, 3]
message = f'last: {numbers.pop()}, length: {len(numbers)}'
message                        # 'last: 3, length: 2'
numbers                        # [1, 2]
```

 

For practice, focus on exact text, spaces, expression values, and evaluation order. Advanced formatting codes and intricate quote rules are outside this lesson. See [Python’s f-string reference](https://docs.python.org/3.12/reference/lexical_analysis.html#f-strings) for optional details.

 

Self-check: why is length 2 rather than 3?

The pop call runs first and removes one item. Only then is len(numbers) evaluated.

 

Practice 17–20: combine text and calculations, distinguish str from repr, and remember that expressions inside strings execute real Python operations.
