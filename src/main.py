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

required_pkgs = []
disallowed_pkgs = []
for c in constraints:
    p = helper.filter_by_constraint(pkgs, c)
    if c.install:
        required_pkgs.append(p)
    else:
        disallowed_pkgs.append(Not(p))

with_deps = []
with_conflicts = []
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

    con_list = repository[k].conflicts
    all_of = []
    for con in con_list:
        if con.range == Range.exactly:
            p = pkgs[f'{con.name}={con.version}']
            all_of.append(Not(p))
        else:
            sub_pkgs = helper.filter_by_vconstraint(pkgs, con)
            all_of.extend(map(lambda x: Not(x), sub_pkgs.values()))

    if len(all_of) > 1:
        with_conflicts.append(Implies(pkg, And(all_of)))
    elif len(all_of) == 1:
        with_conflicts.append(Implies(pkg, all_of[0]))

solver = Solver()
solver.add(*with_deps, *with_conflicts, *required_pkgs, *disallowed_pkgs)
commands = []
if solver.check() == sat:
    model = solver.model()
    for i in model:
        if is_true(model[i]):
            commands.append(f'+{i.name()}')

print(json.dumps(commands))

with open(sys.argv[1].replace('repository', 'commands'), 'a') as commands_file:
    json.dump(commands, commands_file)
