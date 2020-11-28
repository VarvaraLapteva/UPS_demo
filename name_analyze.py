#!/usr/bin/env python3

import pandas as pd

def guess_gender(name_arr, last_chars=1):
    """ Ввод - список имён и количество последних букв в имени для повышения точности проверки
    Вывод - обращение (Уважаемый/Уважаемая) для каждого из имён в списке

    :param name_arr: Список имён
    :type name_arr: list
    :param last_chars: Количество последних букв для сравнения
    :type last_chars: int
    :return:
    :rtype:
    """
    tmp_names_dict = {"boys": calculate_occurrances(boy_names, last_chars),
                  "girls": calculate_occurrances(girl_names, last_chars)}
    for name in name_arr:
        prefix_name = calculate_name_weight(name, tmp_names_dict, last_chars)
        print(prefix_name + name)


def calculate_occurrances(pd_df, end_length):
    res_dict = {}
    for name in pd_df.index:
        try:
            for endswith in range(-end_length, 0, 1):
                if name.strip()[endswith:] in res_dict.keys():
                    res_dict[name.strip()[endswith:].lower()] += pd_df.loc[name]["NumberOfPersons"]
                else:
                    res_dict[name.strip()[endswith:].lower()] = pd_df.loc[name]["NumberOfPersons"]
        except IndexError:
            pass
    return res_dict


def calculate_name_weight(name, names_dict, last_letters=3):
    """
    Функция проверяет сколько раз последние last_letters (или меньше) букв имени
    встречаются в словаре и высчитывает относительный вес для каждого совпадения.
    Чем больше последних букв - тем выше точность

    :param name: проверяемое имя
    :type name: str
    :param names_dict: словарь имён (муж и жен)
    :type names_dict: dict
    :param last_letters: сколько последних букв имени брать для подсчёта
    :type last_letters: int
    :return: обращение Уважаемый/Уважаемая
    :rtype: str
    """
    test_name = name[-last_letters:].lower() if len(name) > last_letters else name.lower()

    def sub_calculation(tmp_dict, tmp_name):
        name_len = len(tmp_name)
        for x in range(name_len):
            res = tmp_dict.get(tmp_name[x:])
            if res:
                return res, name_len - x
        return 0, 0
    boy_w = sub_calculation(names_dict["boys"], test_name)
    girl_w = sub_calculation(names_dict["girls"], test_name)
    if boy_w[1] > girl_w[1] or (boy_w[1] == girl_w[1] and boy_w[0] > girl_w[0]):
        prefix = "Уважаемый "
    elif girl_w[1] > boy_w[1] or (boy_w[1] == girl_w[1] and boy_w[0] < girl_w[0]):
        prefix = "Уважаемая "
    else:
        prefix = "Неведомая тварь "
    return prefix


girls = pd.read_csv("demography/Girls.csv", sep=";")
girl_names = girls[["Name", "NumberOfPersons"]].groupby("Name").sum()

boys = pd.read_csv("demography/Boys.csv", sep=";")
boy_names = boys[["Name", "NumberOfPersons"]].groupby("Name").sum()

names_dict = {"boys": calculate_occurrances(boy_names, 1),
              "girls": calculate_occurrances(girl_names, 1)}

boys_ordered = [(x, names_dict["boys"][x]) for x in sorted(names_dict["boys"].keys())]
girls_ordered = [(x, names_dict["girls"][x]) for x in sorted(names_dict["girls"].keys())]
#
#
result_columns = ["Letter", "Boys", "Girls"]
boys_df = pd.DataFrame(boys_ordered, columns=["Letter", "Boys"])
girls_df = pd.DataFrame(girls_ordered, columns=["Letter", "Girls"])
result = boys_df.merge(girls_df, how='outer').fillna(0).sort_values("Letter", axis=0).set_index("Letter")
print(result.to_string())

# Для тестирования берём последние три буквы
name_arr = ["Бек", "Гюльчатай", "Мамед", "Катирута", "Алибек", "Яндырбай", "Илья", "Николай",
            "Ильяс", "Ия", "Ая", "Зоя", "Немезиди", "Сергей", "Ёж", "Александр"]
guess_gender(sorted(name_arr), 3)
