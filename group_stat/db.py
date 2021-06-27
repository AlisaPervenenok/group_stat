import sqlite3


DATABASE = "GroupStatistics.db"


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.DatabaseError as e:
        print("Error: ", e)

    return connection


def create_table(connection, create_table_sql):
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.DatabaseError as e:
        print("Error: ", e)


def main():
    database = DATABASE

    sql_create_groups_table = """ CREATE TABLE IF NOT EXISTS "Group" (
                                        "@Group" integer PRIMARY KEY,
                                        "ExternalId" text NOT NULL,
                                        "MembersCount" integer
                                    ); """

    connection = create_connection(database)

    if connection is not None:
        create_table(connection, sql_create_groups_table)
    else:
        print("Ошибка! Невозможно создать соединение с базой")


if __name__ == '__main__':
    main()
