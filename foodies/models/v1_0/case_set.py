#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Union, List, Optional

from pydantic import BaseModel, Field

from foodies.models.v1_0.case import Case


class CaseSet(BaseModel):
    id: str = Field(description="测试用例名，全局唯一 地标识了一个测试用例集。")
    description: Optional[str] = Field(description="测试用例集描述。")
    cases: List[Union[str, Case]] = Field(
        description="一个字符串或步骤对象构成的列表。声明了该测试用例集包含的测试用例或测试用例子集，其值可以为测试用例（集）名，或新定义的测试用例（集）对象。", default=[])
    ordered: bool = Field(description="声明 cases 是否有序，当值为 true 时，测试执行默认按列表顺序执行；当值为 false 时，测试执行顺序不指定。缺省为 false。",
                          default=False)


# CaseSet.update_forward_refs()
