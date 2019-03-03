from enum import Enum

class Package:
    def __init__(self, name, version, size, conflicts, depends):
        self.name = name
        self.version = version
        self.size = size
        self.conflicts = parse_constraints(conflicts)
        self.depends = list(map(parse_constraints, depends))

    def __repr__(self):
        return f'''Package(
    name: {self.name},
    version: {self.version},
    size: {self.size},
    conflicts: {self.conflicts},
    depends: {self.depends}
)'''

    @classmethod
    def from_json(cls, json):
        return cls(
            json['name'],
            json['version'],
            json['size'],
            json.get('conflicts', []),
            json.get('depends', []))

class Range(Enum):
    above = 0
    below = 1
    and_above = 2
    and_below = 3
    exactly = 4

class Constraint:
    def __init__(self, name, version, range):
        self.name = name
        self.version = version
        self.range = range

    def __repr__(self):
        return f'Constraint({self.name}, {self.version} {self.range})'

def parse_constraint(string):
    if '<=' in string:
        range = Range.and_below
        [name, version] = string.split('<=')
    elif '>=' in string:
        range = Range.and_above
        [name, version] = string.split('>=')
    elif '<' in string:
        range = Range.below
        [name, version] = string.split('<')
    elif '>' in string:
        range = Range.above
        [name, version] = string.split('>')
    elif '=' in string:
        range = Range.exactly
        [name, version] = string.split('=')
    else:
        return Constraint(string, None, None)

    return Constraint(name, version, range)

def parse_constraints(strings):
    return list(map(parse_constraint, strings))
