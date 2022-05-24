async def get_news(*, api_key: str, req_client, query: str)  -> dict:
    resp = await req_client.get(f'https://newsapi.org/v2/everything?q={query}&pageSize=1&sortBy=popularity&apiKey={api_key}')
    if resp.status != 200:
        return {"error": "Could not find news!"}
    content = await resp.json()
    return {
        "author": content["articles"][0]["author"],
        "content": content["articles"][0]["content"],
        "description": content["articles"][0]["description"],
        "title": content["articles"][0]["title"],
        "url": content["articles"][0]["url"],
        "image": content["articles"][0]["urlToImage"],
    }

def format_channels(data) -> dict:
    welcome = data.welcome
    leave = data.leave
    log = data.log
    vent = data.vent
    ret_dict = {}
    if welcome == 0:
        ret_dict.update({"welcome": "No welcome channel has been configurd yet!"})
    else:
        ret_dict.update({"welcome": f"<#{welcome}>"})

    if leave == 0:
        ret_dict.update({"leave": "No leave channel has been configurd yet!"})
    else:
        ret_dict.update({"leave": f"<#{leave}>"})

    if log == 0:
        ret_dict.update({"log": "No log channel has been configurd yet!"})
    else:
        ret_dict.update({"log": f"<#{log}>"})

    if vent == 0:
        ret_dict.update({"vent": "No vent channel has been configurd yet!"})
    else:
        ret_dict.update({"vent": f"<#{vent}>"})
    return ret_dict

colours = {
    "orange" : "FFA500",
    "red" : "FF0000",
    "green" : "00FF00",
    "blue" : "0000FF",
    "magenta" : "FF00FF",
    "violet" : "EE82EE",
    "cyan" : "00FFFF",
    "pink" : "FF69B4",
    "orange" : "FFA500",
    "white" : "e6edf0",
    "yellow" : "FFFF00",}

def get_hex(colour: str) -> str:
    return colours.get(colour)