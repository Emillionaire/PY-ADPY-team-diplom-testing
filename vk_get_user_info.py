import requests
from settings_reader import vk_user_token, URL
from pprint import pprint


def get_user_info(user_id):
    params = {
        'fields': 'bdate, city, sex',
        'user_ids': user_id,
        'access_token': vk_user_token,
        'v': '5.89'
    }

    result = requests.get(URL, params=params)
    pprint(result.json())
    data = result.json()
    name = f'{data["response"][0]["first_name"]} {data["response"][0]["last_name"]}'

    try:
        bdate = data['response'][0]['bdate'].split('.')[2]
    except:
        bdate = 0
    try:
        city = data['response'][0]['city']['id']
    except KeyError:
        city = 1

    result_dict = {'vk_id': data['response'][0]['id'],
                   'name': name,
                   'city': city,
                   'bdate': bdate,
                   'sex': data['response'][0]['sex']}
    return result_dict
