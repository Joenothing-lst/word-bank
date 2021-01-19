import re
import random

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.utils import unescape

from .data_source import word_bank as wb

wb_matcher = on_message(priority=99)


@wb_matcher.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = wb.match(event.user_id, event.raw_message, flags=1)
    if msg:
        await bot.send(event, message=unescape(random.choice(msg)))


wb_set_cmd = on_command('问', aliases={'全局问', '全局模糊问', '模糊问', })

@wb_set_cmd.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = event.raw_message
    if isinstance(event, GroupMessageEvent):
        index = event.group_id
    else:
        index = event.user_id

    kv = re.findall('([模糊全局]*)问(.*?)答(.*)', msg, re.S)
    if kv:
        flag, key, value = kv[0]
        res = wb.set(0 if '全局' in flag else index,
                     key,
                     value,
                     flags=int('模糊' in flag))
        if res:
            await bot.send(event, message='我记住了~')
    else:
        await bot.send(event, message='格式错误')


wb_del_cmd = on_command('删除词条')

@wb_del_cmd.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = event.message.__str__()
    res = wb.delete(event.user_id, msg)
    if res:
        await bot.send(event, message='删除成功~')
