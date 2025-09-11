#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Optional

from pydantic import BaseModel, Field


class FuncRet(BaseModel):
    type: str = Field(description="描述函数返回类型，取值范围包括纯量包含的数据类型，以及 map 和 list。缺省为 string。", default="string")
    value: str = Field(description="字符串形式描述的该函数的调用。形如 func(arg1=value1, arg2=value2, ...)。")
    description: Optional[str] = Field(description="该环境变量的描述。")
