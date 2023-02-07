import re
import sys
from functools import cached_property
from typing import Optional


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

    @property
    def current_object(self):
        return self.defined_objects[-1]

    ##############################################
    # Matcher methods:

    def start_type_class(self, type_name, type_class):
        self.defined_objects.append({"_name": type_name, "_type": type_class})

    def start_item_list(self, items_name):
        self.current_list = []
        self.current_object[items_name] = self.current_list

    def add_item(self, field_name):
        field_items = list(part.strip() for part in field_name.split(":"))
        self.current_list.append(field_items)

    def is_defined_in(self, module_name):
        self.current_object["_module_name"] = module_name

    def noop(self):
        return

    #############################################
    # The main parsing routine:

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

        return [object for object in self.defined_objects]


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
