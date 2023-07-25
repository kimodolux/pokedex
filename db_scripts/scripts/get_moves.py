import requests

POKE_API_URL = "https://pokeapi.co/api/v2/"


def get_link(link: str):
    res = requests.get(link)
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}


def get_move_names():
    res = requests.get(POKE_API_URL + "move?limit=912")
    if res.status_code == 200:
        return res.json()
    else:
        return {"err": f"Error: {res.status_code}"}


def move_name():
    move_names = get_move_names()
    move_data = [get_link(move_link["url"]) for move_link in move_names["results"]]
    # save pokemon data to db
    count = 1
    for move in move_data:
        res = requests.post(
            "http://127.0.0.1:5000/api/create_move",
            headers={"Content-type": "application/json", "Accept": "text/plain"},
            json={"data": move},
        )

        print(res.status_code)
        print(res.text)
        print(count)
        count += 1


move_name()
