import hikari
import lightbulb
import pykawaii

class Anime(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__("Anime", "Anime commands!")
        self.client = pykawaii.Client().sfw

anime = Anime()

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.option(name="member", description="The member to hold hands with!", required=True, type=hikari.Member)
@lightbulb.command(name="handhold", description=f"Hold hands with someone!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def handhold_(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get('member')
    if member.id == ctx.author.id:
        return await ctx.respond("Too lonely, huh?")
    gif = await anime.client.handhold()
    embed = hikari.Embed(description=f"{ctx.author.mention} holds hands with {member.mention}!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.option(name="member", description="The member to hug!", required=True, type=hikari.Member)
@lightbulb.command(name="hug", description=f"Hug someone!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def hug_user(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get('member')
    if member.id == ctx.author.id:
        return await ctx.respond("Too lonely, huh?")
    gif = await anime.client.hug()
    embed = hikari.Embed(description=f"{ctx.author.mention} hugs {member.mention}!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.option(name="member", description="The member to kill!", required=True, type=hikari.Member)
@lightbulb.command(name="kill", description=f"Kill someone!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def kill_user(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get('member')
    if member.id == ctx.author.id:
        return await ctx.respond("Too lonely, huh?")
    gif = await anime.client.kill()
    embed = hikari.Embed(description=f"{ctx.author.mention} kills {member.mention}!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.option(name="member", description="The member to kiss!", required=True, type=hikari.Member)
@lightbulb.command(name="kiss", description=f"Kiss someone!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def kiss_user(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get('member')
    if member.id == ctx.author.id:
        return await ctx.respond("Too lonely, huh?")
    gif = await anime.client.kiss()
    embed = hikari.Embed(description=f"{ctx.author.mention} kisses {member.mention}!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.option(name="member", description="The member to bite!", required=True, type=hikari.Member)
@lightbulb.command(name="bite", description=f"Bite someone!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def bite_user(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get('member')
    if member.id == ctx.author.id:
        return await ctx.respond("Too lonely, huh?")
    gif = await anime.client.bite()
    embed = hikari.Embed(description=f"{ctx.author.mention} bites {member.mention}!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.option(name="member", description="The member to bonk!", required=True, type=hikari.Member)
@lightbulb.command(name="bonk", description=f"Bonk someone!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def bonk_user(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get('member')
    if member.id == ctx.author.id:
        return await ctx.respond("Too lonely, huh?")
    gif = await anime.client.bonk()
    embed = hikari.Embed(description=f"{ctx.author.mention} bonk {member.mention}!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.option(name="member", description="The member to bully!", required=True, type=hikari.Member)
@lightbulb.command(name="bully", description=f"Bully someone!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def kiss_user(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get('member')
    if member.id == ctx.author.id:
        return await ctx.respond("Too lonely, huh?")
    gif = await anime.client.bully()
    embed = hikari.Embed(description=f"{ctx.author.mention} is bullying {member.mention}!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.option(name="member", description="The member to cringe at!", required=True, type=hikari.Member)
@lightbulb.command(name="cringe", description=f"Cringe at someone!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def cringe_(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get('member')
    if member.id == ctx.author.id:
        return await ctx.respond("Too lonely, huh?")
    gif = await anime.client.cringe()
    embed = hikari.Embed(description=f"{ctx.author.mention} is cringing at {member.mention}!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.command(name="cry", description=f"Send a crying reaction!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def cry(ctx: lightbulb.SlashContext):
    gif = await anime.client.cry()
    embed = hikari.Embed(description=f"{ctx.author.mention} is crying...", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.command(name="happy", description=f"Send a happy reaction!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def happy(ctx: lightbulb.SlashContext):
    gif = await anime.client.happy()
    embed = hikari.Embed(description=f"{ctx.author.mention} is happy!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.command(name="dance", description=f"Send a dancing reaction!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def happy(ctx: lightbulb.SlashContext):
    gif = await anime.client.dance()
    embed = hikari.Embed(description=f"{ctx.author.mention} is dancing!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.command(name="wave", description=f"Send a waving reaction!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def wave_(ctx: lightbulb.SlashContext):
    gif = await anime.client.wave()
    embed = hikari.Embed(description=f"{ctx.author.mention} is waving!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@anime.command
@lightbulb.command(name="blush", description=f"Send a blushing reaction!", auto_defer=True, ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def blush_(ctx: lightbulb.SlashContext):
    gif = await anime.client.blush()
    embed = hikari.Embed(description=f"{ctx.author.mention} is blushing!", colour=ctx.author.accent_colour).set_image(gif)
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(anime)