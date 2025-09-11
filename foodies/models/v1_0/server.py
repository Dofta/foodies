#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, Dict, List

from pydantic import BaseModel, Field


class Server(BaseModel):
    type: str = Field(description="描述变量类型，取值范围包括纯量包含的数据类型，以及 map 和 list。缺省为 string。", default="string")
    value: str = Field(description="服务端URI")
    env: str = Field(description="环境类型，取值范围为：prod、test、dev、pre", default='test')
    description: Optional[str] = Field(description="提供该环境的一些介绍和描述。")
    labels: Optional[List[Dict]] = Field(description="以键值对列表的形式提供一些追加的标签值。")
