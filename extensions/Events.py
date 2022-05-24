import lightbulb
import hikari

class Events(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__("Events", "Event Listeners")

event = Events()

@event.listener(lightbulb.SlashCommandErrorEvent)
async def cooldown_error_handler(event: lightbulb.SlashCommandErrorEvent):
    if isinstance(event.exception, hikari.NotFoundError):
        return
    if isinstance(event.exception, lightbulb.CommandIsOnCooldown):
        embed = hikari.Embed(title=f"{event.context.command} is on cooldown!", description=f"Retry after {event.exception.retry_after}", colour=event.context.author.accent_colour)
        await event.context.respond(embed=embed)

    raise event.exception

def load(bot: lightbulb.BotApp):
    bot.add_plugin(event)