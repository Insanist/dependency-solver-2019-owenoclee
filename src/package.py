from enum import Enum

class Package:
    def __init__(self, name, version, size, conflicts, depends):
        self.name = name
        self.version = version
        self.size = size
        self.conflicts = list(map(VersionConstraint.from_str, conflicts))
        self.depends = list(map(lambda l: list(map(VersionConstraint.from_str, l)), depends))

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

class VersionConstraint:
    def __init__(self, name, version, range):
        self.name = name
        self.version = version
        self.range = range

    def __repr__(self):
        return f'VersionConstraint({self.name}, {self.version} {self.range})'

    @classmethod
    def from_str(cls, string):
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
            return cls(string, None, None)

        return cls(name, version, range)
