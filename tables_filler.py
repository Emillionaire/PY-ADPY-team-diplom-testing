import psycopg2


def add_user(conn, result):
    vk_id = result['vk_id']
    name = result['name']
    city = result['city']
    bdate = result['bdate']
    sex = result['sex']
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO person (vk_id, name, city, bdate, sex)
                VALUES (%s, %s, %s, %s, %s)
            ''', (vk_id, name, city, bdate, sex))
            conn.commit()
            return 'Добавил тебя в базу! Теперь ты можешь написать "искать", чтобы запустить поиск знакомств!'
    except psycopg2.errors.UniqueViolation:
        conn.commit()
        return 'Ты уже есть в базе! И можешь приступить к поиску знакомств, напиши "искать"!'


def add_viewed_person(conn, viewed_person_id, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO user_viewed (personid, viewed_id)
                VALUES (%s, %s)
            ''', (user_id, viewed_person_id))
            conn.commit()
    except:
        print(f'Провал записи "просмотренного" {viewed_person_id}, {user_id}')


def add_favorite_person(conn, favorite_person_id, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO user_favorite (personid, favorite_id)
                VALUES (%s, %s)
            ''', (user_id, favorite_person_id))
            conn.commit()
    except:
        print(f'Провал записи "избранного" {favorite_person_id}, {user_id}')


def manual_bdate(conn, bdate, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE person SET bdate = %s WHERE vk_id = %s
            ''', (bdate, user_id))
            conn.commit()
    except:
        print(f'Провал изменения даты рождения {bdate}')
