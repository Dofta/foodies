#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, List

from pydantic import BaseModel, Field


class Output(BaseModel):
    name: str = Field(description=" 输入参数名称")
    type: str = Field(description="输入参数类型")
    description: Optional[str] = Field(description="该参数作用的描述。")
