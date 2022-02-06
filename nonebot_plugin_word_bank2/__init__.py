import random

from nonebot import export, on_command, on_message, on_regex
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.adapters.onebot.v11.permission import (
    GROUP_ADMIN,
    GROUP_OWNER,
    PRIVATE_FRIEND,
)
from nonebot.adapters.onebot.v11.utils import unescape
from nonebot.log import logger
from nonebot.params import CommandArg, State
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from .data_source import word_bank as wb
from .util import (
    get_message_img,
    parse_ban_msg,
    parse_ban_time,
    parse_cmd,
)

reply_type = "random"

export().word_bank = wb

wb_matcher = on_message(priority=99)


@wb_matcher.handle()
async def handle_wb(bot: Bot, event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        index = event.group_id
    else:
        index = event.user_id

    msgs = wb.match(index, unescape(event.raw_message))
    if msgs and reply_type == "random":

        msg = random.choice(msgs)
        duration = parse_ban_time(msg)

        if duration and isinstance(event, GroupMessageEvent):
            msg = parse_ban_msg(msg)
            await bot.set_group_ban(
                group_id=event.group_id,
                user_id=event.user_id,
                duration=duration,
            )

        await wb_matcher.finish(
            await wb.parse_msg(
                msg=msg,
                nickname=event.sender.card or event.sender.nickname,
                sender_id=event.sender.user_id,
            )
        )

    elif msgs and reply_type != "random":
        for msg in msgs:
            duration = parse_ban_time(msg)
            if duration and isinstance(event, GroupMessageEvent):
                msg = parse_ban_msg(msg)
                await bot.set_group_ban(
                    group_id=event.group_id,
                    user_id=event.user_id,
                    duration=duration,
                )

            await wb_matcher.finish(
                await wb.parse_msg(
                    msg=msg,
                    nickname=event.sender.card or event.sender.nickname,
                    sender_id=event.sender.user_id,
                ),
            )
    else:
        await wb_matcher.finish()


wb_set_cmd = on_regex(
    r"^(?:全局|模糊|正则)*问",
    permission=GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND | SUPERUSER,
)


@wb_set_cmd.handle()
async def wb_set(bot: Bot, event: MessageEvent):

    if isinstance(event, GroupMessageEvent):
        index = event.group_id
    else:
        index = event.user_id

    pic_data = get_message_img(event.json())
    kv = parse_cmd(r"([模糊全局正则]*)问\s?(.+?)\s?答\s?(.+)", event.raw_message)

    if kv and not pic_data:
        flag, key, value = kv[0]
        type_ = 3 if "正则" in flag else 2 if "模糊" in flag else 1

        res = wb.set(0 if "全局" in flag else index, unescape(key), value, type_)

        if res:
            await wb_set_cmd.finish(message="我记住了~")
    elif kv and pic_data and ("CQ:image" not in kv[0][1]):
        # 如果回答中含有图片 则保存图片 并将图片替换为 /img xxx.image
        flag, key, value = kv[0]
        value = await wb.convert_and_save_img(pic_data, value)
        type_ = 3 if "正则" in flag else 2 if "模糊" in flag else 1

        res = wb.set(0 if "全局" in flag else index, unescape(key), value, type_)
        if res:
            await wb_set_cmd.finish(message="我记住了~")


wb_del_cmd = on_command(
    "删除词条",
    permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | PRIVATE_FRIEND,
)


@wb_del_cmd.handle()
async def wb_del_(event: MessageEvent, arg: Message = CommandArg()):
    logger.debug(isinstance(event, GroupMessageEvent))

    if isinstance(event, GroupMessageEvent):
        index = event.group_id
    else:
        index = event.user_id

    logger.debug(index)

    msg = arg.extract_plain_text()

    logger.debug(msg)
    res = wb.delete(index, unescape(msg))
    if res:
        await wb_del_cmd.finish(message="删除成功~")


wb_del_admin = on_command(
    "删除全局词条",
    permission=SUPERUSER,
)


@wb_del_admin.handle()
async def wb_del_admin_(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        res = wb.delete(0, unescape(msg))
        if res:
            await wb_del_admin.finish(message="删除成功~")


async def wb_del_all(
    event: MessageEvent, state: T_State = State(), arg: Message = CommandArg()
):
    msg = arg.extract_plain_text().strip()
    if msg:
        state["is_sure"] = msg


wb_del_all_cmd = on_command(
    "删除词库", permission=SUPERUSER | GROUP_OWNER | PRIVATE_FRIEND, handlers=[wb_del_all]
)
wb_del_all_admin = on_command("删除全局词库", permission=SUPERUSER, handlers=[wb_del_all])
wb_del_all_bank = on_command("删除全部词库", permission=SUPERUSER, handlers=[wb_del_all])


@wb_del_all_cmd.got("is_sure", prompt="此命令将会清空您的群聊/私人词库，确定请发送 yes")
async def wb_del_all_(event: MessageEvent, state: T_State = State()):
    is_sure: Message = state["is_sure"]
    if is_sure.extract_plain_text() == "yes":

        if isinstance(event, GroupMessageEvent):
            res = wb.clean(event.group_id)
            if res:
                await wb_del_all_cmd.finish("删除群聊词库成功~")

        else:
            res = wb.clean(event.user_id)
            if res:
                await wb_del_all_cmd.finish("删除个人词库成功~")

    else:
        await wb_del_all_cmd.finish("命令取消")


@wb_del_all_admin.got("is_sure", prompt="此命令将会清空您的全局词库，确定请发送 yes")
async def wb_del_all_admin_(event: MessageEvent, state: T_State = State()):
    is_sure: Message = state["is_sure"]
    if is_sure.extract_plain_text() == "yes":
        res = wb.clean(0)
        if res:
            await wb_del_all_admin.finish("删除全局词库成功~")

    else:
        await wb_del_all_admin.finish("命令取消")


@wb_del_all_bank.got("is_sure", prompt="此命令将会清空您的全部词库，确定请发送 yes")
async def wb_del_all_bank_(bot: Bot, event: MessageEvent, state: T_State = State()):
    is_sure: Message = state["is_sure"]
    if is_sure.extract_plain_text() == "yes":
        res = wb._clean_all()

        if res:
            await wb_del_all_bank.finish("删除全部词库成功~")

    else:
        await wb_del_all_bank.finish("命令取消")
