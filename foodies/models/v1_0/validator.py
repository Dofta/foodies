#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Optional, Dict, List

from pydantic import BaseModel, Field

from foodies.models.v1_0.function import Function
from foodies.models.v1_0.meta import Meta


class Validator(BaseModel):
    __root__: Optional[Dict[str, Meta]] = Field(
        description="一个键值对列表，键为该检查函数对应的输入参数名，值为对应参数的传入值。{function_ref} 为该检查函数的引用，如 '#/functions/validate_http_code'。")
    # __root__: Dict[str, List[Dict]] = Field(
    #     description="一个包含两个固定对象的列表。第一项为一个函数对象，用于定义检查函数；第二项为一个键值对列表，为第一项定义的函数的当前输入。该字段检查函数仅在当前步骤生效。")
