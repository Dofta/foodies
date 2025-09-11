#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from foodies.models.v1_0.input import Input
from foodies.models.v1_0.output import Output


class Function(BaseModel):
    name: str = Field(
        description="函数名。当函数类型为 builtin 时，函数名必须存在于通用插件库中；当函数类型为 user-def 时，可以直接以文本形式提供函数，或提供可读取到函数内容的外部引用。")
    type: str = Field(description=" 区分函数的类型，目前取值范围仅两种：builtin、user-def。")
    language: str = Field(description=" 声明函数使用的编程语言，缺省为 python。", default="python")
    input: Optional[Dict[str, Input]] = Field(description="函数的输入，为一个输入对象声明的列表。")
    output: Optional[Dict[str, Output]] = Field(description="函数的输入，为一个输入对象声明的列表。")
    content: Optional[str] = Field(description="为一段文本形式直接提供的函数代码，或一个指向函数内容的外部引用。")
    timeout: int = Field(description="指明函数在执行超过 timeout 时间的情况下直接停止并抛出超时异常，单位为秒，缺省值 60。", default=60)
    tags: Optional[List[str]] = Field(description="为一个文本标签列表，方便为函数增加标签进行统计和分类。")
