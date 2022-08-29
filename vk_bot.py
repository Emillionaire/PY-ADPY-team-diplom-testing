from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import tables_filler
import tables_search
import vk_get_another_people
import vk_get_user_info


def start_bot(token, conn):
    vk = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk)
    count = 0

    def write_msg(user_id, message):
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text
                try:
                    if int(request) in range(1900, 2008):
                        tables_filler.manual_bdate(conn, request, event.user_id)
                        write_msg(event.user_id,
                                  f'Спасибо, я вписал {request} как твой год рождения. Теперь ты можешь написать "искать" и приступить к подбору знакомств!')

                except ValueError:
                    if request == 'привет':
                        write_msg(event.user_id,
                                  f'Привет, пользователь! Чтобы начать поиск новых друзей нужно добавить тебя в базу. Напиши "добавь"!')

                    elif request == 'добавь':
                        result = vk_get_user_info.get_user_info(event.user_id)
                        show_wrong = 0
                        if result['bdate'] == 0:
                            show_wrong = 1
                        if result['city'] == 1:
                            write_msg(event.user_id, 'Я не смог распознать твой город, поэтому буду искать для тебя людей из Москвы!')
                        result = tables_filler.add_user(conn, result)
                        write_msg(event.user_id, result)
                        if show_wrong == 1:
                            write_msg(event.user_id,
                                      'Я не смог распознать твой год рождения. Напиши его сейчас в чат в формате четырех цифр (например: 2003)!')


                    elif request == 'искать':
                        result = vk_get_another_people.get_another_people(conn, event.user_id)
                        result = result.json()
                        viewed_list = tables_search.take_user_viewed(conn, event.user_id)
                        viewed_person_id = result["response"]["items"][count]["id"]
                        while viewed_person_id in viewed_list:
                            count += 1
                            viewed_person_id = result["response"]["items"][count]["id"]
                        write_msg(event.user_id,
                                  f'Имя: {result["response"]["items"][count]["first_name"]}'
                                  f'\nФамилия: {result["response"]["items"][count]["last_name"]}'
                                  f'\nhttps://vk.com/id{viewed_person_id}'
                                  f'\n***фото***'
                                  f'\nНапишите "далее" чтобы продолжить поиск или "хочу" чтобы добавить человека в избранное!')
                        tables_filler.add_viewed_person(conn, viewed_person_id, event.user_id)

                    elif request == 'далее':
                        result = vk_get_another_people.get_another_people(conn, event.user_id)
                        result = result.json()
                        count += 1
                        viewed_list = tables_search.take_user_viewed(conn, event.user_id)
                        viewed_person_id = result["response"]["items"][count]["id"]
                        while viewed_person_id in viewed_list:
                            count += 1
                            viewed_person_id = result["response"]["items"][count]["id"]
                        write_msg(event.user_id,
                                  f'Имя: {result["response"]["items"][count]["first_name"]}'
                                  f'\nФамилия: {result["response"]["items"][count]["last_name"]}'
                                  f'\nhttps://vk.com/id{viewed_person_id}'
                                  f'\n***фото***'
                                  f'\nНапишите "далее" чтобы продолжить поиск или "хочу" чтобы добавить человека в избранное!')
                        tables_filler.add_viewed_person(conn, viewed_person_id, event.user_id)

                    elif request == 'хочу':
                        tables_filler.add_favorite_person(conn, viewed_person_id, event.user_id)
                        write_msg(event.user_id,
                                  f'Я добавил этого человека в ваше избранное. Напишите "далее" чтобы продолжить поиск!')

                    elif request == 'пока':
                        write_msg(event.user_id, 'пока(')

                    elif request == 'избранное':
                        result = tables_search.take_user_favorites(conn, event.user_id)
                        for i in result:
                            write_msg(event.user_id, i)

                    else:
                        write_msg(event.user_id, 'Не понял команду. Список команд:'
                                                 '\n"привет" - чтобы поздороваться :)'
                                                 '\n"добавь" - чтобы корректно внести себя в базу (нужно для поиска), обязательно для поиска'
                                                 '\n"искать" - запуск поиска занкомств'
                                                 '\n"далее" - если ты уже запускал поиск знакомств'
                                                 '\n"хочу" - добавляет в избранное последнего просмотренного тобой человека'
                                                 '\n"пока" - чтобы попрощаться ;)'
                                                 '\n"избранное" - показывает список людей которых ты добавил в избранное')
