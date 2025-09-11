#!/usr/bin/env python
# -*- coding: utf-8 -*-


import collections
from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from foodies.models.v1_0.meta import Meta
from foodies.models.v1_0.result import Result
from foodies.models.v1_0.validator import Validator


class Step(BaseModel):
    id: str = Field(description=" 输入参数名称")
    type: str = Field(description="说明步骤类型，目前可选取值：function", default="function")
    meta: Meta = Field(description="根据步骤类型不同目前有两种定义，描述了步骤执行所需的元数据或其引用。", default=Meta.construct())
    validators: Optional[List[Validator]] = Field(description="步骤检查列表。默认传递当前 Step Object 的 meta 和 response 信息作为输入。")
    description: Optional[str] = Field(description="step的描述。")
    loop: Optional[Dict] = Field(description='条件、次数、选代值循环参数')
