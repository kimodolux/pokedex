import requests

POKE_API_URL = "https://pokeapi.co/api/v2/"


def get_first_gen_pokedex():
    res = requests.get(POKE_API_URL + "pokemon?limit=151")
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}


def get_pokemon(pokemon_name: str):
    res = requests.get(POKE_API_URL + "pokemon/" + pokemon_name)
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}


def get_link(link: str):
    res = requests.get(link)
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}
