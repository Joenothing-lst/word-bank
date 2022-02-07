<div align="center">

# nonebot-plugin-word-bank2

_✨ 无数据库的轻量问答插件 ✨_

</div>

# !!! 注意

由于 [#770](https://github.com/nonebot/nonebot2/issues/770)

因此需要改动nonebot bata1的源码才能正常使用 发送图片功能

`...site-packages/nonebot/adapters/_template.py`

`L178`从

```py
if inspect.ismethod(method):
                formatter = getattr(segment_class, format_spec)
        return (
```
改为

```py
if callable(method):
                formatter = getattr(segment_class, format_spec)
        return (
```

# 功能

- 无数据库的轻量问答插件
- 支持模糊问答
- 支持特殊回复
- 自动转译CQ码
- 支持图片回复
- 支持指令大杂烩

# 安装

```
pip install nonebot-plugin-word-bank2
```


# 开始使用

## 问答教学

- 设置词条命令由`问句`和`答句`组成。设置之后,  收到`消息`时触发。并非所有人都可以设置词条,  详见[权限](#permission)
  
- 格式`[模糊|全局|正则]问...答...`
  - `模糊|全局|正则` 匹配模式中可任性一个或`不选`

- 教学中可以使用换行
  - 例如 
    ```
    问
    123
    答
    456
    ```

- 问答句中的首首尾空白字符会被自动忽略

- 私聊好友个人也可以建立属于自己的词库, 可以实现类似备忘录的功能

### 问句选项

- `问...答...` 全匹配模式, 必须全等才能触发答

- `模糊问...答...` 当`问句`出现在`消息`里时则会触发
  

- `正则问...答...`,  当`问句`被`消息`正则捕获时则会匹配  
- 
    例如: 正则问[他你]不理答你被屏蔽了

    | 消息     | 回复       |
    | -------- | ---------- |
    | 他不理   | 你被屏蔽了 |
    | 他不理我 | 你被屏蔽了 |
    | 你不理我 | 你被屏蔽了 |

- `全局问...答...`,  在所有群聊和私聊中都可以触发,  可以和以上几种组合使用  
  - 例如: `全局模糊问 晚安 答 不准睡`

- 问句可包含`at` 即在QQ聊天中手动at群友
  - 建议只在`问...答...`中使用
  - 例如: `问 @这是群名称 答 老婆!`


###  答句选项

- `/at` + `qq号`, 当答句中包含`/at` + `qq号`时将会被替换为@某人
  - 例如: `问 群主在吗 答 /at 123456789在吗`

- `/self`, 当答句中包含`/self`时将会被替换为发送者的群昵称  
  - 例如: `问 我是谁 答 你是/self` (群昵称为: 我老婆)

- `/atself`, 当答句中包含`/atself`时将会被替换为@发送者
  - 例如: `问 谁是牛头人 答 @这是群昵称`


- `/ban`, 当答句中包含`/ban`后紧跟数字时将会禁言发送者, 单位为秒, 默认为300
  - 例如: `问 牛头人天下第一 答 /ban 114514 ???`

## 删除词条

- 以下指令需要结合自己的`COMMAND_START` 这里为 `/`

- 删除词条+需要删除的`问句`
  - 例如: `/删除词条 你好`

- 删除全局词条+需要删除的`问句`  
  - 例如: `/删除全局词条 你好`

- 删除全局词库
  - 例如: `/删除全局词库`

- 删除全部词库  
  - 例如: `/删除全部词库`

- <span id="permission">权限</span> 

|              | 群主 | 群管理 | 私聊好友 | 超级用户 |
| ------------ | ---- | ------ | -------- | -------- |
| 增删词条     | O    | O      | O        | O        |
| 增删全局词条 | X    | X      | X        | O        |
| 删除词库     | O    | X      | X        | O        |
| 删除全局词库 | X    | X      | X        | O        |
| 删除全部词库 | X    | X      | X        | O        |


# 更新记录

- v0.0.1 
  - 基于fork进行重构


# 特别感谢

- [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot/nonebot2](https://github.com/nonebot/nonebot2)
- [Joenothing-lst/word-bank](https://github.com/Joenothing-lst/word-bank)

# 优化建议

- 请提交issue或者pr
