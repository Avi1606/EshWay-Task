# Add `map_values` Utility Method to python-benedict

## Repository
- **URL**: https://github.com/fabiocaccamo/python-benedict
- **Commit**: e3947e59ea898183a541434ed3cecf665a56cba9
- **Language**: Python
- **Category**: feature_request
- **Difficulty**: medium

## Goal

Add a new utility method `map_values` to the `benedict` dict class that applies a transformation function to all **top-level** values in the dictionary and returns a new `benedict` instance with the transformed values.

The library currently provides `filter` (select items by predicate) but has no method to transform/map values using a callback. This is a natural and commonly needed companion to `filter`.

## Architecture and Interface

### Core Free Function (`benedict/core/map_values.py`)

`benedict.core.map_values` must be a **free function** importable via:

```python
from benedict.core import map_values
```

It takes two positional arguments `(mapping, transformer)`:
- `mapping`: a dict-like object (the source dictionary).
- `transformer`: a callable that receives `(key, value)` and returns the new value.

It must:
- Return a **new plain `dict`** with the transformed values.
- Raise `ValueError` if `transformer` is not callable.
- Apply the transformation to **top-level values only** — nested dicts and lists within values are passed as-is to the transformer, not iterated into.
- Not mutate the input `mapping`.
- Be listed in the `__all__` export of `benedict/core/__init__.py`.

### Class Method (`benedict.map_values`)

The `benedict` class must expose `map_values(self, transformer)` that:
- Calls the core free function internally.
- Returns a **new instance** of the **exact same type** as `self` (preserving subclass identity).
- Raises `ValueError` if `transformer` is not callable.
- Does not mutate the original instance.

## Validation

- `./test.sh base` must pass all existing repository tests.
- `./test.sh new` must fail before implementation and pass after correct implementation.
- The returned value from the class method must be a new instance, not the same object.
- The core free function must return a plain `dict`, not a `benedict`.
- `"map_values"` must appear in `benedict.core.__all__`.