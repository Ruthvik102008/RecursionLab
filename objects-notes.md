# Objects: data with useful behavior

Work through one section and its four problems at a time. These explanations and practice examples were written for this workbook after reading all four video transcripts. The practice problems are new applications, not a transcript or an answer key.

[1. Objects](#objects) · [2. Working with types](#types) · [3. Type hints](#hints) · [4. Data classes](#records)

| Your video | Useful moments | Practice |
| --- | --- | --- |
| [Objects](https://www.youtube.com/watch?v=Q-CewobDFZM) | 0:14 dates · 1:29 attributes · 2:21 methods · 3:44 data and behavior | 1–4 |
| [Working with Types](https://www.youtube.com/watch?v=GBgyDCENCS0) | 0:00 inspection · 0:21 isinstance · 0:55 conversion | 5–8 |
| [Type Hints](https://www.youtube.com/watch?v=g2DiXOsGdfM) | 0:12 annotations · 1:13 unions · 1:48 aliases · 2:15 generics · 4:38 static checking | 9–12 |
| [Data Classes](https://www.youtube.com/watch?v=fdBjVdConb4) | 0:24 named parts · 3:34 dataclass · 5:50 display behavior · 6:58 __str__ | 13–16 |

<a id="objects"></a>

## 1. An object represents something

A date is more useful than three unrelated numbers: it knows which pieces are its year, month, and day, and can calculate a difference from another date. An **attribute** is a named part accessed through a dot. A **method** is behavior you call through a dot.

```python
from datetime import date
departure = date(2028, 6, 4)
arrival = date(2028, 6, 9)
departure.month                  # 6: stored information
departure.isoformat()            # '2028-06-04': method result
duration = arrival - departure
duration.days                    # 5
```

Read `departure.month` as “ask this date for its month.” Read `departure.isoformat()` as “ask this date to produce a display string.” The parentheses perform the call. An expression before the dot is evaluated first; `(arrival - departure).days` asks the resulting duration for its days.

A **class** describes a kind of object. Calling `date(...)` constructs an instance of that class. Classes are also values: you can pass `date` or `int` to another function, just as you can pass a number.

**Self-check: why does departure.month() fail?**

The month attribute holds an integer, not a callable method. The dot retrieves a value; parentheses attempt to call that value.

Practice 1–4: distinguish retrieving information, calling behavior, and constructing a value. The type of an intermediate result tells you what operations make sense next.

<a id="types"></a>

## 2. Inspecting and converting do different jobs

| Expression | Question answered |
| --- | --- |
| `type(value)` | What exact class does this value have? |
| `isinstance(value, float)` | Is this a float instance, including a subclass? |
| `float(value)` | Can I construct a float from this value? |

```python
text = '6.25'
type(text)                       # str
isinstance(text, float)           # False
number = float(text)
type(number)                     # float
text                             # still '6.25'
```

Conversion returns a new result; it does not change what the original name refers to. Invalid numeric text raises `ValueError`. Converting a float with `int` truncates toward zero, so `int(-3.9)` is `-3`, not `-4`. Converting is not rounding.

A subtle Python relationship: `isinstance(True, int)` is True because bool is a subclass of int. `type(True) is int` is False. Choose the test that matches the function’s contract.

**Self-check: does type('12') calculate 12?**

No. It returns the class str. The explicit call int('12') constructs an integer.

<a id="hints"></a>

## 3. Type hints describe a contract

```python
def offset(x: int) -> int:
    return x + 2

offset(4)                        # 6
offset(1.5)                      # 3.5: Python still executes it
```

The annotation after a parameter names the intended input type. The arrow names the intended result type. Ordinary Python execution does not enforce these hints or convert inputs. A static type checker analyzes code separately and can flag inconsistencies. This workbook checks required annotation syntax on selected problems and runs behavioral tests; it does not run a full static type checker.

`str | float` permits either type. An alias such as `type Measurement = str | float` gives that union a name. It does not define a new runtime constructor called Measurement.

```python
# Python 3.12+ syntax used in the video and this workbook:
type Measurement = str | float

def unchanged[T](x: T) -> T:
    return x
```

One type variable used twice communicates a relationship: whichever type comes in also goes out. A union in each position merely lists allowed alternatives; it does not express the same relationship. A constrained variable, `def unchanged[T: (int, float)](x: T) -> T:`, documents an int-to-int or float-to-float contract.

**Self-check: can a correct annotation fix a wrong calculation?**

No. Documentation and runtime behavior need separate checks. A return annotation of int does not turn an incorrect returned string into an integer.

Practice 9–12 uses Python 3.12 syntax. Keep the requested annotations while implementing the behavior. Python loads on the first run and needs an internet connection.

<a id="records"></a>

## 4. Data classes give each part a name

With a list such as `['Dock', 7.5]`, you must remember what each position means. A small data class puts those names into the definition once.

```python
from dataclasses import dataclass

@dataclass
class Parcel:
    destination: str
    weight: float

p = Parcel(destination='Dock', weight=7.5)
p.weight                         # 7.5
type(p).__name__                  # 'Parcel'
```

The decorator supplies useful ordinary behavior, including a constructor, representation, and equality comparison. Field order determines positional constructor order. Keyword arguments make the intended field explicit. A default field, such as `insured: bool = False`, follows required fields.

A method inside a class receives its instance as `self`. Special method `__str__` returns the readable string used by `str` and `print`. It must *return* a string, not print it and return None. The video assigns an existing formatting function to this special attribute; defining it in the class body installs the same kind of behavior.

Field hints remain hints: the constructor does not reject a string merely because the field is annotated float. Validation is separate behavior you would have to implement when a contract requires it.

**Self-check: what is the difference between Parcel and p?**

Parcel is a class. p is one instance storing a particular destination and weight. Another instance can store different values.

Practice 13–16: define records, use their named information, then give one record a readable display behavior.
