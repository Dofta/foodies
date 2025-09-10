#!/usr/bin/env python
# -*- coding: utf-8 -*-


def add_hook(rule, hook):
    if 'logic' in rule:
        for r in rule['rules']:
            add_hook(r, hook)
    else:
        for k in ['v1', 'v2']:
            rule[k] = lambda h=hook, v=rule[k]: h(v)


def check_rule_for_hook(rule, hook):
    import copy
    rule = copy.deepcopy(rule)
    add_hook(rule, hook)
    return check_rule(rule)


def check_rule(rule):
    if 'logic' in rule:
        return LOGIC_MAP[rule['logic']](rule['rules'])
    v1 = rule['v1']() if hasattr(rule['v1'], '__call__') else rule['v1']
    v2 = rule['v2']() if hasattr(rule['v2'], '__call__') else rule['v2']
    return OPERATOR_MAP[rule['op']](v1, v2)


def logic_and(rules):
    for rule in rules:
        if not check_rule(rule):
            return False
    return True


def logic_or(rules):
    for rule in rules:
        if check_rule(rule):
            return True
    return False


LOGIC_MAP = {
    'AND': logic_and,
    'OR': logic_or,
}

OPERATOR_MAP = {
    "<": lambda v1, v2: v1 < v2,
    ">": lambda v1, v2: v1 > v2,
    "<=": lambda v1, v2: v1 <= v2,
    ">=": lambda v1, v2: v1 >= v2,
    "==": lambda v1, v2: v1 == v2,
    "!=": lambda v1, v2: v1 != v2,
    "in": lambda v1, v2: v1 in v2,
    "not in": lambda v1, v2: v1 not in v2,
}



if __name__ == '__main__':

    condition = {"op": "<=", "v1": 6, "v2": 5}

    condition2 = {
        "logic": "AND",
        "rules": [
            {"op": "==", "v1": "aaab", "v2": "aaa"},
            {"op": "<=", "v1": 5, "v2": 5}
        ]
    }

    print(check_rule(condition2))