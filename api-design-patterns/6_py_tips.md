# Python Little Big Things

Subtle behaviors that can cause real bugs or give you elegant one-liners.

---

## 1. `and` returns the last truthy / first falsy

```python
a = 14
b = 4
print(b and a)  # ➝ 14
```

`and` doesn’t coerce to `True` or `False` — it returns actual values. If the first value is falsy (`0`, `''`, `None`, etc.), it returns that immediately. Otherwise, it evaluates and returns the second.

Useful for chaining:
```python
user = token_data and token_data.get("user")
```

---

## 2. `or` returns the first truthy value

```python
a = 0
b = "hello"
print(a or b)  # ➝ "hello"
```

If the first value is truthy, it's returned immediately. Otherwise, it goes to the next one.

Handy for default values:
```python
limit = user_input or DEFAULT_LIMIT
```

---

## 3. Mutable default arguments stick around

```python
def log_message(msg, log=[]):
    log.append(msg)
    return log

print(log_message("start"))     # ['start']
print(log_message("processing"))  # ['start', 'processing'] ← not reset
print(log_message("done"))        # ['start', 'processing', 'done']
```

### Why this happens

In Python, **default argument values are evaluated only once**, when the function is **defined**, not every time it’s called. That means if you use a mutable object like a list or dict, it's shared across all calls that don’t override the default.
Under the hood:
```python
def log_message(msg, log=[]):
    ...

# Is roughly like:
_log = []
def log_message(msg, log=_log):
    ...
```

You might expect the log to be empty each time, but it keeps growing because it reuses the same list across all calls. 
So when `log.append(msg)` happens, it's always modifying the same list unless you explicitly pass a new one.

Correct pattern:
```python
def log_message(msg, log=None):
    if log is None:
        log = []
    log.append(msg)
    return log
```

Now a new list is created each time the function is called without an argument.

---

## 4. `else` on a loop runs only if there was **no `break`**

```python
for i in [1, 2, 3]:
    if i == 2:
        break
else:
    print("loop finished cleanly")  # won't run
```

The `else` clause after a `for` or `while` runs **only if the loop wasn't interrupted by `break`**.

Great for search patterns:
```python
for user in users:
    if user.is_admin:
        break
else:
    raise ValueError("No admin found")
```

---

## 5. Underscores have special meaning

```python
_var    # "internal use" by convention
var_    # avoids name conflict (e.g. with `class`)
__var   # name-mangled to _Class__var
_       # discard value or reuse last expression (in REPL)
```

Examples:
```python
for _ in range(3):
    do_something()

x, _, z = (1, 2, 3)  # ignore middle value

>>> 5 + 3
8
>>> _ * 2
16
```

---

## 6. Chained comparison is smarter than it looks

```python
x = 5
print(1 < x < 10)  # ➝ True
```

This is not just syntax sugar — Python evaluates it as:
```python
(1 < x) and (x < 10)
```

Also works with equality:
```python
if a == b == c:
    ...
```

---

## 7. Functions are objects (you can tag them)

```python
def greet(name):
    return f"Hello, {name}"

greet.version = "v1.2"
print(greet.version)  # ➝ v1.2
```

You can add attributes to functions like any object. Useful for plugins, tagging, or attaching metadata to behavior.

---

## 8. `set` uses hashes — no guaranteed order

```python
s = {"a", "b", "c"}
print(s)  # order is arbitrary

# Meanwhile:
d = {"a": 1, "b": 2, "c": 3}
print(d)  # insertion order preserved (Python 3.7+)
```

Don’t rely on the order of a `set`. Even though it may look stable in small tests, it’s not guaranteed — especially across Python versions or machines.

---

## 9. Walrus operator (`:=`) allows inline assignment

```python
if (n := len(data)) > 10:
    print(f"Too much data: {n}")
```

Python 3.8+ lets you assign and use a value inside expressions. Great for avoiding repeated computation.

---

## 10. Decorators are just function wrappers

```python
def debug(fn):
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@debug
def run():
    print("Running!")

run()
# ➝ Calling run
# ➝ Running!
```

A decorator is just a function that takes another function and returns a new one. You can build logging, caching, validation, etc., by wrapping logic.

```python
# This:
@debug
def func(): ...

# Is the same as:
func = debug(func)
```

---

