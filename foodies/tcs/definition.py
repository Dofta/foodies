#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from foodies.models.v1_0.definitions import Definitions as definitions_model
from foodies.utils.logger import make_decorator_for_func
log_func = make_decorator_for_func(__file__)


# @log_func(name='解析动态引用')
def parse_val(val):
    def cb(match) -> str:
        key = match.group(1)
        r = re.compile(r'(.*?)([\.\[].*)')
        m = r.match(key)
        var = None
        if m:
            key = m.group(1)
            var = m.group(2)
        definition = Definition()
        if key not in definition.key_map:
            return match.group(0)
        key_res_type = definition.key_map[key]['res_type']
        key_type = definition.key_map[key]['type']
        key_value = definition.key_map[key]['value']
        if m:
            return RES_TYPE_MAP[key_res_type](key_value, var)
        return DATA_TYPE_MAP[key_type](RES_TYPE_MAP[key_res_type](key_value))
    reobj = re.compile(r'\{\{ *(.*?) *\}\}')
    match = reobj.match(val)
    # 如果能全匹配，返回原本的数据类型，如果不能全匹配，说明是拼串了，按字符串替换处理
    return cb(match) if match else reobj.sub(lambda m: str(cb(m)), val)


def list_data(s):
    if type(s) == dict:
        for k, v in s.items():
            s[k] = list_data(v)
    elif type(s) == list:
        for k, v in enumerate(s):
            s[k] = list_data(v)
    elif type(s) == str:
        s = parse_val(s)
        if type(s) != str:
            s = list_data(s)
    return s


def parse_variables(s):
    return list_data(s)


def parse_servers(s):
    return list_data(s)


def parse_headers(s):
    return list_data(s)


def parse_envs(s):
    val = parse_val(s)
    val = os.getenv(val)
    if not val:
        raise Exception("env %s not found" % s)
    return val


def parse_func_rets(s, v=None):
    from foodies.tcs.node.base_func_node import BaseFuncNode
    s = parse_val(s)
    s = s.replace("\n", "")
    reobj = re.compile(r'(.*?)\((.*)\)')
    match = reobj.match(s)
    func_name, param = match.groups()
    func = BaseFuncNode.get_func(func_name)
    if not func:
        raise Exception("func %s not found" % func_name)
    data = func(eval(param))
    return eval("data%s" % v) if v else data


DATA_TYPE_MAP = {
    'string': lambda v: str(v),
    'int': lambda v: int(v),
    'float': lambda v: float(v),
    'map': lambda v: v,
    'list': lambda v: v,
    'object': lambda v: v,
}

RES_TYPE_MAP = {
    'variables': parse_variables,
    'servers': parse_servers,
    'headers': parse_headers,
    'envs': parse_envs,
    'func_rets': parse_func_rets
}


class Definition(object):
    def __new__(cls, model: definitions_model=None):
        if '_inst' not in vars(cls):
            cls._inst = super(Definition, cls).__new__(cls)
            cls._inst.model = model
            cls._inst.__key_map = None
        return cls._inst

    @property
    def key_map(self):
        if self.__key_map is None:
            self.__key_map = {}
            for res_type, var_map in self.model.dict().items():
                for v, data in var_map.items():
                    self.__key_map[v] = {
                        'res_type': res_type,
                        'type': data.get('type'),
                        'value': data.get('value')}
        return self.__key_map



