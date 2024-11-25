#!/usr/bin/env python3
"""
Defines unit tests for `utils.py`.
"""

import unittest

from parameterized import parameterized

import utils


class TestAccessNestedMap(unittest.TestCase):
    """
    Defines unit tests for `utils.access_nested_map`.
    """

    @parameterized.expand(
        (
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        )
    )
    def test_access_nested_map(self, nested_map, path, result):
        """
        Tests `utils.access_nested_map`.
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), result)

    @parameterized.expand(
        (
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        )
    )
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Tests `utils.access_nested_map`.
        """
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Defines unit tests for `utils.get_json`.
    """

    @parameterized.expand(
        (
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        )
    )
    @unittest.mock.patch("requests.get")
    def test_get_json(self, url, json, mock_method):
        """
        Tests `utils.get_json`.
        """
        mock_response = unittest.mock.Mock()
        mock_response.json = lambda: json
        mock_method.return_value = mock_response
        self.assertEqual(utils.get_json(url), json)


class TestMemoize(unittest.TestCase):
    """
    Defines unit tests for `utils.memoize`.
    """

    def test_memoize(self):
        """
        Tests `utils.memoize`.
        """

        class TestClass:

            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        with unittest.mock.patch.object(
            test_instance, "a_method", wraps=test_instance.a_method
        ) as mock_method:
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()
