import json
import os
from typing import Union, List


NULL_BANK = dict(congruence={
    0: dict()
}, include={
    0: dict()
})


class WordBank(object):

    def __init__(self):
        self.dir_path = os.path.abspath(os.path.join(__file__, "..", "data"))
        self.data_path = os.path.join(self.dir_path, "bank.json")

        if os.path.exists(self.dir_path):
            print('读取词库位于 ' + self.data_path)
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.__data = json.load(f)
        else:
            os.mkdir(self.dir_path)
            print('创建词库位于 ' + self.data_path)
            self.__data = NULL_BANK
            self.__save()

    def match(self, index: int, msg: str, flags: int = 0) -> Union[None, List]:
        """
        匹配词条

        :param index: 为0时是全局词库
        :param msg:
        :param flags: 为1时为允许模糊匹配（in）， 默认为全匹配（==）
        :return:
        """
        if isinstance(index, int):
            index = str(index)
        reply = self.__data['congruence'].get(index, {}).get(msg, []) \
                or self.__data['congruence'].get('0', {}).get(msg, [])

        if not flags or reply:
            return reply
        else:
            for key in self.__data['include'].get(index, {}):
                if key in msg:
                    return self.__data['include'][index][key]

            for key in self.__data['include'].get('0', {}):
                if key in msg:
                    return self.__data['include']['0'][key]

    def __save(self):
        """
        :return:
        """
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(self.__data, f)

    def set(self, index: int, key: str, value: str, flags: int = 0) -> bool:
        """
        新增词条

        :param index: 为0时是全局词库
        :param key:
        :param value:
        :param flags: 为1时是模糊匹配（in）， 默认为全匹配（==）
        :return:
        """
        index = str(index)
        options = ['congruence', 'include']
        flag = options[flags]

        if self.__data[flag].get(index, {}):
            if self.__data[flag][index].get(key, []):
                self.__data[flag][index][key].append(value)
            else:
                self.__data[flag][index][key] = [value]
        else:
            self.__data[flag][index] = {key: [value]}
        self.__save()
        return True

    def delete(self, index: int, key: str) -> bool:
        """
        删除词条

        :param index: 为0时是全局词库
        :param key:
        :return:
        """
        index = str(index)
        if self.__data['congruence'].get(index, {}).get(key, False):
            del self.__data['congruence'][index][key]
            self.__save()
            return True

        elif self.__data['include'].get(index, {}).get(key, False):
            del self.__data['include'][index][key]
            self.__save()
            return True

        return False

    def clean(self, index: int) -> bool:
        """
        清空某个对象的词库

        :param index: 为0时是全局词库
        :return:
        """
        index = str(index)
        if self.__data.get(index, {}):
            del self.__data[index]
            self.__save()
            return True
        return False

    def _clean_all(self):
        """
        清空所有词库

        :return:
        """
        self.__data = NULL_BANK
        self.__save()
        return True


word_bank = WordBank()
