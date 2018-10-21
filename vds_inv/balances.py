import json
import urllib.request
from urllib.error import URLError

spares_url: str = 'https://job.firstvds.ru/spares.json'
alternatives_url: str = 'https://job.firstvds.ru/alternatives.json'


def get_json(url):
    try:
        with urllib.request.urlopen(url) as response:
            resp = response.read()
    except URLError as e:
        resp = '{}'
    return resp


def get_spares():
    spares_res = get_json(spares_url)
    return json.loads(spares_res)


def get_alternatives():
    alternatives_res = get_json(alternatives_url)
    return json.loads(alternatives_res)


# !Предполагаем, что одна запчасть может быть только в одном списке альтернатив.
def get_balances():
    stocks = {}
    alternatives = get_alternatives()['alternatives']
    spares = get_spares()
    # Сначала разберём список взаимозаменяемых запчастей
    for k, v in alternatives.items():
        count = 0
        arrive = 0
        mustbe = 0
        for spare_name in v:
            spare = spares.get(spare_name)
            if spare is None:
                continue
            count += spare['count']
            arrive += spare['arrive']
            mustbe = max(spare['mustbe'], mustbe)
            spares.pop(spare_name)
        alert = mustbe > count + arrive
        stocks[k] = {'count': count, 'mustbe': mustbe, 'arrive': arrive, 'alert': alert}
    # А потом допишем к нему незаменяемые
    for k, v in spares.items():
        count = v['count']
        arrive = v['arrive']
        mustbe = v['mustbe']
        alert = mustbe > count + arrive
        stocks[k] = {'count': count, 'mustbe': mustbe, 'arrive': arrive, 'alert': alert}
    return stocks


def get_requests():
    request_dict = {}
    spares = get_spares()
    for k, v in spares.items():
        count = v['count']
        arrive = v['arrive']
        mustbe = v['mustbe']
        if mustbe > count + arrive:
            request_dict[k] = mustbe - (count + arrive)
    return request_dict
