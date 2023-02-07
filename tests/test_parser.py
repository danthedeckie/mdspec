import json
from unittest import TestCase

from deepdiff import DeepDiff

from mdspec.parser import ObjectSpec, parse_string


class DifferentResult(AssertionError):
    def __init__(self, source, expected_result, actual_result, diff) -> None:
        self.source = source
        self.expected_result = expected_result
        self.actual_result = actual_result

        source_intented = "\n  " + source.replace("\n", "\n  ")

        super().__init__(
            f"\nGiven:{source_intented}"
            f"\nExpected-Result:\n  {expected_result}"
            f"\nActual-Result:\n  {actual_result}"
            f"\nDiff:\n  {json.dumps(diff, indent=2)}"
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
    def test_parse_empty_string(self):
        self.assertInputResultsIn("", [])

    def test_parse_empty_lines_string(self):
        self.assertInputResultsIn("\n\n\n\n\n", [])

    def test_parse_empty_object(self):
        self.assertInputResultsIn("Foo is a Bar", [ObjectSpec("Foo", "Bar")])

    def test_diff_assert_works(self):
        self.assertInputResultsIn("Foo is a Bar", [ObjectSpec("Foo", "Balloon")])
