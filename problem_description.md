# Add `map_values` Utility Method to python-benedict

## Repository
- **URL**: https://github.com/fabiocaccamo/python-benedict
- **Commit**: e3947e59ea898183a541434ed3cecf665a56cba9
- **Language**: Python
- **Category**: feature_request
- **Difficulty**: medium

## Goal

Add a new utility method `map_values` to the `benedict` dict class that applies a
transformation function to all values in the dictionary and returns a new `benedict`
instance with the transformed values.

The library currently provides `filter` (select items by predicate) but has no method
to transform/map values using a callback. This is a natural and commonly needed
companion to `filter`.

## Behavioral Requirements

1. The `benedict` class must expose a new method called `map_values`.

2. `map_values` must accept a single argument: a callable (function) that receives
   two arguments (key, value) and returns the new value.

3. `map_values` must return a NEW `benedict` instance (not modify in-place).
   The original dict must remain unchanged.

4. The returned instance must be of the same type as the original (i.e., if a
   subclass of `benedict` calls `map_values`, the result should also be that subclass).

5. If the callable argument is not callable, a `ValueError` must be raised with
   a meaningful error message.

6. The method must work correctly with:
   - Empty dicts (returns empty benedict)
   - Dicts with mixed value types (int, str, None, nested dicts, lists)
   - String keys
   - Numeric values that get transformed (e.g., doubling integers)
   - Values transformed to a different type (e.g., int to str)
   - Values transformed to None

7. The transformation must be applied only to top-level values (not recursively
   into nested dicts). This is consistent with how `filter` works.

8. The core logic must live in a dedicated module under `benedict/core/` following
   the existing pattern of one-function-per-file.

9. The method must be importable from `benedict.core`.

## Edge Cases

- Passing a non-callable raises `ValueError`.
- Empty dict input returns an empty `benedict`.
- Transformation function that returns None for all values produces a dict with
  all None values (keys preserved).
- Original dict is never mutated.
- The returned dict is a `benedict` instance.

## Validation

- All existing repository tests must continue to pass.
- The new feature must be accessible as `d.map_values(func)` on any `benedict` instance.
- The returned value must be a new `benedict` instance, not the same object.