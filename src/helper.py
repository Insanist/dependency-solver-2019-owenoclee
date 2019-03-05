def filter_by_vconstraint(pkgs, vconstraint):
    start = f'{vconstraint.name}='
    match_name = {k:v for k, v in pkgs.items() if k.startswith(start)}
    match_name_version = {k:v for k, v in match_name.items() if vconstraint.test(k.split('=')[1])}
    return match_name_version

def filter_by_constraint(pkgs, constraint):
    start = f'{constraint.name}='
    match_name = {k:v for k, v in pkgs.items() if k.startswith(start)}
    if constraint.version == None:
        return list(match_name.values())[0]
    match_name_version = {k:v for k, v in match_name.items() if k.endswith(f'={constraint.version}')}
    return list(match_name_version.values())[0]
