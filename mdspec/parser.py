from functools import cached_property
import re
import sys
from typing import Optional


class ObjectSpec:
    """
    Each main 'object' in the specification is parsed into one of these.

    It contains the name & type of each object (_type_name, _type_class)
    and a list of all the field types on the object (_item_lists), eg ['fields', 'methods']
    Each of those field types is directly on the object itself (eg. self.fields, self.methods)
    Optionally it also has the name of the module where it should be defined ( _module_name)
    """

    _type_class: str
    _type_name: str
    _module_name: Optional[str] = None
    # TODO - think - would it be better just to keep these in a dict rather than directly putting
    # them on the object?
    _item_lists = list

    def __init__(self, type_name, type_class):
        self._type_name = type_name
        self._type_class = type_class
        self._item_lists = []

    def __str__(self):
        return f"<{self._type_class}: {self._type_name}>"

    def __repr__(self):
        return str(self)

    def start_item_list(self, items_name):
        setattr(self, items_name, [])
        self._item_lists.append(items_name)

    def add_item(self, item):
        getattr(self, self._item_lists[-1]).append(item)

    def to_json(self):
        result = {
            "_name": self._type_name,
            "_type": self._type_class,
        }
        for item_list in self._item_lists:
            result[item_list] = getattr(self, item_list)
        return result


class Parser:
    @cached_property
    def matchers(self):
        return [
            (re.compile("(.*) is a (.*)", re.IGNORECASE), self.start_type_class),
            (re.compile("it is defined in (.*)", re.IGNORECASE), self.is_defined_in),
            (re.compile("It has these (.*):", re.IGNORECASE), self.start_item_list),
            (re.compile("- (.*)", re.IGNORECASE), self.add_item),
            (re.compile("^$"), self.noop),
        ]

    def __init__(self):
        self.defined_objects = []

    def start_type_class(self, type_name, type_class):
        self.defined_objects.append(ObjectSpec(type_name, type_class))

    def start_item_list(self, items_name):
        self.defined_objects[-1].start_item_list(items_name)

    def add_item(self, field_name):
        field_items = list(part.strip() for part in field_name.split(":"))
        self.defined_objects[-1].add_item(field_items)

    def is_defined_in(self, module_name):
        self.defined_objects[-1]._module_name = module_name

    def noop(self):
        return

    def parse_string(self, input_string):
        # strip comments:
        contents = re.sub(r"\(.*\)", "", input_string)

        for line in contents.splitlines():
            line = line.strip().strip(".").strip()
            # remove multiple spaces:
            line = re.sub(r"\s+", " ", line)

            for regexp, func in self.matchers:
                if match := regexp.match(line):
                    func(*match.groups())
                    break
            else:
                print(f"Unknown line: {line}")

        return [object.to_json() for object in self.defined_objects]


def read_spec_file(filename):
    with open(filename) as fh:
        return parse_string(fh.read())


def parse_string(input_value):
    parser = Parser()
    return parser.parse_string(input_value)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        defined_objects = read_spec_file(sys.argv[-1])
    else:
        print("usage: modelspec <filename>")

    for object in defined_objects:
        print(f"{object}:")
        for fieldtype in object._item_lists:
            print(f"  {fieldtype}:")
            for field in getattr(object, fieldtype):
                fieldname = field[0]
                field_details = field[1:]
                print(
                    f"  - {field[0]}"
                    f"{' : ' if field_details else ''}"
                    f"{','.join(field_details) if field_details else ''}"
                )
