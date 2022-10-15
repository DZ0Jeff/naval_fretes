import requests
import json
from time import sleep


def maesk_get_location(cityname:str):

    url = "https://api.maersk.com/locations"

    querystring = {"cityName": cityname,"type":"city","sort":"cityName"}

    response = requests.get(url, params=querystring)

    if response.status_code == 404:
        raise Exception(f'Erro: {response.status_code}!\n Paramêtro inválido...')

    if response.status_code == 401:
        raise Exception(f'Erro: {response.status_code}!\n verifique as suas credenciais...')

    if response.status_code != 200:
        raise Exception(f'Erro: {response.status_code}!')

    content = response.content.decode()
    content = content[content.find("{"):content.find("}")+1]
    data = json.loads(content)

    return {
        "city": data['cityName'],
        "maerskGeoLocationId": data['maerskGeoLocationId']
    }


def maesk_get_ship_price(**kwargs):

    url = "https://api.maersk.com/productoffer/v2/productoffers"

    payload = {
        "from": {
            "name": kwargs.get('from_name'), #"Santos (Sao Paulo), Brazil",
            "maerskGeoId": kwargs.get('from_geoid'), #"1BX66GARX9UAH",
            "maerskServiceMode": "CY"
        },
        "to": {
            "name": kwargs.get('to_name'), #"Singapore, Singapore",
            "maerskGeoId": kwargs.get('to_geoid'), #"0XOP5ISJZK0HR",
            "maerskServiceMode": "CY"
        },
        "commodity": {
            "name": kwargs.get('commodity'),  #"(With Lithium Batteries) Electronics, electronic appliances, audio, video equipment, telecommunication equipment",
            "isDangerous": False,
            "dangerousDetails": []
        },
        "containers": [
            {
                "isoCode": "22G1",
                "name": "20 Dry Standard",
                "size": "20",
                "type": "DRY",
                "weight": 18000,
                "quantity": 1,
                "isReefer": False,
                "isNonOperatingReefer": False,
                "isShipperOwnedContainer": False
            }
        ],
        "unit": "KG",
        "shipmentPriceCalculationDate": kwargs.get('send_date'),#"2022-10-31",
        "brandCode": "MAEU",
        "customerCode": "30501103219",
        "isSameRequest": False,
        "loadAFLS": False,
        "weekOffset": 0
    }
    
    headers = {
        "authority": "api.maersk.com",
        "accept": "application/json, text/plain, */*",
        "akamai-bm-telemetry": kwargs.get('akamai_telemetry') ,
        "authorization": kwargs.get('bearer_token'),
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f'Erro: {response.status_code}!\n verifique as suas credenciais...')

    return response.json()
