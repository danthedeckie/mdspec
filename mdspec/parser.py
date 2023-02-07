import re
import sys
from typing import Optional


class ObjectSpec:
    """
    Each main 'object' in the specification is parsed into one of these.

    It contains the name & type of each object (_type_name, _type_class)
    and a list of all the field types on the object (_fieldlist), eg ['fields', 'methods']
    Each of those field types is directly on the object itself (eg. self.fields, self.methods)
    Optionally it also has the name of the module where it should be defined ( _module_name)
    """

    _type_class: str
    _type_name: str
    _module_name: Optional[str] = None
    # TODO - think - would it be better just to keep these in a dict rather than directly putting
    # them on the object?
    _fieldlist = list

    def __init__(self, type_name, type_class):
        self._type_name = type_name
        self._type_class = type_class
        self._fieldlist = []

    def __str__(self):
        return f"<{self._type_class}: {self._type_name}>"

    def __repr__(self):
        return str(self)

    def start_item_list(self, items_name):
        setattr(self, items_name, [])
        self._fieldlist.append(items_name)

    def add_item(self, item):
        getattr(self, self._fieldlist[-1]).append(item)

    def __eq__(self, other):
        if (
            other._type_name == self._type_name
            and other._type_class == self._type_class
            and other._module_name == self._module_name
            and set(self._fieldlist) == set(other._fieldlist)
        ):
            for fieldset in self._fieldlist:
                if set(getattr(self, fieldset)) != set(getattr(other, fieldset)):
                    return False
            return True

        return False


def start_type_class(defined_objects, type_name, type_class):
    defined_objects.append(ObjectSpec(type_name, type_class))


def start_item_list(defined_objects, items_name):
    defined_objects[-1].start_item_list(items_name)


def add_item(defined_objects, field_name):
    field_tuple = tuple(part.strip() for part in field_name.split(":"))
    defined_objects[-1].add_item(field_tuple)


def is_defined_in(defined_objects, module_name):
    defined_objects[-1]._module_name = module_name


def noop(defined_objects):
    return


matchers = [
    (re.compile("(.*) is a (.*)", re.IGNORECASE), start_type_class),
    (re.compile("it is defined in (.*)", re.IGNORECASE), is_defined_in),
    (re.compile("It has these (.*):", re.IGNORECASE), start_item_list),
    (re.compile("- (.*)", re.IGNORECASE), add_item),
    (re.compile("^$"), noop),
]


def read_spec_file(filename):
    with open(filename) as fh:
        return parse_string(fh.read())


def parse_string(input_string):
    defined_objects = []
    # strip comments:
    contents = re.sub(r"\(.*\)", "", input_string)

    for line in contents.splitlines():
        line = line.strip().strip(".").strip()
        # remove multiple spaces:
        line = re.sub(r"\s+", " ", line)

        for regexp, func in matchers:
            if match := regexp.match(line):
                func(defined_objects, *match.groups())
                break
        else:
            print(f"Unknown line: {line}")

    return defined_objects


if __name__ == "__main__":
    if len(sys.argv) > 1:
        defined_objects = read_spec_file(sys.argv[-1])
    else:
        print("usage: modelspec <filename>")

    for object in defined_objects:
        print(f"{object}:")
        for fieldtype in object._fieldlist:
            print(f"  {fieldtype}:")
            for field in getattr(object, fieldtype):
                fieldname = field[0]
                field_details = field[1:]
                print(
                    f"  - {field[0]}"
                    f"{' : ' if field_details else ''}"
                    f"{','.join(field_details) if field_details else ''}"
                )
