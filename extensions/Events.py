import lightbulb
import hikari
from utils import check_level_up, getch_join_channel

class Events(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__("Events", "Event Listeners")

events = Events()

@events.listener(lightbulb.SlashCommandErrorEvent)
async def cooldown_error_handler(event: lightbulb.SlashCommandErrorEvent):
    if isinstance(event.exception, hikari.NotFoundError):
        return
    if isinstance(event.exception, lightbulb.CommandIsOnCooldown):
        embed = hikari.Embed(title=f"'{event.context.command.name}' command is on cooldown!", description=f"Retry after {round(event.exception.retry_after)} seconds!", colour=event.context.author.accent_colour)
        return await event.context.respond(embed=embed)

    raise event.exception

@events.listener(hikari.GuildMessageCreateEvent)
async def message_creation_event(event: hikari.MessageCreateEvent):
    msg = event.message
    inf = await events.bot.xp.create(msg.author.id, msg.guild_id)
    await events.bot.xp.update(msg.author.id, msg.guild_id, xp=inf.xp+5)
    await check_level_up(msg.author, msg.guild_id, inf.xp+5, inf.level, events.bot.xp, msg)

@events.listener(hikari.GuildJoinEvent)
async def bot_join(event: hikari.GuildJoinEvent):
    channel = await getch_join_channel(event)
    if not channel:
        return
    b = events.bot.get_me() or await events.bot.rest.fetch_my_user()
    embed = hikari.Embed(title=b.username, colour=b.accent_colour).set_thumbnail(b.default_avatar_url).add_field("Command Types", "Slash Commands!")
    await channel.send(embed=embed)

@events.listener(hikari.MemberCreateEvent)
async def member_join(event: hikari.MemberCreateEvent):
    channel_info: hikari.TextableChannel = await events.bot.channels.read(event.guild_id)
    if not channel_info:
        return
    channel = events.bot.cache.get_guild_channel(channel_info.welcome)
    if not channel:
        return
    if not isinstance(channel, hikari.TextableGuildChannel):
        return
    
    guild_info = await events.bot.info.read(event.guild_id)
    if not guild_info:
        return
    embed = hikari.Embed(description=f"{event.member.mention}, {guild_info.welcome_message}", colour=hikari.Colour(0xffbc03)).set_thumbnail(event.member.default_avatar_url)
    await channel.send(embed=embed)

@events.listener(hikari.MemberDeleteEvent)
async def member_leave(event: hikari.MemberDeleteEvent):
    channel_info: hikari.TextableChannel = await events.bot.channels.read(event.guild_id)
    if not channel_info:
        return
    channel = events.bot.cache.get_guild_channel(channel_info.leave)
    if not channel:
        return
    if not isinstance(channel, hikari.TextableGuildChannel):
        return
    
    guild_info = await events.bot.info.read(event.guild_id)
    if not guild_info:
        return
    embed = hikari.Embed(description=f"{event.old_member.mention}, {guild_info.leave_message}", colour=hikari.Colour(0xffbc03)).set_thumbnail(event.old_member.default_avatar_url)
    await channel.send(embed=embed)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(events)