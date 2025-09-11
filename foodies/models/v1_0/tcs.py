#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, List, Union, Dict

from pydantic import BaseModel, Field
from foodies.models.v1_0.case import Case
from foodies.models.v1_0.case_set import CaseSet
from foodies.models.v1_0.definitions import Definitions
from foodies.models.v1_0.functions import Functions
from foodies.models.v1_0.info import Info
from foodies.models.v1_0.step import Step


class TCS(BaseModel):
    # tcs: str = Field(description="这个字符串必须为 major.minor.patch 形式的版本号，用于说明当前文档使用的 TCS 版本。工具也可以通过该字段来辨别 TCS 文档。")
    info: Info = Field(description="提供文档相关的元数据，包括一些自定义的 label。用于说明与当前测试用例相关的一些信息。", default=Info.construct())
    definitions: Optional[Definitions] = Field(description="资源声明与定义。字段值为一个资源声明对象，其中每一项为一类资源的具体定义。",
                                               default=Definitions.construct())
    functions: Optional[Functions] = Field(
        description="函数声明与定义。字段值为函数对象的列表，每一项为一个函数的具体定义。")
    steps: Optional[Dict[str, Step]] = Field(description="步骤声明与定义。字段值为步骤对象的列表，供用例对象组织使用；步骤对象也可以直接在用例对象中声明和定义。",
                                             default={})
    cases: Dict[str, Case] = Field(
        description="用例声明与定义。字段值为用例对象的列表，每一项为一个完整可执行的测试用例描述，可供用例集对象组织使用，用例对象也可以直接在用例集对象中声明和定义。",
        default={})
    case_sets: Dict[str, CaseSet] = Field(
        description="用例集声明和定义。字段值为用例集对象或用例对象组成列表，每一项为一个用例集描述，或是一个完整可执行的测试用例描述。用例集对象用于对测试用例进行分类、分层和组织。", default={})


if __name__ == "__main__":
    # tcs = TCS.construct()
    # print(tcs.json())
    print(TCS.schema_json(indent=2))
