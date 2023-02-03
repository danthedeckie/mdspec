import re
import sys

# globals (for now)
defined_objects = []


class ObjectSpec:
    _type_class: str
    _type_name: str
    _module_name: str
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


def start_type_class(type_name, type_class):
    defined_objects.append(ObjectSpec(type_name, type_class))


def start_item_list(items_name):
    defined_objects[-1].start_item_list(items_name)


def add_item(field_name):
    field_tuple = tuple(part.strip() for part in field_name.split(":"))
    defined_objects[-1].add_item(field_tuple)


def is_defined_in(module_name):
    defined_objects[-1]._module_name = module_name


def noop():
    return


matchers = [
    (re.compile("(.*) is a (.*)", re.IGNORECASE), start_type_class),
    (re.compile("it is defined in (.*)", re.IGNORECASE), is_defined_in),
    (re.compile("It has these (.*):", re.IGNORECASE), start_item_list),
    (re.compile("- (.*)", re.IGNORECASE), add_item),
    (re.compile("^$"), noop),
]


def readspec(filename):
    with open(filename) as fh:
        contents = fh.read()

    # strip comments:
    contents = re.sub(r"\(.*\)", "", contents)

    for line in contents.splitlines():
        line = line.strip().strip(".").strip()
        # remove multiple spaces:
        line = re.sub(r"\s+", " ", line)

        for regexp, func in matchers:
            if match := regexp.match(line):
                func(*match.groups())
                break
        else:
            print(f"Unknown line: {line}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        readspec(sys.argv[-1])
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
