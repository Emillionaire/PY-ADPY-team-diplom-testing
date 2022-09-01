# функция создания таблицы для подходящих пользователей
def create_tables(conn):
    user_relevant = '''
        CREATE TABLE IF NOT EXISTS user_relevant(
        ID SERIAL PRIMARY KEY,
        person_vk_id INT NOT NULL,
        rel_person_vk_id INT NOT NULL
        );
    '''
    with conn.cursor() as cursor:
        cursor.execute(user_relevant)
        conn.commit()

# фунцкия добавления всех подходящих пользователей в БД
def add_relevant_user(conn, person_id, rel_list):
    for i in rel_list:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO user_relevant (person_vk_id, rel_person_vk_id)
                VALUES (%s, %s)
            ''', person_id, i)
            conn.commit()


# функция получения всех подходящих пользователей из БД
def take_relevant_user(conn, person_id):
    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM user_relevant WHERE person_vk_id = %s
        ''', (person_id,))
        conn.commit
        result = cursor.fetchall()
    return result


# фунцкия получения всех просмотренных пользователей из БД
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


# функция получения не просмотренных пользователей из подходящих
def subtracting(rel_person, viewed_person):
    result = [i for i in rel_person if i not in viewed_person]
    return result
