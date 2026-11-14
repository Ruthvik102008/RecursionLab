# Attributes: where a value belongs changes how it behaves

 

You already know how to define a class, initialize instance fields, and call a method. This chapter focuses on the next layer: a class can store its own shared attributes, an instance can hide a shared value, and Python follows a lookup rule when you use a dot. For prerequisites, revisit [Object-oriented programming](oop.html); these exercises concentrate on the new distinctions.

 

[1. Class attributes](#attributes-shared)[2. Lookup](#attributes-lookup)[3. Assignment](#attributes-assignment)[4. Functions and methods](#attributes-functions)[5. Following a dot expression](#attributes-combine) 

 | Your video | What is new here? | Read 

 | [Method Calls](https://www.youtube.com/watch?v=mimP7cNrSHA) | The receiver can be an expression; method lookup precedes the call | [Section 5](#attributes-combine) 

 | [Attribute Lookup](https://www.youtube.com/watch?v=FfaDt5BIET8) | Instance-first lookup, class fallback, getattr and hasattr | [Section 2](#attributes-lookup) 

 | [Class Attributes](https://www.youtube.com/watch?v=v_x70Eh2zNc) | One shared value on the class, rather than a copied field | [Section 1](#attributes-shared) 

 | [Bound Methods](https://www.youtube.com/watch?v=3tDCHG-qyt4) | Class-function calls supply the receiver explicitly | [Section 4](#attributes-functions) 

 | [Attribute Assignment](https://www.youtube.com/watch?v=Qxgl9ErC3uU) | Class updates versus individual overrides | [Section 3](#attributes-assignment) 

These notes were checked against all five available supplied-video transcripts. The explanatory order groups related ideas rather than repeating an exercise quota per video. The author’s [textbook chapter](https://composingprograms.com/pages/25-object-oriented-programming.html#class-attributes) is an optional reference.

 

## 1. Class attributes belong to the class

 

Consider a fleet whose delivery vans normally have the same speed limit. Each van has its own name, but a shared default limit belongs to the class. Assignment in the class body creates that class attribute. Assignment through self in the initializer creates an instance attribute instead.

 

```python
class DeliveryVan:
    limit = 40

    def __init__(self, name):
        self.name = name

    def travel_time(self, distance):
        return distance / self.limit

east = DeliveryVan('East')
west = DeliveryVan('West')
DeliveryVan.limit              # 40
east.limit                     # 40
west.limit                     # 40
```

 

There is one limit attribute on DeliveryVan, not an automatically copied limit field on every van. Both instances can read it because instance lookup can continue into the class. The initializer does not need to copy the default into each instance. Doing so would change what happens when the shared setting is updated later.

 

A class is an object too: the expression DeliveryVan refers to the class object. DeliveryVan.limit selects its attribute. In contrast, east refers to one instance, with its own name attribute. Methods defined by a def in the class body are class attributes containing functions, which receive special handling when found through an instance.

 

Self-check: does east.limit mean that limit must be stored inside east?

No. A dot expression tells you what was looked up, not where the successful lookup found it. Here the class supplies the value because east has no instance attribute named limit.

 

A class attribute provides one shared value. An instance can use it without storing its own copy.

 

## 2. Read an instance first, then its class

 

For the ordinary classes in this chapter, evaluate the expression to the left of the dot to obtain an object. If it is an instance, look for the named attribute on that instance first. If absent, look in its class. If the class value is a function, instance lookup produces a bound method. Inheritance and more advanced customization are outside this lesson.

 

```python
DeliveryVan.limit = 50
east.limit                     # 50
west.limit                     # 50
east.travel_time(100)          # 2.0

field = 'name'
getattr(east, field)           # 'East'
hasattr(east, 'limit')         # True: class fallback counts
hasattr(east, 'paint')         # False
```

 

The part after a literal dot is a fixed name. Writing east.field asks for an attribute actually named field, not the attribute whose name is stored in the variable field. Use getattr when a string chooses the attribute. The two-argument form requires the attribute to exist; use hasattr first when absence is permitted by your task. You can also write `getattr(east, field, fallback)`: the third argument is returned only when that attribute is missing, not when a present value is 0 or None.

 

Presence and truthiness answer different questions. An attribute holding 0, False, an empty list, or None is still present. Never discard one merely because its value is false when a task asks for all existing attributes. Also, hasattr includes attributes found through the class; it does not mean “stored directly on this instance.”

 

Self-check: how would you select the attribute named by field?

Use getattr(east, field). The string value inside field selects the name. Ordinary east.field uses the literal name field.

 

Dynamic lookup changes how the attribute’s name is supplied; it follows the same lookup rules as a dot expression.

 

## 3. Writing does not follow the same fallback rule

 

```python
east.limit = 30
east.limit                     # 30: instance attribute
west.limit                     # 50: class attribute
DeliveryVan.limit              # still 50

DeliveryVan.limit = 60
east.limit                     # still 30
west.limit                     # now 60
north = DeliveryVan('North')
north.limit                    # 60
```

 

For these ordinary objects, dot assignment sets an attribute on the object to the left of the dot. Assigning east.limit creates or updates an instance attribute. It does not search upward for the existing class attribute and replace that. The instance attribute shadows the class value during later reads.

 

Assigning DeliveryVan.limit changes the class attribute. Instances without an override see the updated value; east keeps its own override. New instances also use the current class value unless initialization installs an instance attribute with that name. An alias for east reaches the same instance, so an assignment through that alias affects east’s override.

 

Inside a method, self.limit = self.limit + 5 first reads with the lookup rule, then assigns to self. If the original value came from the class, the result still becomes an instance attribute. It does not increase the shared class setting. Separate the read target from the write target before predicting the result.

 

Self-check: why did updating the class to 60 not update east to 60?

east already has its own limit attribute. Lookup finds 30 there and stops; it does not need the class value.

 

Read: instance, then class. Write: the object explicitly named to the left of the dot.

 

## 4. A class function and a bound method use different call forms

 

```python
east.travel_time(90)                 # 3.0
DeliveryVan.travel_time(east, 90)     # 3.0

method_name = 'travel_time'
chosen = getattr(east, method_name)
chosen(60)                          # 2.0
plain = getattr(DeliveryVan, method_name)
plain(west, 120)                    # 2.0
```

 

Through east, travel_time becomes a bound method: its receiver is already supplied. Through DeliveryVan, travel_time is the function stored in the class, so the call explicitly supplies the object for self. Both forms execute the same function body. They differ in how that first argument is provided, not in the meaning of distance.

 

Dynamic lookup preserves the distinction. getattr(east, method_name) gives a bound method, while getattr(DeliveryVan, method_name) gives the function. A bound method needs the ordinary explicit arguments only. Adding east again would supply too many arguments. Conversely, calling the class function without a receiver omits a required argument.

 

The previous OOP chapter already taught saving a bound method and calling it later. The new application here is selecting a method by a string or retrieving the underlying class function. Do not recreate an instance to manufacture a receiver: use the object the task supplies so its overrides and lasting state are respected.

 

Self-check: does the class-function form construct another van?

No. DeliveryVan.travel_time is an attribute lookup, not a call to DeliveryVan itself. The existing instance east is passed explicitly to that function.

 

Instance lookup supplies self automatically. Class lookup returns the ordinary function, which needs self explicitly.

 

## 5. Follow the actual object to the left of the dot

 

The receiver need not be a simple variable name. It can be a list selection, a function call returning an object, or a chain of attribute selections. Evaluate that expression to find the receiver before thinking about the method. The name after a literal dot remains a simple fixed name.

 

```python
vans = [east, west]
vans[1].travel_time(120)        # 2.0: west uses limit 60

def pick_van(index):
    return vans[index]

pick_van(0).travel_time(90)     # 3.0: east uses limit 30
pick_van(1).limit = 45
west.limit                     # 45: assignment targets west
DeliveryVan.limit              # still 60
```

 

In the call, the dot expression is the operator expression: evaluate it to obtain a method, then evaluate the explicit arguments and call the method. An expression such as pick_van(1).limit = 45 evaluates pick_van(1) to west and sets an attribute on that instance. The function did not copy the van or turn the assignment into a class update.

 

For a reliable trace, record which object each expression produces, where the attribute lookup succeeds, and whether you are reading or writing. Compare an unmodified peer as well as the changed instance. A solution can produce one correct result while accidentally changing the shared setting for every other instance.

 

Self-check: does pick_van(1).limit = 45 change every van?

No. The receiver expression produces west, so the assignment installs west’s instance override. The class value stays 60, and east keeps its separate override of 30.

 

A complicated receiver expression follows the same rules: evaluate the receiver, look up or assign the attribute on the appropriate object, then perform the requested operation.

 

## Practice map

Switch to Practice above. Each task targets a different decision; the expandable hints are there when you need them.

- Change the shared default — class attributes
- Give one object its own rate — attribute assignment
- Look up a named attribute — dynamic lookup
- Supply self explicitly — methods and functions
