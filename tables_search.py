import psycopg2
from psycopg2.extras import DictCursor


def take_user_data(conn, user_id):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('''
            SELECT * FROM person WHERE vk_id = %s
        ''', (user_id,))
        conn.commit()
        result = cursor.fetchone()
        result_dict = {
            'vk_id': result['vk_id'],
            'name': result['name'],
            'city': result['city'],
            'bdate': result['bdate'],
            'sex': result['sex']
        }
        return result_dict


def take_user_favorites(conn, user_id):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('''
            SELECT * FROM user_favorite WHERE personid = %s
        ''', (user_id,))
        conn.commit()
        result = cursor.fetchall()
        favorite_list = []
        for i in result:
            favorite_list.append(f'https://vk.com/id{i[2]}')
        return favorite_list


def take_user_viewed(conn, user_id):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('''
            SELECT * FROM user_viewed WHERE personid = %s
        ''', (user_id,))
        conn.commit()
        result = cursor.fetchall()
        viewed_list = []
        for i in result:
            viewed_list.append(i[2])
        return viewed_list
