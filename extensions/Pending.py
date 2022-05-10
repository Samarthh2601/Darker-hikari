import lightbulb
import hikari
import random
import miru
from views import *

class Pending(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__(name="pendingellaneous Commands", description="Other Utility Commands")
        
pending = Pending()

@pending.command
@lightbulb.option(name="text", description="The content to send!", required=True)
@lightbulb.option(name="name", description="The name of the user which sends the message!", required=False)
@lightbulb.option(name="image_url", description="The avatar of the user which sends the message!", required=False)
@lightbulb.command(name="vent", description="Anonymously vent in the venting channel!", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def _vent(ctx: lightbulb.SlashContext):
    data = await pending.bot.channels.read(ctx.guild_id)
    if not data:
        await pending.bot.channels.create_acc(ctx.guild_id, 0, 0, 0, 0)
        return await ctx.respond("No Venting channel has been set up in this server!")
    
    vent_channel = await pending.bot.rest.fetch_channel(data.vent)
    if not vent_channel:
        return await ctx.respond("An invalid vent channel has been set up!")
    text = ctx._options.get("text")
    if len(text) > 500:
        return await ctx.respond("Exceeded Maximum Character Limit for **TEXT**")
    name = ctx._options.get("name") or random.choice(["CornDog998", "HilariousBlade089", "ZapBolt125"])
    image_url = ctx._options.get("image_url")
    if image_url:
    #     async with pending.bot.http as ses: 
    #         async with ses.get(image_url) as r: 
    #             try:
    #                 if r.status not in range(200, 299):
    #                     return await ctx.respond("Could not find that image!")
    #                 img_or_gif = BytesIO(await r.read()) 
    #                 b_value = img_or_gif.getvalue()
    #             except hikari.HTTPError: return await ctx.respond("File size is too big!")
        webhook = await pending.bot.rest.create_webhook(vent_channel.id, name=name, avatar=image_url)
    else:
        webhook = await pending.bot.rest.create_webhook(vent_channel.id, name=name, avatar=image_url)
    embed = hikari.Embed(description=text, color=hikari.Color.from_rgb(222, 0, 100))
    await webhook.execute(embed=embed)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(pending)