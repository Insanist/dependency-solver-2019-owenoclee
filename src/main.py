import sys
import json
from package import Package
from constraint import Constraint

parsed = []
for i in range(1, 4):
    with open(sys.argv[i]) as f:
        parsed.append(json.load(f))

repository = parsed[0]
initial = parsed[1]
constraints = parsed[2]

repository = list(map(Package.from_json, repository))
constraints = list(map(Constraint.from_str, constraints))

print(repository)
print(constraints)
