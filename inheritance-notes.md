# Inheritance, object-oriented design, and special methods

 

You already know how to create an instance and write a method. Now connect related classes, reuse existing behavior, and follow attribute lookup when several definitions compete. These four videos cover inheritance and design; the final, clearly marked supplement introduces a few special methods from the instructor's textbook. Run the worked examples in order: later examples use classes defined earlier.

 

[1 · Inheritance](#inheritance-basics)[2 · Design and composition](#inheritance-design)[3 · Multiple inheritance](#inheritance-multiple)[4 · Lookup practice](#inheritance-lookup)[Supplement · Special methods](#inheritance-special) 

 | Video | New idea 

 | [Inheritance](https://www.youtube.com/watch?v=Bqpe1iyq5vE) | Inherited behavior, overrides, and base-method reuse 

 | [Object-Oriented Design](https://www.youtube.com/watch?v=tULG0_WfbgU) | Composition, class-valued arguments, and coordinated objects 

 | [Multiple Inheritance](https://www.youtube.com/watch?v=rpVwO64Iqps) | Combining behavior from two related base classes 

 | [Attribute Lookup Practice](https://www.youtube.com/watch?v=qFvC4SwbG4A) | Inherited initialization, overridden methods, and object chains  

 

## 1 · Specify what changes; inherit the rest

 

`class Child(Parent):` makes Child a subclass of Parent. An inherited method is available without copying its definition. Defining the same name in Child overrides the inherited name. If Child has no initializer, lookup can find Parent's initializer. The receiver is still a Child instance.

 

```python
class Parcel:
    rate = 3
    def __init__(self, weight):
        self.weight = weight
    def quote(self):
        return self.weight * self.rate
    def add_weight(self, amount):
        self.weight += amount
        return self.weight

class CarefulParcel(Parcel):
    rate = 4
    extra_weight = 1
    def add_weight(self, amount):
        return Parcel.add_weight(self, amount + self.extra_weight)

careful = CarefulParcel(2)
print(careful.quote())          # 8
print(careful.add_weight(2))    # 5
print(careful.quote())          # 20
```

 

CarefulParcel inherits initialization and quote. Its quote uses the inherited function, but `self.rate` finds CarefulParcel's rate. The overridden add_weight adjusts the amount and reuses the original implementation. Looking up a function on the class, as in `Parcel.add_weight`, does not supply the receiver automatically: pass self explicitly.

 

For these ordinary attributes, search the instance first, then its class, then base classes. An assignment to an instance attribute does not change the class attribute. An inherited name is looked up when needed; base definitions are not copied into each subclass.

 

```python
careful.extra_weight = 0
print(careful.add_weight(1))    # 6
print(CarefulParcel.extra_weight)  # 1
Parcel.rate = 5
plain = Parcel(2)
print(plain.quote())            # 10
print(careful.quote())          # 24
```

 

Plain sees Parcel's changed rate. Careful still finds rate 4 in its own class. Prefer `self.extra_weight` over hard-coding 1: it respects both a more specialized subclass and an instance-specific override.

 

Self-check: why not call self.add_weight inside this override?

That lookup finds the same override again and recursively calls it. Calling Parcel.add_weight(self, ...) deliberately chooses the base implementation while keeping the current object as its receiver.

 

Takeaway: separate where a method is found from which object becomes self. An inherited method still works on the actual subclass instance.

  

 

## 2 · A specialized thing is-a; a manager has-a collection

 

A careful parcel is a parcel, so inheritance expresses that relationship. A depot has parcels; it is not a parcel itself. Composition stores the related objects in attributes. You used object-valued attributes before; the new design step is coordinating a collection through each object's own methods.

 

```python
class Depot:
    def __init__(self):
        self.parcels = []
    def accept(self, weight, kind=Parcel):
        package = kind(weight)
        self.parcels.append(package)
        return package
    def quotes(self):
        return [package.quote() for package in self.parcels]
    def load_all(self, amount):
        for package in self.parcels:
            package.add_weight(amount)

depot = Depot()
regular = depot.accept(2)
fragile = depot.accept(2, CarefulParcel)
print(depot.quotes())          # [10, 8]
print(depot.parcels[1] is fragile)  # True
depot.load_all(1)
print(depot.quotes())          # [15, 16]
print(len(Depot().parcels))     # 0
```

 

Classes are values, so kind can refer to Parcel or CarefulParcel. Calling `kind(weight)` constructs the chosen kind. Pass the class, not an already-created instance. Accept remembers and returns that exact new object, allowing the caller and depot to reach the same parcel.

 

The load_all loop does not need a separate type check for careful parcels. Calling each package's method selects its appropriate behavior. Similarly, the video's bank pays interest using each account's own rate and deposit method. An overridden deposit can therefore affect what happens even during interest payment.

 

Give every depot its own collection during initialization. A shared collection would incorrectly mix parcels from different depots. Avoid copying a whole base method just to change one small rule; reuse the existing implementation so future fixes remain shared.

 

Self-check: why did fragile gain two units when load_all received 1?

It is a different CarefulParcel from the earlier careful variable. Its extra_weight still comes from the class and equals 1. Its override adds the requested 1 plus that extra 1.

 

Takeaway: choose inheritance for specialization and composition for ownership. Let each contained object's methods handle its own rules.

  

 

## 3 · Combine two specializations

 

Python allows more than one base class. The video combines checking-account withdrawal behavior with savings-account deposit behavior. Both specialize the same Account base. The combined class can supply its own starting state while inheriting different methods from its two parents.

 

```python
class LabeledParcel(Parcel):
    label_fee = 2
    def quote(self):
        return Parcel.quote(self) + self.label_fee

class BundleParcel(CarefulParcel, LabeledParcel):
    def __init__(self, weight):
        self.weight = weight

bundle = BundleParcel(1)
print(bundle.quote())          # 6
print(bundle.add_weight(2))    # 4
print(bundle.quote())          # 18
```

 

In this particular diamond, the class lookup order is BundleParcel, CarefulParcel, LabeledParcel, Parcel, then object. Quote comes from LabeledParcel; add_weight comes from CarefulParcel. The shared Parcel base comes after both specializations. Do not search all the way through Parcel before considering LabeledParcel.

 

Quote eventually calls Parcel.quote on the same bundle. That base function uses `self.rate`, which finds CarefulParcel's 4. Thus the initial quote is `1 * 4 + 2`. After the extra weight is included, it is `4 * 4 + 2`.

 

Defining the combined initializer replaces inherited initialization; Python does not automatically run every parent's initializer as well. Our example explicitly sets the needed weight. The video's combined account similarly supplies its holder and special initial balance.

 

Self-check: does choosing Parcel.quote turn bundle into a Parcel?

No. It chooses a function implementation, not a replacement receiver. Self remains bundle, so instance and subclass overrides can still affect attributes read inside that function.

 

Takeaway: trace the defined lookup order for the given hierarchy. These examples require a simple diamond, not the algorithm for arbitrary multiple-inheritance graphs.

  

 

## 4 · Trace construction before following dots

 

The final video combines three levels of inheritance with objects stored inside other objects. An initializer inherited from a base class can invoke a method overridden in the actual subclass. Write down each new instance separately, then record its own attributes.

 

```python
class Seed:
    number = 9
    def choose(self, n):
        return WrappedSeed(n - 1)

class WrappedSeed(Seed):
    count = 3
    def __init__(self, n):
        if n:
            self.next = self.choose(n)
        else:
            self.next = DirectSeed(1)

class DirectSeed(WrappedSeed):
    def choose(self, n):
        return n

root = WrappedSeed(1)
root.count = 8
print(DirectSeed(2).count)       # 3
print(Seed.number == DirectSeed.number)  # True
print(root.next.next.next)      # 1
print(root.count, WrappedSeed.count)  # 8 3
```

 

Root's next is a WrappedSeed initialized with 0. That object's next is a DirectSeed initialized with 1. DirectSeed inherits the initializer, but `self.choose(1)` uses DirectSeed's override, so its next is the integer 1. Three next lookups reach that integer; another next would be an error.

 

For each dot, finish the expression on its left before searching for the name on its right. Distinguish an attribute found on the instance from one inherited through classes. Changing root.count affects root only; it does not rewrite WrappedSeed.count.

 

Self-check: why does DirectSeed(2).count return 3 rather than 2?

The initializer stores 2 as next. It does not create a count attribute. Lookup finds count in WrappedSeed, where its value is 3. Attribute names matter independently of their numerical values.

 

Takeaway: track object identity, construction, and attribute names separately. Follow one completed lookup at a time.

  

 

## Supplement · Let familiar syntax call special methods

 

The four supplied clips do not teach a special-method lesson. This short extension comes from the instructor's [Object Abstraction chapter](https://composingprograms.com/3ed/object-abstraction/), included because you requested special methods. These methods connect class behavior to built-in operations.

 

 | Operation | Method | Return

 | `repr(x)` | `__repr__(self)` | A useful representation string

 | `str(x)`, `print(x)` | `__str__(self)` | A readable string

 | `x + y` | `__add__(self, other)` | The addition result 

```python
class Milestone:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance
    def __repr__(self):
        return f'Milestone({self.name!r}, {self.distance})'
    def __str__(self):
        return self.name + ': ' + str(self.distance) + ' km'

marker = Milestone('Gate', 2)
print(str(marker))             # Gate: 2 km
print(repr(marker))            # Milestone('Gate', 2)
print([marker])                # [Milestone('Gate', 2)]
```

 

Return the string; do not print inside these methods. The f-string conversion `!r` inserts the field's repr, including appropriate quotes. Containers use their items' repr. A reconstructible representation does not automatically define equality between two instances.

 

```python
class Distance:
    def __init__(self, km):
        self.km = km
    def __add__(self, other):
        return Distance(self.km + other.km)

short = Distance(2)
long = Distance(5)
combined = short + long
print(combined.km)             # 7
print(short.km, long.km)        # 2 5
print(combined is short)       # False
```

 

This example assumes two Distance operands. Addition creates a fresh result rather than changing either input. In practice, check `isinstance(other, Distance)` first. If it is false, `return NotImplemented` lets Python try the other operand’s supported operation and ultimately raise TypeError if neither type supports the pair. NotImplemented is a special value, not an exception and not the same as NotImplementedError. The Vector practice uses this small guard; more advanced arithmetic dispatch is outside this supplement.

 

Self-check: will returning the number 7 from __str__ work?

No. Both __str__ and __repr__ must return strings. Convert numerical fields when building their text.

 

Takeaway: special methods implement behavior for existing syntax. Check exact return types as well as visible output.

  

Sources: all four supplied English transcripts were retrieved and read. Inheritance was also cross-checked against [the instructor's slides](https://cs61a.org/fa26/assets/lec/21-Inheritance.pdf). The labeled special-method supplement uses [Composing Programs](https://composingprograms.com/3ed/object-abstraction/) and [Python's data model reference](https://docs.python.org/3.12/reference/datamodel.html); it is not attributed to the four clips.

 

## Practice map

Switch to Practice above. Each task targets a different decision; the expandable hints are there when you need them.

- Inherit the behavior, change a default — inheritance
- Extend a parent method with a fee — overriding
- An inherited initializer calls your override — lookup through self
- A bank contains accounts — composition
- Combine two parents deliberately — multiple inheritance
- Two useful string representations — special methods · supplement
- Teach + to combine objects — special methods · supplement
