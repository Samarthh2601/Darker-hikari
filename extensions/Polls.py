import lightbulb
import hikari
import datetime

class Poll(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__("Polls", "Create polls!")

poll = Poll()

@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.add_checks(lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@poll.command
@lightbulb.option(name="poll_title", description="The title of the poll!", type=str, required=False)
@lightbulb.option(name="poll_description", description="The description of the poll!", type=str, required=False)
@lightbulb.option(name="option_one", description="The first option!", required=True, type=str)
@lightbulb.option(name="option_two", description="The second option!", required=True, type=str)
@lightbulb.option(name="option_three", description="The third option!", required=False, type=str)
@lightbulb.option(name="option_four", description="The fourth option!", required=False, type=str)
@lightbulb.option(name="option_five", description="The fifth option!", required=False, type=str)
@lightbulb.option(name="option_six", description="The sixth option!", required=False, type=str)
@lightbulb.option(name="timed_poll", description="Should the poll have a timeout or not? Results after end if timeouts!", choices=["Yes", "No"], required=False, type=str, default="No")
@lightbulb.option(name="days", description="The days after which the poll should end!", required=False, type=int, default=0)
@lightbulb.option(name="hours", description="The hours after which the poll should end!", required=False, type=int, default=0)
@lightbulb.option(name="minutes", description="The minutes after which the poll should end!", required=False, type=int, default=0)
@lightbulb.option(name="seconds", description="The seconds after which the poll should end!", required=True, type=int, default=0)
@lightbulb.command(name="poll", description="Raise a poll!", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def create_poll(ctx: lightbulb.SlashContext):
    title: str = ctx._options.get("poll_title")    
    desc: str = ctx._options.get("poll_description")
    option_one: str = ctx._options.get("option_one")
    option_two: str = ctx._options.get("option_two")
    option_three: str = ctx._options.get("option_three")
    option_four: str = ctx._options.get("option_four")
    option_five: str = ctx._options.get("option_five")
    option_six: str = ctx._options.get("option_six")
    timed_poll: str = ctx._options.get("timed_poll")

    _guild = ctx.get_guild() or await poll.bot.rest.fetch_guild(ctx.guild_id)
    channel: hikari.TextableGuildChannel = ctx.get_channel() or await poll.bot.rest.fetch_channel(ctx.channel_id)
    await channel.edit(permission_overwrites=[hikari.PermissionOverwrite(id=ctx.guild_id, type=hikari.PermissionOverwriteType.ROLE,deny=(hikari.Permissions.ADD_REACTIONS))])

    embed = hikari.Embed(color=ctx.author.accent_colour)
    if title:
        embed.title = title
    if desc:
        embed.description = desc

    embed.add_field(name="Option 1", value=f"1️⃣ ) {option_one}", inline=False)
    embed.add_field(name="Option 2", value=f"2️⃣ ) {option_two}", inline=False)
    reactions_to_add = ["1️⃣", "2️⃣"]
    if option_three:
        embed.add_field(name="Option 3", value=f"3️⃣ ) {option_three}", inline=False)
        reactions_to_add.append("3️⃣")
    if option_four: 
        embed.add_field(name="Option 4", value=f"4️⃣ ) {option_four}", inline=False)
        reactions_to_add.append("4️⃣")
    if option_five: 
        embed.add_field(name="Option 5", value=f"5️⃣ ) {option_five}", inline=False)
        reactions_to_add.append("5️⃣")
    if option_six:
        embed.add_field(name="Option 6", value=f"6️⃣ ) {option_six}", inline=False)
        reactions_to_add.append("6️⃣")

    if _guild.icon_url:
        embed.set_thumbnail(_guild.icon_url)

    msg = await channel.send(embed=embed)
    for emoji in reactions_to_add: 
        await msg.add_reaction(emoji)
    if timed_poll.lower() == "no":    
        return await ctx.respond(f"Raised a poll in {channel.mention}!")

    days = ctx._options.get("days")
    hours = ctx._options.get("hours")
    minutes = ctx._options.get("minutes")
    seconds = ctx._options.get("seconds")

    end_time = (datetime.datetime.utcnow() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))
    to_send = int((end_time).timestamp())
    await poll.bot.polls.create(ctx.guild_id, msg.id, end_time)
    await poll.bot.rest.create_message(ctx.channel_id, f"{ctx.author.mention}, Successfully Setup the poll! Ending: <t:{to_send}:R>")

def load(bot: lightbulb.BotApp):
    bot.add_plugin(poll)