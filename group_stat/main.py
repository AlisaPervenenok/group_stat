import vk_api
import sqlite3
from group_stat import constants

token = '14d8df3314d8df3314d8df33a014a0be00114d814d8df33740fe8d5e060c40f4e783807'
group_ids = [
    'rambler', 'ramblermail', 'horoscopesrambler', 'championat', 'championat.auto', 'championat_cybersport', 'livejournal', 'afisha'
]


def add_groups(GROUP_IDS):
    connection = sqlite3.connect('GroupStatistics.db')
    cursor = connection.cursor()
    result = []
    try:
        for group in GROUP_IDS:
            cursor.execute(""" INSERT INTO "Group" ("ExternalId") VALUES (?) """, [group])
            fetch_result = cursor.fetchall()
            result.append(fetch_result)

    except sqlite3.DatabaseError as e:
        print("Error: ", e)
    else:
        connection.commit()
        connection.close()

        return result


def get_group_list(filter_obj=None):
    connection = sqlite3.connect('GroupStatistics.db')
    cursor = connection.cursor()

    if filter_obj:
        filter_obj = prepare_filter(filter_obj)

    sql_get_group_list = prepare_query(filter_obj)

    try:
        cursor.execute(sql_get_group_list)
        result = cursor.fetchall()
    except sqlite3.DatabaseError as e:
        print("Error: ", e)
    else:
        connection.commit()
        connection.close()
        return result


def prepare_filter(_filter):
    if not isinstance(_filter, dict):
        raise Warning(
            "Передан некорректный тип параметра - фильтр списочного метода get_group_list должен иметь тип dict!"
        )
    for key, value in _filter.items():
        if key not in constants.GROUP_FILTER_DICT:
            _filter.pop(key)
        expected_field_type = constants.GROUP_FILTER_DICT[key]
        if not isinstance(value, expected_field_type):
            raise Warning(
                f"Передан некорректный тип поля {key}, ожидается {expected_field_type}")
    return _filter


def prepare_query(_filter):
    GET_GROUP_LIST_BASE = """ SELECT "@Group", "ExternalId" FROM "Group" """
    WHERE_BASE = """ WHERE "@Group" IS NOT NULL """
    if _filter:
        for key, value in _filter.items():
            # TODO: плохо, придумать другой способ формирования динамического запроса
            WHERE_BASE += f""", {key} = ANY({value})"""
    return GET_GROUP_LIST_BASE + WHERE_BASE


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()

    group_list = get_group_list()
    if not group_list:
        add_groups(GROUP_IDS)
        group_list = get_group_list()
    #TODO: Найти способ сразу получать словарь из execute, а не список кортежей
    for group in group_list:
        members_dict = vk.groups.getMembers(group_id=group[1])
        members_count = members_dict['count']
        stat_dict = {
             '@Group': group[0],
             'MembersCount': members_count
        }
        update_group_stat(stat_dict)


def update_group_stat(stat_dict):
    connection = sqlite3.connect('GroupStatistics.db')
    cursor = connection.cursor()
    group = stat_dict.get('@Group')
    members_count = stat_dict.get('MembersCount')

    try:
        cursor.execute(""" UPDATE "Group" SET "MembersCount"=? WHERE "@Group"=? """, [members_count, group])
        cursor.fetchall()

    except sqlite3.DatabaseError as e:
        print("Error: ", e)
    else:
        connection.commit()
        connection.close()


def get_stat():
    connection = sqlite3.connect('GroupStatistics.db')
    cursor = connection.cursor()
    try:
        cursor.execute(""" SELECT * FROM "Group" """)
        result = cursor.fetchall()

    except sqlite3.DatabaseError as e:
        print("Error: ", e)
    else:
        connection.commit()
        connection.close()

        return result


if __name__ == '__main__':
    main()


