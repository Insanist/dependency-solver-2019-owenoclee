def filter_by_vconstraint(pkgs, vconstraint):
    start = f'{vconstraint.name}='
    match_name = {k:v for k, v in pkgs.items() if k.startswith(start)}
    match_name_version = {k:v for k, v in match_name.items() if vconstraint.test(k.split('=')[1])}
    return match_name_version
