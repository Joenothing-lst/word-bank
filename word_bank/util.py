import re

from typing import Optional


def parse_cmd(pattern, msg: str) -> list:
    return re.findall(pattern, msg, re.S)


def parse_at(msg: str) -> str:
    return re.sub(r'/at(\d+)', r'[CQ:at,qq=\1]', msg)


def parse_self(msg: str, **kwargs) -> str:
    return parse_at_self(re.sub(r'/self', str(kwargs.get('nickname', '')), msg), **kwargs)


def parse_at_self(msg: str, **kwargs) -> str:
    sender_id = kwargs.get('sender_id', '')
    if sender_id:
        return re.sub(r'/atself', f"[CQ:at,qq={sender_id}]", msg)
    else:
        return msg


def parse_ban(msg: str) -> Optional[int]:
    matcher = re.findall(r'/ban([ \d]*)', msg)
    if matcher:
        duration = matcher[0]
        # 默认 5 分钟
        return int(duration.strip() or 300)


def parse(msg, **kwargs) -> str:
    return parse_at(parse_self(msg, **kwargs))
