import lightbulb 


class Admin(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__(name="Admin Commands", description="Bot Admin Commands")

admin = Admin()

@admin.command
@lightbulb.command(name="reload", description="Reload all the extensions", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def reload_exts(ctx: lightbulb.SlashContext):
    admin.bot.unload_extensions("./extensions/Moderation")
    admin.bot.load_extensions("./extensions/Moderation")
    await ctx.respond("Yes")

def load(bot: lightbulb.BotApp):
    bot.add_plugin(admin)