from unittest import TestCase

from mdspec.parser import ObjectSpec, parse_string


class TestInitial(TestCase):
    def test_parse_empty_string(self):
        objects = parse_string("")
        self.assertEqual(objects, [])

    def test_parse_empty_lines_string(self):
        objects = parse_string("\n\n\n\n\n")
        self.assertEqual(objects, [])

    def test_parse_empty_object(self):
        objects = parse_string("Foo is a Bar")
        self.assertEqual(objects, [ObjectSpec("Foo", "Bar")])


class TestCompare(TestCase):
    """
    For all the other tests to work, we need an easy way to compare object specs.
    And we need that to be reliable...
    """

    def test_equal(self):
        self.assertEqual(ObjectSpec("Foo", "Bar"), ObjectSpec("Foo", "Bar"))

    def test_unequal_type_name(self):
        self.assertNotEqual(ObjectSpec("Foo", "Bar"), ObjectSpec("Baz", "Bar"))

    def test_unequal_type_class(self):
        self.assertNotEqual(ObjectSpec("Foo", "Bar"), ObjectSpec("Foo", "Baz"))

    def test_unequal_fields(self):
        first = ObjectSpec("Foo", "Bar")
        second = ObjectSpec("Foo", "Bar")
        first.start_item_list("fields")
        second.start_item_list("fields")
        first.add_item("a")
        second.add_item("b")

        self.assertNotEqual(first, second)

    # TODO - test for order?
