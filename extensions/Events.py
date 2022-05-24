import lightbulb
import hikari
from utils import check_level_up

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
        embed = hikari.Embed(title=f"{event.context.command.name} is on cooldown!", description=f"Retry after {round(event.exception.retry_after)}", colour=event.context.author.accent_colour)
        return await event.context.respond(embed=embed)

    raise event.exception

@events.listener(hikari.MessageCreateEvent)
async def message_creation_event(event: hikari.MessageCreateEvent):
    msg = event.message
    inf = await events.bot.xp.create(msg.author.id, msg.guild_id)
    await events.bot.xp.update(msg.author.id, msg.guild_id, xp=inf.xp+5)
    await check_level_up(msg.author, msg.guild_id, inf.xp+5, inf.level, events.bot.xp, msg)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(events)