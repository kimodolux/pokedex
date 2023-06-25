import requests

POKE_API_URL = "https://pokeapi.co/api/v2/"


def get_link(link: str):
    res = requests.get(link)
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}


def get_ability_names():
    res = requests.get(POKE_API_URL + "ability?limit=358")
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}


def ability_name():
    ability_names = get_ability_names()
    ability_data = [
        get_link(ability_link["url"]) for ability_link in ability_names["results"]
    ]
    # save pokemon data to db
    count = 1
    for ability in ability_data:
        res = requests.post(
            "http://127.0.0.1:5000/api/create_ability",
            headers={"Content-type": "application/json", "Accept": "text/plain"},
            json={"data": ability},
        )

        print(res.status_code)
        print(res.text)
        print(count)
        count += 1


ability_name()
