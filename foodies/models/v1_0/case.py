#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import List, Optional, Dict, Any, Union

from pydantic import BaseModel, Field

from foodies.models.v1_0.step import Step


class Case(BaseModel):
    id: str = Field(description="测试用例名，唯一标识了一个测试用例。")
    description: Optional[str] = Field(description="测试用例描述")
    steps: List[Union[str, Step]] = Field(description="一个字符串或步骤对象构成的 有序 列表。声明了该测试用例包含的步骤，其值可以为步骤名，或新定义的步骤对象。",
                                          default=[])
    skip: List[str] = Field(
        description="  一个正整数列表，取值范围为 1 到 n （包括 1 和 n）之间的所有整数，其中 n 为测试用例包含步骤数。字段声明了哪些步骤的 检查结果 可以 跳过 不做判断。缺省为空列表。",
        default=[])
    loop: Optional[Dict] = Field(description="case循环参数", default={})
