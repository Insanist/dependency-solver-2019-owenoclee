class Package:
    def __init__(self, name, version, size, conflicts, depends):
        self.name = name
        self.version = version
        self.size = size
        self.conflicts = conflicts
        self.depends = depends

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
