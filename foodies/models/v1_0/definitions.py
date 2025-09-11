#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, Dict, List

from pydantic import BaseModel, Field, Extra

from foodies.models.v1_0.header import Header
from foodies.models.v1_0.server import Server
from foodies.models.v1_0.variable import Variable
from foodies.models.v1_0.env import Env
from foodies.models.v1_0.func_ret import FuncRet


class Definitions(BaseModel):
    class Config:
        extra = Extra.allow

    variables: Optional[Dict[str, Variable]] = Field(description="变量资源。键 为变量名，全局唯一；值为一个变量对象。", default={})
    headers: Optional[Dict[str, Header]] = Field(description="HTTP 请求头变量资源。键 为请求头变量名；值为请求头变量具体值", default={})
    header_sets: Optional[Dict[str, Dict[str, str]]] = Field(
        description="HTTP 请求头资源（组装请求头）。键 为该组装的请求头的代称名；值为一个请求头变量值引用的列表。",
        default={})
    servers: Optional[Dict[str, Server]] = Field(description="HTTP 服务端资源（提供不同测试环境）。键 为该测试环境服务端代称名；值为一个服务端资源对象。",
                                                 default={})
    envs: Optional[Dict[str, Env]] = Field(
        description="环境变量资源。键 为变量名，全局唯一；值为使用的环境变量名称。使用时被替换为环境变量的实际值。", 
        default={})
    func_rets: Optional[Dict[str, FuncRet]] = Field(
        description="初始化函数结果资源。键 为变量名，全局唯一；值为一个函数调用表达式。使用时被替换为函数调用返回结果。", 
        default={})