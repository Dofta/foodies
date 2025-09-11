#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Dict

from pydantic import BaseModel, Field

from foodies.models.v1_0.function import Function


class Functions(BaseModel):
    __root__: Dict[str, Function] = Field(description="key 为function_name，为全局唯一的函数名，值为一个函数对象。")
