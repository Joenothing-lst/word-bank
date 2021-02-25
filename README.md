<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-wordbank

_✨ 无数据库的轻量问答插件 ✨_

</div>

<p align="center">
  <a href="https://github.com/Joenothing-lst/word-bank/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Joenothing-lst/word-bank.svg" alt="license">
  </a>
  <a href="https://pypi.org/project/nonebot-plugin-wordbank/">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-wordbank.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="python">
</p>


- 基于[nonebot2](https://github.com/nonebot/nonebot2)

## 功能

- 无数据库的轻量问答插件
- 支持模糊问答
- 支持特殊回复
- 自动转译CQ码

## 安装

必须使用 `pip`

- 通过`pip`从 [PyPI](https://pypi.org/project/nonebot_plugin_wordbank/) 安装

``` {.sourceCode .bash}
pip install nonebot-plugin-wordbank
```


## 开始使用
- 使用方法：

    * 设置词条命令由`问句`和`答句`组成。设置之后，收到`消息`时触发。并非所有人都可以设置词条，详见[权限](#permission)
    
    * `问句`及其关键字
    
        * 问，当`问句`和`消息`全等时才会匹配  
        例子：问他不理答你被屏蔽了
        
            | 消息 | 回复 |
            | --- | --- |
            | 他不理 | 你被屏蔽了 |
            | 他不理我 | - |
            | 你不理我 | - |
            
        * 模糊问，当`问句`出现在`消息`里时则会匹配  
        例子：模糊问他不理答你被屏蔽了
        
            | 消息 | 回复 |
            | --- | --- |
            | 他不理 | 你被屏蔽了 |
            | 他不理我 | 你被屏蔽了 |
            | 你不理我 | - |
           
        * 正则问，当`问句`被`消息`正则捕获时则会匹配  
        例子：正则问[他你]不理答你被屏蔽了
        
            | 消息 | 回复 |
            | --- | --- |
            | 他不理 | 你被屏蔽了 |
            | 他不理我 | 你被屏蔽了 |
            | 你不理我 | 你被屏蔽了 |
            
        * 全局问，在所有群聊和私聊中都可以触发，可以和以上几种组合使用  
        例子：全局模糊问不理我答你被屏蔽了
            
    * `答句`  
    
        * `/at` + `qq号`，当答句中包含`/at` + `qq号`时将会被替换为@某人（即`CQ码`）  
        例子：问群主在吗答/at123456789在吗  
            
            | 群主qq号 | 消息 | 回复 |
            | --- | --- | --- |
            | 123456789 | 群主在吗 | @群主 在吗 |
        
        * `/self`，当答句中包含`/self`时将会被替换为发送者的群昵称  
        例子：问你好答/self你好啊  
        
            | 发送者 | 消息 | 回复 |
            | --- | --- | --- |
            | 皆无 | 你好 | 皆无你好啊 |
            
        * `/atself`，当答句中包含`/atself`时将会被替换为@发送者
        例子：问你好答/atself你好啊  
        
            | 发送者 | 消息 | 回复 |
            | --- | --- | --- |
            | 皆无 | 你好 | @皆无你好啊 |
    
    * 删除 
        * 删除词条+需要删除的`问句`  
        例子：删除词条你好
        
        * 删除全局词条+需要删除的`问句`  
        例子：删除全局词条你好
        
        * 删除全局词库  
        例子：删除全局词库  
        
        * 删除全部词库  
        例子：删除全部词库
    
    * <span id="permission">权限</span> 
    
        |  | 群主 | 群管理 | 私聊好友 | 超级用户 |
        | --- | --- | --- | --- | --- |
        | 增删词条 | O | O | O | O |
        | 增删全局词条 | X | X | X | O |
        | 删除词库 | O | X | X | O |
        | 删除全局词库 | X | X | X | O |
        | 删除全部词库 | X | X | X | O |
        
        注：私聊好友个人也可以建立属于自己的词库，与群词库是同级且独立的。
 
- 开发者使用：

``` python
from nonebot_plugin_wordbank import wb
```

## 配置项

- `reply_type`可以选择回复类型，随机在回答中返回一个 或 返回所有回答，默认为前者`random`。
- 若需要更改`reply_type`，使用如下代码：
``` python
import nonebot_plugin_wordbank

nonebot_plugin_wordbank.reply_type = "all"
```


## 导出给其他插件

``` python
from nonebot import require

wb = require("nonebot_plugin_wordbank").export()
```

## 更新记录

* V1.0.1
    * 修复正则词条可能会被转义的bug。
    * 修复全局词条可能不会正确响应的bug。
    * 修复词库路径错误的bug。

* V1.0.0
    * 修复了一些BUG，丰富了基础功能。

## 特别感谢

- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)

## 优化建议
- 请提交issue或者pr