import requests

import tables_search
import vk_get_user_info
from settings_reader import vk_user_token, URL_search


def get_another_people(conn, user_id):
    result = tables_search.take_user_data(conn, user_id)
    vk_id = result['vk_id']
    name = result['name']
    city = result['city']
    bdate = result['bdate']
    sex = result['sex']
    if sex == 1:
        target_sex = 2
    else:
        target_sex = 1

    params = {
        'sort': 0,
        'count': 999,
        'city': city,
        'birth_year': bdate,
        'sex': target_sex,
        'access_token': vk_user_token,
        'v': '5.89',
        'fields': city
    }

    result = requests.get(URL_search, params=params)
    return result
