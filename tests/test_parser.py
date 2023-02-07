from unittest import TestCase

from deepdiff import DeepDiff

from mdspec.parser import parse_string


class DifferentResult(AssertionError):
    def __init__(self, source, expected_result, actual_result, diff) -> None:
        self.source = source
        self.expected_result = expected_result
        self.actual_result = actual_result

        source_intented = "\n  " + source.replace("\n", "\n  ")

        formatted_result = str(diff)

        super().__init__(
            f"\nGiven:{source_intented}"
            f"\nExpected-Result:\n  {expected_result}"
            f"\nActual-Result:\n  {actual_result}"
            f"\nDiff:\n  {formatted_result}"
        )


class BaseTestCase(TestCase):
    def assertInputResultsIn(self, source, expected_result):
        actual_result = parse_string(source)
        diff = DeepDiff(actual_result, expected_result)

        if diff:
            raise DifferentResult(
                source=source,
                expected_result=expected_result,
                actual_result=actual_result,
                diff=diff,
            )


class TestInitial(BaseTestCase):
    def test_diff_assert_works(self):
        with self.assertRaises(DifferentResult):
            self.assertInputResultsIn("Foo is a Bar", [{"tis different!": "forsooth..."}])

    def test_parse_empty_string(self):
        self.assertInputResultsIn("", [])

    def test_parse_empty_lines_string(self):
        self.assertInputResultsIn("\n\n\n\n\n", [])

    def test_parse_empty_object(self):
        self.assertInputResultsIn("Foo is a Bar", [{"_name": "Foo", "_type": "Bar"}])

    def test_parse_object_including_fields(self):
        self.assertInputResultsIn(
            """
            Foo is a Bar
            It has these fields:
             - red
             - green
             - blue
            """,
            [
                {
                    "_name": "Foo",
                    "_type": "Bar",
                    "fields": [["red"], ["green"], ["blue"]],
                }
            ],
        )

    def test_parse_object_including_fields_with_additional_values(self):
        self.assertInputResultsIn(
            """
            Foo is a Bar
            It has these fields:
             - red: tomatos strawberries roses
             - green: cabbage broccoli new-deals
             - blue: oceans skys feelings
            """,
            [
                {
                    "_name": "Foo",
                    "_type": "Bar",
                    "fields": [
                        ["red", "tomatos strawberries roses"],
                        ["green", "cabbage broccoli new-deals"],
                        ["blue", "oceans skys feelings"],
                    ],
                }
            ],
        )
