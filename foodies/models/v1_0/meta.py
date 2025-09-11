#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, Dict, List

from pydantic import BaseModel, Field


class Meta(BaseModel):
    function_name: str = Field(description="步骤使用的函数名称。", default="")
    system: Optional[str] = Field(description="运行操作系统环境。", default='')
    input: Optional[Dict] = Field(description="一个键值对 map，键为该函数对应的输入参数名，值为对应参数的传入值。", default={})
    timeout: Optional[int] = Field(description="函数执行默认的超时限制，即超出这个时间后函数中止。单位秒，默认值 60。", default=60)