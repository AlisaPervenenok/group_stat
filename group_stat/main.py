""" Скрипт сбора статистики по группам """
import vk_api

from group_list import GroupList
from group import Group
from db import SqlQuery
from statistics import GroupStatistics

token = '14d8df3314d8df3314d8df33a014a0be00114d814d8df33740fe8d5e060c40f4e783807'

DEFAULT_EXTERNAL_IDS = (
    'rambler', 'ramblermail', 'horoscopesrambler', 'championat', 'championat.auto', 'championat_cybersport',
    'livejournal', 'afisha'
)


def main():

    sql_create_groups_table = """ CREATE TABLE IF NOT EXISTS "Group" (
                                        "@Group" integer PRIMARY KEY,
                                        "ExternalId" text NOT NULL,
                                        "MembersCount" integer
                                    ); """

    SqlQuery(sql_create_groups_table)

    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    group_list = GroupList()
    group_list_result = group_list.get()

    if not group_list_result:
        for external_id in DEFAULT_EXTERNAL_IDS:
            group = Group({'ExternalId': external_id})
            group.upsert()
        # TODO:  в 32 версии SQLite отсутствует RETURNING
        group_list = GroupList()
        group_list_result = group_list.get()

    # TODO: Найти способ сразу получать словарь из execute, а не список кортежей
    for group in group_list_result:
        members_dict = vk.groups.getMembers(group_id=group[1])
        members_count = members_dict['count']
        stat_dict = {
             '@Group': group[0],
             'MembersCount': members_count
        }
        statistics = GroupStatistics(stat_dict)
        statistics.update()


if __name__ == '__main__':
    main()
