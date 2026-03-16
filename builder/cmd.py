def cmd_set(d: dict[str, str], params: list[str]):
    if len(params) < 2:
        print("Invalid SET: the variable requires a name and a value!")
        return
    d[params[0]] = params[1]


def cmd_get(dict: dict[str, str], param: str):
    return dict[param]


def cmd_project(data: dict[str, str], param: str):
    data['NAME'] = param[8:]


def cmd_project_type(data: dict[str, str], param: str):
    data['PROJECT_TYPE'] = param[13:].strip()


def cmd_version(data: dict[str, str], param: str):
    data['VERSION'] = str(param[8:])


