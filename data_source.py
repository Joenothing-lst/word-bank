import json
import os


NULL_BANK = {
    'congruence': {
        0: {}
    },
    'include': {
        0: {}
    }
}


class WordBank():

    def __init__(self):
        self.dir_path = os.path.abspath(os.path.join(__file__, "..", "./bank.json"))
        if os.path.exists(self.dir_path):
            print('读取词库位于 ' + self.dir_path)
            with open(self.dir_path, 'r') as f:
                self.__data = json.load(f)
        else:
            print('创建词库位于 ' + self.dir_path)
            self.__data = NULL_BANK
            self.__save()

    def match(self, index: int, msg: str, flags=0):
        """
        匹配词条

        :param index: 为0时是全局词库
        :param key:
        :param flags: 为1时为允许模糊匹配（in）， 默认为全匹配（==）
        :return:
        """
        index = str(index)
        reply = self.__data['congruence'].get(index, {}).get(msg, [])

        if not flags or reply:
            return reply
        else:
            for key in self.__data['include'].get(index, {}):
                if key in msg:
                    return self.__data['include'][index][key]

    def __save(self):
        """
        :return:
        """
        with open(self.dir_path, 'w') as f:
            json.dump(self.__data, f)

    def set(self, index: int, key: str, value: str, flags=0):
        """
        新增词条

        :param index: 为0时是全局词库
        :param key:
        :param value: 为1时是模糊匹配（in）， 默认为全匹配（==）
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

    def delete(self, index: int, key: str):
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

    def clean(self, index: int):
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
