from enum import Enum

class Constraint:
    def __init__(self, install, name, version):
        self.install = install
        self.name = name
        self.version = version

    def __repr__(self):
        return f'Constraint({"Install" if self.install else "Uninstall"} \
{self.name}:{self.version if self.version != None else "*"})'

    @classmethod
    def from_str(cls, string):
        install = string.startswith('+')
        constraint = string.strip('+-')
        [name, version] = constraint.split('=') if '=' in string else [constraint, None]
        return cls(install, name, version)
