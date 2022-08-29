from settings_reader import *
import tables_creator
import vk_bot

import psycopg2

if __name__ == '__main__':
    # Connect to DB
    conn = psycopg2.connect(database=database, user=user, password=password, port=port, host=host)

    # Clear tables in DB if 'reset_scheme_tables' in settings.ini is 1, if 0 - don't clear
    if reset_scheme_tables == '1':
        tables_creator.reset_scheme_tables(conn)

    # Create tables in DB
    tables_creator.create_tables(conn)


    # Starting bot
    vk_bot.start_bot(vk_group_token, conn)


