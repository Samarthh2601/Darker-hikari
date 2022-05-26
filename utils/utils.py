import hikari
import random

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

_colours = {
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
    return _colours.get(colour)

async def check_level_up(author: hikari.Member, guild_id: int, xp: int, cur_level: int, db, msg) -> None:
    if xp%250!=0:
        return
    await db.update(author.id, guild_id, level=cur_level+1)
    embed = hikari.Embed(title="Level Up!", description=f"XP: {xp}\nLevel:{cur_level+1}", colour=msg.author.accent_colour)
    try:
        return await msg.author.send(embed=embed)
    except (hikari.ForbiddenError):
        return
    
def sort_records(records: list):
    sorted_records = (sorted(records, key=lambda x: x[-1]))
    if len(sorted_records) > 10:
        sorted_records = sorted_records[:10]
    return sorted_records.reverse()

async def getch_join_channel(event: hikari.GuildJoinEvent):
    guild = event.get_guild() or await event.fetch_guild()
    if guild.system_channel_id:
        return await guild.fetch_system_channel()
    channels = guild.get_channels()
    c = [channel for channel in channels if ("welcome", "entry", "come", "general", "hangout", "off-topic", "chill") in channel.name]
    if c:
        return c[0]
    return None

def eightball_response():
    return random.choice(["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.","Yes.", "Yes, definitely.", "You may rely on it."])

def hack_user(member: hikari.Member):
    reddit_usernames = [f"Thunder{member.username}xD56899", f"{member.username}CutieUwU6969", f"FriedPotato{member.username}3321"]
    reddit_passwords = [f"do**na***55***", f"me**uwu**{str(member.id)[5:10]}"]
    hacking_list = [["Initiating Hack...", f"Name: {member.username}\nID:{member.id}", f"Connecting to {str(member.id)[:7]}...",f"Failed Connecting to {str(member.id)[:7]}...", "Retrying...",f"Successfully Connected to {member.username}'s account",f"Checking Discord Connections...",f"Reddit Account found...",f"Loading Reddit app...",f"Username: {random.choice(reddit_usernames)}\nPassword:{random.choice(reddit_passwords)}",f"Changing Password...",f"Password Successfully reset!",f"Liking E-girl posts...",f"Upvoting UwU Pictures..."f"Liked {random.randint(169, 1000)} posts..."f"Reporting account abuse to Reddit...",f"Deleting Account...","Account Successfully Deleted!✅""Logging back into Discord...","Transferring Nitro...","Checking DMs...",f"Most Common Word: {random.choice(['potato', 'tomato', 'uwu', 'lmao', 'lol', 'cringe', 'ded'])}","Injecting Virus...","Successfully Injected ✅","Logging Off...","Shutting down the hacking system...""The Completely-Privacy-Breaching-Dangerous-Dark-Hack hack is finished!"], ["Initiating Hack...", f"Name: {member.username}\nID:{member.id}", f"Connecting to {str(member.id)[:7]}...",f"Failed Connecting to {str(member.id)[:7]}...", "Retrying...",f"Successfully Connected to {member.username}'s account","Checking Discord Connections...","Twitter Account found...","Loading Twitter Details","Injecting Dark tweets...","Most Recent Tweet: Killed my own UwU shadow xD","Deleting Account...","Account Successfully deleted✅","Logging back into Discord...","transferring Nitro...","Checking DMs...",f"Most Common Word: {random.choice(['potato', 'tomato', 'uwu', 'lmao', 'lol', 'cringe', 'ded'])}","Injecting Virus...","Successfully Injected ✅","Logging Off...","Shutting down the hacking system...""The Completely-Privacy-Breaching-Dangerous-Dark-Hack hack is finished!"]]
    return random.choice(hacking_list)