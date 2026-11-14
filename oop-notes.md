# Object-oriented programming

 

You already know that values have types and that a dataclass can hold fields. These lessons explain how an ordinary class gives its objects both information and behavior. You will practice creating instances, updating their state, keeping track of aliases, and calling methods. Work through the videos in order, then try the matching four problems before continuing.

 

 [1 · Objects and classes](#oop-v1) [2 · Defining a class](#oop-v2) [3 · Instances and aliases](#oop-v3) [4 · Calling methods](#oop-v4)   

 | Watch | Main idea | Practice  

 | [Object-Oriented Programming](https://www.youtube.com/watch?v=XdRZkeCRXs4) | Classes, instances, and object methods | 1–4 

 | [Class Statements](https://www.youtube.com/watch?v=TqDKnrR0YXc) | Initialization and instance state | 5–8 

 | [Creating Instances](https://www.youtube.com/watch?v=4XWMp1xjIEE) | Identity, attributes, and aliases | 9–12 

 | [Methods](https://www.youtube.com/watch?v=ep1IZVNFKRo) | The receiver becomes self | 13–16   

 

## 1 · A class describes behavior; an instance holds particular data

 

A class is a type of object. An instance is one particular object with that type. For example, `list` is a class, while `[4, 7]` is an instance. Many different lists share the same operations, but they do not all contain the same items. A method is an operation called on an object through a dot expression.

 

```python
numbers = list(range(3))
print(numbers)             # [0, 1, 2]
print(type(numbers) is list)  # True
numbers.append(8)
print(numbers)             # [0, 1, 2, 8]
```

 

Calling `list(...)` constructs a list instance. In `numbers.append(8)`, the object to the left of the dot is the receiver, and `append` is its method. Append adds one item to that same list. This is newly introduced material: earlier practice avoided append, but this video explicitly explains it.

 

Mutation and returning a value are separate actions. Append mutates its receiver and returns `None`. Assigning that return value to the name of your list therefore loses that name's reference to the list.

 

```python
outcome = numbers.append([5, 6])
print(outcome)             # None
print(numbers)             # [0, 1, 2, 8, [5, 6]]
```

 

The last item is one nested list. Append does not unpack it into separate items. Also, `type(numbers)` gives the class itself, rather than the string `"list"`.

 

Self-check: does append make a new list?

No. If two names refer to the same list, both observe the added item. When you need a new outer list, construct or slice a copy first. An outer copy still refers to the original nested objects.

 

Takeaway: an object's class determines its available behavior; a method call can change that particular object.

 

Practice 1–4: construct a list, identify its class, append an item, then append to a new outer copy.

  

 

## 2 · Define persistent information with self attributes

 

An ordinary class statement contains functions that become methods. Its `__init__` method initializes a newly created instance. Python supplies that instance as the first argument, conventionally named `self`. The remaining arguments come from the call that creates it.

 

```python
class Meter:
    def __init__(self, label, initial):
        self.name = label
        self.reading = initial

    def bump(self, step):
        self.reading = self.reading + step
        return self.reading

    def clear(self):
        self.reading = 0

room = Meter('Room', 10)
print(room.name)           # Room
print(room.reading)        # 10
print(room.bump(3))        # 13
print(room.reading)        # 13
```

 

`label` and `initial` are local parameter names used during initialization. `self.name` and `self.reading` are attributes stored on the instance; they remain accessible after the method finishes. The parameter name and attribute name do not have to match.

 

A local assignment such as `reading = 0` would bind a local name. Writing `self.reading = 0` changes the receiver's attribute. Remember the dot whenever you mean an object's stored state.

 

```python
cleared = room.clear()
print(cleared)             # None
print(room.reading)        # 0
```

 

Clear changes the reading but has no return statement, so its return value is None. Initializers should likewise finish without returning a non-None value. Calling `Meter(...)` gives you the new instance; it does not give you an initializer's custom result.

 

The lecture's bank-account example also uses a conditional guard: when a withdrawal is too large, it returns a message before updating the balance. Check the condition before the mutation so a rejected action leaves state unchanged.

 

Self-check: what is self when room.bump(3) runs?

It is the same instance referenced by room. The explicit argument 3 becomes step. Self is neither the class nor a newly constructed second meter.

 

Takeaway: attributes preserve an instance's state; each method can read or update that state through self.

 

Practice 5–8: initialize a badge, update a counter, define an account, and protect ticket stock against oversized requests.

  

 

## 3 · Assignment shares an object; construction creates another

 

Each call to your class creates a distinct instance. Matching attribute values do not merge those objects. Assignment to another name, however, creates an alias for the existing object. Use `is` and `is not` to ask whether two references identify the same object.

 

```python
first = Meter('Desk', 4)
second = Meter('Desk', 4)
alias = first
print(first is second)    # False
print(alias is first)     # True
alias.bump(2)
print(first.reading)      # 6
print(second.reading)     # 4
```

 

The update through alias is visible through first because both names refer to one instance. Second stays unchanged because it was constructed independently. Renaming or assigning an object does not copy it.

 

An attribute can hold another object, rather than only a number or string. Python also allows you to add an attribute after initialization. A chain of dot expressions follows those references one at a time.

 

```python
first.partner = second
print(first.partner is second)  # True
first.partner.reading = 9
print(second.reading)           # 9
print(first.reading)            # 6
```

 

Here, `first.partner` refers to second. Updating its reading changes second's reading; it does not change first's own reading. The attribute stores a reference to the object, not an independent duplicate of its current fields.

 

Self-check: how would you get independent state?

Construct another Meter and initialize its attributes with the desired values. Verify that it is not the original object. Simply assigning another name, or storing the original in an attribute, still shares the original.

 

Takeaway: follow references carefully. Different names can reach one object, while different constructor calls create independent instances.

 

Practice 9–12: create an independent pair of accounts, attach a backup reference, change its balance, and construct an independent account copy.

  

 

## 4 · A bound method call supplies self automatically

 

A method definition includes self, but an ordinary dot call does not pass it explicitly. In `first.bump(5)`, Python supplies first as self and 5 as step. That is why the definition has two parameters while the call has one explicit argument.

 

```python
print(first.bump(5))       # 11
print(first.reading)       # 11
saved_bump = first.bump
print(saved_bump(1))       # 12
```

 

The saved bound method still knows its receiver. Calling it updates first. A method call's returned value records that particular call's result; a later call may change the object's state again.

 

```python
earlier = first.bump(2)
later = alias.bump(3)
print(earlier, later)      # 14 17
print(first.reading)       # 17
```

 

First and alias are the same receiver. Both calls change it, but earlier remains the integer 14. When a task asks for results from two sequential calls, keep each returned result rather than reading the final attribute twice.

 

Self-check: should you call first.bump(first, 5)?

No. The dot call already supplies first as self. Passing first again adds an extra explicit argument. Use first.bump(5).

 

Takeaway: separate the receiver, the explicit arguments, the returned result, and the lasting state change.

 

Practice 13–16: return a method result, call methods on two possibly aliased receivers, double stored state, and transfer between two distinct accounts.

 

Source note: captions could not be exported for the Methods video. These notes use its directly inspected teaching slide and the author's [Composing Programs section on objects and methods](https://composingprograms.com/3ed/object-oriented-programming/). The other three videos had complete available transcripts. This page covers their introductory material, without requiring later object-oriented topics.
