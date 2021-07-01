CREATE_TEST_TABLE = """ CREATE TABLE IF NOT EXISTS "Group" (
                                    "@Group" integer PRIMARY KEY,
                                    "ExternalId" text NOT NULL,
                                    "MembersCount" integer
                                ); """

DROP_TEST_TABLE = """ DROP TABLE IF EXISTS "Group" """