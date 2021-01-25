# nonebot-plugin-wordbank

- 基于[nonebot2](https://github.com/nonebot/nonebot2)

## 功能

- 无数据库的轻量问答插件
- 支持模糊问答

## 开始使用

必须使用 pip

- 通过 pip 从 [PyPI](https://pypi.org/project/nonebot_plugin_wordbank/) 安装

``` {.sourceCode .bash}
pip install nonebot-plugin-wordbank
```

## 使用方式

- 问xxx答xxx
- 模糊问xxx答xxx
- 全局问xxx答xxx
- 全局模糊问xxx答xxx
- 删除词条xxx

## 导出给其他插件

```python
from nonebot import require

wb = require("nonebot_plugin_wordbank").word_bank
```

## 更新记录

## 特别感谢

- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)

## 优化建议
- 请提交issue或者pr
