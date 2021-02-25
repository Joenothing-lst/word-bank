import json
import os
import re

from typing import Optional, Union, List


OPTIONS = ['congruence', 'include', 'regex']

NULL_BANK = dict((option, {"0": {}}) for option in OPTIONS)


class WordBank(object):

    def __init__(self):
        self.dir_path = os.path.abspath(os.path.join(__file__, "..", "data"))
        self.data_path = os.path.join(self.dir_path, "bank.json")

        if os.path.exists(self.data_path):
            print('读取词库位于 ' + self.data_path)
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.__data = {key: data.get(key) or {"0": {}} for key in NULL_BANK.keys()}

        else:
            os.mkdir(self.dir_path)
            print('创建词库位于 ' + self.data_path)
            self.__data = NULL_BANK
            self.__save()

    def match(self, index: Union[int, str], msg: str, flags: int = 0) -> Optional[List]:
        """
        匹配词条

        :param index: 为0时是全局词库
        :param msg: 需要匹配的消息
        :param flags:   0: 无限制（默认）
                        1: 全匹配（==）
                        2: 模糊匹配（in）
                        3: 正则匹配（regex）
        :return: 首先匹配成功的消息列表
        """
        if flags:
            return self._match(index, msg, flags)

        else:
            for type_ in range(1, len(self.__data)+1):
                re_msg = self._match(index, msg, type_)
                if re_msg:
                    return re_msg

    def _match(self, index: Union[int, str], msg: str, flags: int = 1) -> Optional[List]:
        """
        匹配词条

        :param index: 为0时是全局词库
        :param msg: 需要匹配的消息
        :param flags:   1: 全匹配（==）
                        2: 模糊匹配（in）
                        3: 正则匹配（regex）
        :return: 首先匹配成功的消息列表
        """

        if isinstance(index, int):
            index = str(index)

        type_ = OPTIONS[flags-1]
        bank = dict(self.__data[type_].get(index, {}), **self.__data[type_].get("0", {}))

        if flags == 1:
            return bank.get(msg, [])

        elif flags == 2:
            for key in bank:
                if key in msg:
                    return bank[key]

        elif flags == 3:
            for key in bank:
                try:
                    if re.search(key, msg, re.S):
                        return bank[key]
                except re.error:
                    print(f'正则匹配错误 - pattern: {key}, string: {msg}')

    def __save(self):
        """
        :return:
        """
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, ensure_ascii=False, indent=4)

    def set(self, index: Union[int, str], key: str, value: str, flags: int = 1) -> bool:
        """
        新增词条

        :param index: 为0时是全局词库
        :param key: 触发短语
        :param value: 触发后发送的短语
        :param flags:   1: 全匹配（==）
                        2: 模糊匹配（in）
                        3: 正则匹配（regex）
        :return:
        """
        index = str(index)
        flag = OPTIONS[flags-1]

        if self.__data[flag].get(index, {}):
            if self.__data[flag][index].get(key, []):
                self.__data[flag][index][key].append(value)
            else:
                self.__data[flag][index][key] = [value]
        else:
            self.__data[flag][index] = {key: [value]}

        self.__save()
        return True

    def delete(self, index: Union[int, str], key: str) -> bool:
        """
        删除词条

        :param index: 为0时是全局词库
        :param key: 触发短语
        :return:
        """
        index = str(index)
        flag = False

        for type_ in self.__data:
            if self.__data[type_].get(index, {}).get(key, False):
                del self.__data[type_][index][key]
                flag = True

        self.__save()
        return flag

    def clean(self, index: Union[int, str]) -> bool:
        """
        清空某个对象的词库

        :param index: 为0时是全局词库
        :return:
        """
        index = str(index)
        flag = False

        for type_ in self.__data:
            if self.__data[type_].get(index, {}):
                del self.__data[type_][index]
                flag = True

        self.__save()
        return flag

    def _clean_all(self):
        """
        清空所有词库

        :return:
        """
        self.__data = NULL_BANK
        self.__save()
        return True


word_bank = WordBank()
