""" Скрипт сбора статистики по группам VK """
import vk_api
import group_stat
import db

token = '14d8df3314d8df3314d8df33a014a0be00114d814d8df33740fe8d5e060c40f4e783807'

DEFAULT_EXTERNAL_IDS = (
    'rambler', 'ramblermail', 'horoscopesrambler', 'championat', 'championat.auto', 'championat_cybersport',
    'livejournal', 'afisha'
)

CREATE_GROUP_TABLE = """ CREATE TABLE IF NOT EXISTS "Group" (
                                    "@Group" integer PRIMARY KEY,
                                    "ExternalId" text NOT NULL,
                                    "MembersCount" integer
                                ); """


def get_vk_group_statistics(vk):

    if not vk:
        raise Warning('Для получения статистики групп VK требуется авторизация по сервисному ключу доступа')

    group_list = group_stat.GroupList()
    group_list_result = group_list.get()

    if not group_list_result:
        for external_id in DEFAULT_EXTERNAL_IDS:
            group = group_stat.Group({'ExternalId': external_id})
            group.upsert()

        group_list = group_stat.GroupList()
        group_list_result = group_list.get()

    for group in group_list_result:
        members_dict = vk.groups.getMembers(group_id=group[1])
        members_count = members_dict['count']
        stat_dict = {
             '@Group': group[0],
             'MembersCount': members_count
        }
        statistics = group_stat.GroupStatistics(stat_dict)
        statistics.update()


def create_group_table():
    return db.SqlQuery(CREATE_GROUP_TABLE)


def vk_auth():
    vk_session = vk_api.VkApi(token=token)
    return vk_session.get_api()


if __name__ == '__main__':
    create_group_table()
    vk = vk_auth()
    get_vk_group_statistics(vk)


