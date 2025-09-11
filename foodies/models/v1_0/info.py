#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, List

from pydantic import BaseModel, Field, Extra


class Info(BaseModel):
    class Config:
        extra = Extra.allow

    title: str = Field(description="该份测试用例文档的标题。缺省值使用根节点的测试用例集名称。")
    summary: Optional[str] = Field(description="一段文本作为测试用例的简介。")
    test_type: Optional[str] = Field(description="描述测试用例的测试类型。")
    automatable: bool = Field(description="是否支持自动化执行。当值为 true 时，该文档内容理论上可以被相关自动化测试框架工具读取并直接执行；缺省值为 false。",
                              default=False)
    author: Optional[List[str]] = Field(description="为文档的作者或共同作者。当测试用例为通过 OAS 工具自动生成的内容时，值为 ['oas']。", default=[''])
    version: Optional[str] = Field(description="描述测试用例的版本号。")
