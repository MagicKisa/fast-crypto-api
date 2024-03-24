import requests
import json


def data_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


apis_dict = data_from_json("apis_dict.json")


def get_url_and_apikey(platform):
    url, apikey = None, None
    for api in apis_dict["apis"]:
        if api["scan_name"] == platform:
            url = api["url"]
            apikey = api["apikey"]

    return url, apikey


def get_source_code(address, platform):
    if address is None:
        raise ValueError("address cannot be None")
    if platform is None:
        raise ValueError("platform have to be specified")

    url, apikey = get_url_and_apikey(platform)

    if url is None or apikey is None:
        raise Exception("That platform is not supported")

    params = {"module": "contract", "action": "getsourcecode", "address": address, "apikey": apikey}
    source_code = request_code(url, params=params)

    return source_code


def request_code(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()  # Извлечение данных из JSON-ответа
        try:
            source_code = data['result'][0]['SourceCode']
        except TypeError:
            return None

        return source_code

    raise Exception("response code is not 200")

    
