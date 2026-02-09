import unittest

from benedict import benedict


class TestMapValuesMethod(unittest.TestCase):
    """Tests for the map_values utility method on benedict."""

    def test_map_values_doubles_integers(self):
        """map_values should transform all values using the given function."""
        d = benedict({"a": 1, "b": 2, "c": 3})
        result = d.map_values(lambda k, v: v * 2)
        expected = {"a": 2, "b": 4, "c": 6}
        self.assertEqual(result, expected)

    def test_map_values_returns_new_benedict_instance(self):
        """map_values should return a new benedict instance, not the same object."""
        d = benedict({"a": 1, "b": 2})
        result = d.map_values(lambda k, v: v)
        self.assertIsInstance(result, benedict)
        self.assertIsNot(result, d)

    def test_map_values_does_not_mutate_original(self):
        """The original dict must remain unchanged after map_values."""
        d = benedict({"x": 10, "y": 20})
        original_copy = d.clone()
        _ = d.map_values(lambda k, v: v + 100)
        self.assertEqual(d, original_copy)

    def test_map_values_empty_dict(self):
        """map_values on an empty dict should return an empty benedict."""
        d = benedict()
        result = d.map_values(lambda k, v: v)
        self.assertEqual(result, {})
        self.assertIsInstance(result, benedict)

    def test_map_values_transform_type_int_to_str(self):
        """map_values should handle type changes (int -> str)."""
        d = benedict({"a": 1, "b": 2, "c": 3})
        result = d.map_values(lambda k, v: str(v))
        expected = {"a": "1", "b": "2", "c": "3"}
        self.assertEqual(result, expected)

    def test_map_values_transform_to_none(self):
        """map_values should allow transforming all values to None."""
        d = benedict({"a": 1, "b": "hello", "c": [1, 2]})
        result = d.map_values(lambda k, v: None)
        expected = {"a": None, "b": None, "c": None}
        self.assertEqual(result, expected)

    def test_map_values_uses_key_in_transformation(self):
        """The transformation function should receive the key as first argument."""
        d = benedict({"prefix_a": 1, "prefix_b": 2})
        result = d.map_values(lambda k, v: f"{k}={v}")
        expected = {"prefix_a": "prefix_a=1", "prefix_b": "prefix_b=2"}
        self.assertEqual(result, expected)

    def test_map_values_mixed_value_types(self):
        """map_values should work with mixed value types."""
        d = benedict({"a": 1, "b": "text", "c": None, "d": [1, 2], "e": {"nested": True}})
        result = d.map_values(lambda k, v: type(v).__name__)
        expected = {"a": "int", "b": "str", "c": "NoneType", "d": "list", "e": "dict"}
        self.assertEqual(result, expected)

    def test_map_values_raises_on_non_callable_string(self):
        """map_values must raise ValueError if argument is not callable."""
        d = benedict({"a": 1})
        with self.assertRaises(ValueError):
            d.map_values("not_a_function")

    def test_map_values_raises_on_none_argument(self):
        """map_values must raise ValueError if argument is None."""
        d = benedict({"a": 1})
        with self.assertRaises(ValueError):
            d.map_values(None)

    def test_map_values_raises_on_bool_argument(self):
        """map_values must raise ValueError if argument is a bool."""
        d = benedict({"a": 1})
        with self.assertRaises(ValueError):
            d.map_values(True)

    def test_map_values_raises_on_int_argument(self):
        """map_values must raise ValueError if argument is an int."""
        d = benedict({"a": 1})
        with self.assertRaises(ValueError):
            d.map_values(42)

    def test_map_values_single_item(self):
        """map_values should work with a single-item dict."""
        d = benedict({"only": 42})
        result = d.map_values(lambda k, v: v * 10)
        self.assertEqual(result, {"only": 420})

    def test_map_values_preserves_all_keys(self):
        """All keys from the original must be present in the result."""
        d = benedict({"a": 1, "b": 2, "c": 3, "d": 4, "e": 5})
        result = d.map_values(lambda k, v: 0)
        self.assertEqual(set(result.keys()), set(d.keys()))

    def test_map_values_with_string_values_uppercase(self):
        """map_values should work with string transformations."""
        d = benedict({"first": "hello", "second": "world"})
        result = d.map_values(lambda k, v: v.upper())
        expected = {"first": "HELLO", "second": "WORLD"}
        self.assertEqual(result, expected)

    def test_map_values_no_recursion_into_nested_dicts(self):
        """map_values should not recursively transform nested dicts or lists."""
        d = benedict({"a": 5, "b": {"inner_a": 10, "inner_b": 20}, "c": [100, 200, 300]})
        result = d.map_values(lambda k, v: v * 2 if isinstance(v, int) else v)
        expected = {"a": 10, "b": {"inner_a": 10, "inner_b": 20}, "c": [100, 200, 300]}
        self.assertEqual(result, expected)

    def test_map_values_nested_values_passed_as_whole_object(self):
        """Transformer should receive nested dicts/lists as whole objects, not recursively."""
        d = benedict({"a": {"inner": 1}, "b": [1, 2, 3]})
        calls = []
        
        def capture_calls(k, v):
            calls.append((k, v))
            return v
        
        d.map_values(capture_calls)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], ("a", {"inner": 1}))
        self.assertEqual(calls[1], ("b", [1, 2, 3]))

    def test_map_values_preserves_subclass_type(self):
        """map_values should return an instance of the same subclass."""
        class MyBenedict(benedict):
            pass
        
        d = MyBenedict({"a": 1, "b": 2})
        result = d.map_values(lambda k, v: v * 2)
        self.assertEqual(type(result), MyBenedict)


class TestMapValuesCoreFunction(unittest.TestCase):
    """Tests for the map_values core function import."""

    def test_map_values_importable_from_core(self):
        """map_values function should be importable from benedict.core."""
        from benedict.core import map_values
        self.assertTrue(callable(map_values))

    def test_map_values_in_core_all(self):
        """map_values should be in benedict.core.__all__."""
        import benedict.core
        self.assertIn("map_values", benedict.core.__all__)

    def test_map_values_core_returns_plain_dict(self):
        """The core function should return a plain dict, not a benedict."""
        from benedict.core import map_values
        d = {"a": 1, "b": 2}
        result = map_values(d, lambda k, v: v * 2)
        self.assertEqual(type(result), dict)
        self.assertNotEqual(type(result), benedict)

    def test_map_values_core_function_raises_on_non_callable(self):
        """The core function should raise ValueError for non-callable."""
        from benedict.core import map_values
        with self.assertRaises(ValueError):
            map_values({"a": 1}, 123)

    def test_map_values_core_raises_on_none(self):
        """The core function should raise ValueError for None."""
        from benedict.core import map_values
        with self.assertRaises(ValueError):
            map_values({"a": 1}, None)

    def test_map_values_core_no_recursion(self):
        """The core function should not recursively transform nested values."""
        from benedict.core import map_values
        d = {"a": 5, "b": {"nested": 10}}
        result = map_values(d, lambda k, v: v * 3 if isinstance(v, int) else v)
        expected = {"a": 15, "b": {"nested": 10}}
        self.assertEqual(result, expected)

    def test_map_values_core_does_not_mutate_input(self):
        """The core function should not mutate the input dict."""
        from benedict.core import map_values
        d = {"a": 1, "b": 2}
        original = d.copy()
        _ = map_values(d, lambda k, v: v * 10)
        self.assertEqual(d, original)


if __name__ == "__main__":
    unittest.main()