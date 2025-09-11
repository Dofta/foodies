#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, List, Any, Dict, Union

from pydantic import BaseModel, Field, Extra


class Params(BaseModel):
    path: Optional[List[Union[str, Dict]]] = Field(description="一个由字符串和键值对构成的列表，第一项始终为请求路径，其中路径上的参数以 {xxx} 表示，第二项开始声明了这些参数的具体值。")
    summary: Optional[str] = Field(description="一段文本作为测试用例的简介。")
    test_type: Optional[str] = Field(description="描述测试用例的测试类型。")
    automatable: bool = Field(description="是否支持自动化执行。当值为 true 时，该文档内容理论上可以被相关自动化测试框架工具读取并直接执行；缺省值为 false。",
                              default=False)
    author: Optional[List[str]] = Field(description="为文档的作者或共同作者。当测试用例为通过 OAS 工具自动生成的内容时，值为 ['oas']。")
    version: Optional[str] = Field(description="描述测试用例的版本号。")
