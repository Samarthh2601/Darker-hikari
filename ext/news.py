import json
api_version = "v2"

async def get_news(*, api_key: str, req_client, query: str)  -> dict:
    resp = await req_client.get(f'https://newsapi.org/{api_version}/everything?q={query}&pageSize=1&sortBy=popularity&apiKey={api_key}')
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