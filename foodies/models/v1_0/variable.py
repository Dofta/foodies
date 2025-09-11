#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Optional

from pydantic import BaseModel, Field


class Variable(BaseModel):
    type: str = Field(description="描述变量类型，取值范围包括纯量包含的数据类型，以及 map 和 list。缺省为 string。", default="string")
    value: Any = Field(description="该变量的具体值 或 引用。")
    description: Optional[str] = Field(description="该变量的描述。")
