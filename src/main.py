import sys
import json
from package import Package, Range
from constraint import Constraint
from z3 import *
import helper

parsed = []
for i in range(1, 4):
    with open(sys.argv[i]) as f:
        parsed.append(json.load(f))

repository = parsed[0]
initial = parsed[1]
constraints = parsed[2]

repository = {p.get_id():p for p in map(Package.from_json, repository)}
constraints = list(map(Constraint.from_str, constraints))

pkgs = {k:Bool(k) for k, _ in repository.items()}

with_deps = []
for k, pkg in pkgs.items():
    dep_list_list = repository[k].depends
    all_of = []
    for dep_list in dep_list_list:
        any_of = []
        for dep in dep_list:
            if dep.range == Range.exactly:
                p = pkgs[f'{dep.name}={dep.version}']
                any_of.append(p)
            else:
                sub_pkgs = helper.filter_by_vconstraint(pkgs, dep)
                any_of.extend(sub_pkgs.values())

        if len(any_of) > 1:
            all_of.append(Or(any_of))
        elif len(any_of) == 1:
            all_of.append(any_of[0])

    if len(all_of) > 1:
        with_deps.append(Implies(pkg, And(all_of)))
    elif len(all_of) == 1:
        with_deps.append(Implies(pkg, all_of[0]))

print(with_deps)
