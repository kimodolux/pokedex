import requests

POKE_API_URL = "https://pokeapi.co/api/v2/"


def get_link(link: str):
    res = requests.get(link)
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}


def get_pokemon_names():
    res = requests.get(POKE_API_URL + "pokemon?limit=493")
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}


def pokemon_name():
    pokemon_names = get_pokemon_names()
    pokemon_data = [
        get_link(pokemon_link["url"]) for pokemon_link in pokemon_names["results"]
    ]
    # save pokemon data to db
    count = 1
    for pokemon in pokemon_data:
        res = requests.post(
            "http://127.0.0.1:5000/api/create_pokemon",
            headers={"Content-type": "application/json", "Accept": "text/plain"},
            json={"data": pokemon},
        )

        print(res.status_code)
        print(count)
        count += 1


pokemon_name()
