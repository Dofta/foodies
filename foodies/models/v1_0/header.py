#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Optional, Union, Dict

from pydantic import BaseModel, Field


class Header(BaseModel):
    type: str = Field(description="描述变量类型，取值范围包括纯量包含的数据类型，以及 map 和 list。缺省为 string。", default="string")
    value: Union[str, Dict] = Field(description="请求头变量的具体值 或 引用。")
    description: Optional[str] = Field(description="该请求头变量的描述。")
