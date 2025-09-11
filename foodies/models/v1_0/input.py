#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, List, Any

from pydantic import BaseModel, Field


class Input(BaseModel):
    name: str = Field(description=" 输入参数名称")
    required: bool = Field(description=" 说明参数是否必须。缺省值为 true。")
    type: str = Field(description="输入参数类型")
    default: Optional[Any] = Field(description="与 type 匹配的输入参数默认值 或 引用。")
    description: Optional[str] = Field(description="该参数作用的描述。")
