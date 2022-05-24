import lightbulb
import hikari
import random
from io import BytesIO

class General(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__(name="General Commands", description="General Utility commands")

gen = General()

@gen.command
@lightbulb.command(name="ping", description="Get My Ping!", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext):
    embed = hikari.Embed(title="My Ping", description=f"{int(gen.bot.heartbeat_latency) * 1000}ms")
    await ctx.respond(embed=embed)

@gen.command
@lightbulb.option(name="member", description="The member to send this message to!", type=hikari.Member, required=True)
@lightbulb.option(name="message", description="The content to send!", type=str, required=True)
@lightbulb.command(name="send", description="Send A Message To Another Member!", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def send_msg(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get("member")
    message = ctx._options.get("message")
    if ctx.author == member:
        return await ctx.respond("You cannot send a message to yourself!")

    if len(message) > 1000:
        return await ctx.respond("Message Limit crossed!")

    embed= hikari.Embed(title=f"A message from {ctx.author.username}!", description=message, color=ctx.author.accent_color).set_thumbnail(ctx.author.display_avatar_url)
    try:
        await member.send(embed=embed)
        await ctx.respond(f"Successfully Messaged {member.mention}!")
    except hikari.ForbiddenError:
        return await ctx.respond(f"{member.mention}'s DMs are off!")

@gen.command
@lightbulb.option(name="member", description="The Member to get the avatar of!", type=hikari.Member, required=False)
@lightbulb.command(name="avatar", description="Get your avatar or of a Member's!", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def get_avatar(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get("member") or ctx.author
    embed = hikari.Embed(color=member.accent_color).set_image(member.display_avatar_url)
    await ctx.respond(embed=embed)

@gen.command
@lightbulb.option(name="member", description="The Member to get information of!", type=hikari.Member, required=False)
@lightbulb.command(name="profile", description="Get Information about a Member!", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def get_user_info(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get("member") or ctx.member
    presence = member.get_presence()
    acc_creation = member.created_at.strftime("%Y-%m-%d")
    guild_join = member.joined_at.strftime("%Y-%m-%d")
    status = presence.visible_status
    if presence.activities: activities = [activity.name for activity in presence.activities]
    else: activities = "No Activity"
    
    nickname = member.nickname
    if not nickname:
        nickname = "No Nick Name"

    embed = hikari.Embed(color=member.accent_color).set_image(member.display_avatar_url).add_field("Username", member, inline=True).add_field("Name", member.username, inline=True).add_field("Tagline", member.discriminator, inline=True).add_field("Nickname", nickname, inline=True).add_field("Discord ID", member.id, inline=True).add_field("Colour", member.get_top_role().color, inline=True).add_field("Number of Roles", len(member.role_ids)-1, inline=True).add_field("Server Join", guild_join, inline=True).add_field("Account Creation", acc_creation, inline=True).add_field("Status", status, inline=True).add_field("Activities", activities, inline=True).add_field("Avatar URL", f"[{member.username}'s avatar URL]({member.display_avatar_url})", inline=True)
    await ctx.respond(embed=embed)

@gen.command
@lightbulb.option(name="id_or_link", description="Enter the Message link or ID", required=True)
@lightbulb.command(name="bookmark", description="Get a link to the message straight to your DMs! Run the command in the same channel as the message!", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def bm_mes(ctx: lightbulb.SlashContext):
    _content: str = ctx._options.get("id_or_link")

    if len(_content) == 18 and _content.isdigit(): message_id = _content

    elif len(_content) == 85 and not _content.isdigit() and _content.startswith("https://discord.com/channels/"): message_id = _content.split("/")[-1]
    else: return await ctx.respond("Invalid Message ID/Link was given!")

    message_channel = ctx.get_channel() or await gen.bot.rest.fetch_channel(ctx.channel_id)
    message = gen.bot.cache.get_message(message_id) or await gen.bot.rest.fetch_message(channel=message_channel, message=message_id)
    if not message:
        return await ctx.respond("Could not find that message!")
    message_channel = await message.fetch_channel()
    msgc_name = message_channel.name
    if not message.content and message.embeds or not message.content and message.attachments:
        initial_message_chars = "Contains Embeds/Images/etc..."
    else:
        message_length = len(message.content)
        if message_length > 10: initial_message_chars = message.content[0:10]
        elif message_length <= 10 and message_length >= 5: initial_message_chars = message.content[0:8]
        elif message_length <= 5: initial_message_chars = message.content[0:5]

    embed = hikari.Embed(title="Message Bookmark", description=f"{initial_message_chars}...", color=ctx.author.accent_colour).set_thumbnail(ctx.author.display_avatar_url).add_field("Server", ctx.get_guild().name, inline=True).add_field("Message author", message.author, inline=True).add_field("Message Channel", msgc_name, inline=True).add_field("Original Message", f"[See Original Message]({message.make_link(ctx.guild_id)})")
    try:
        await ctx.author.send(embed=embed)
        await ctx.respond("Successfully sent you the bookmark!")
    except hikari.ForbiddenError:
        await ctx.respond("Your DMs are closed! Enable your DMs to get a link!")

@gen.command
@lightbulb.option(name="text", description="The text to reply with!", required=True, type=str)
@lightbulb.option(name="id_or_link", description="Enter the Message link or ID to reply to!", required=True)
@lightbulb.option(name="member", description="This will default to the specified message's author if not given", required=False, type=hikari.Member)
@lightbulb.command(name="reply", description="Reply to a Member's message!", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def reply_msg(ctx: lightbulb.SlashContext):
    _content: str = ctx._options.get("id_or_link")
    
    _msg_text: str =  ctx._options.get("text")
    if len(_msg_text) > 500:
        return await ctx.respond("The text should be under 500 characters!")

    if len(_content) == 18 and _content.isdigit(): message_id = _content

    elif len(_content) == 85 and not _content.isdigit(): message_id = _content.split("/")[-1]
    else: return await ctx.respond("Invalid Message ID/Link was given!")

    message_channel = ctx.get_channel() or await gen.bot.rest.fetch_channel(ctx.channel_id)
    message = gen.bot.cache.get_message(message_id) or await gen.bot.rest.fetch_message(channel=message_channel, message=message_id)
    if not message:
        return await ctx.respond("Could not find that message!")
    
    _member: hikari.Member = ctx._options.get("member") or message.author
    message_channel = await message.fetch_channel()
    msgc_name = message_channel.name
    if not message.content and message.embeds or not message.content and message.attachments:
        initial_message_chars = "Contains Embeds/Images/etc..."
    else:
        message_length = len(message.content)
        if message_length > 10: initial_message_chars = message.content[0:10]
        elif message_length <= 10 and message_length >= 5: initial_message_chars = message.content[0:8]
        elif message_length <= 5: initial_message_chars = message.content[0:5]

    embed = hikari.Embed(title=f"Replying on behalf of {ctx.author}", description=_msg_text, color=ctx.author.accent_colour).set_thumbnail(ctx.author.display_avatar_url).add_field("Message ref", f"{initial_message_chars}...", inline=True).add_field("Server", ctx.get_guild().name, inline=True).add_field("Message author", message.author, inline=True).add_field("Message Channel", msgc_name, inline=True).add_field("Original Message", f"[See Original Message]({message.make_link(ctx.guild_id)})")
    

    try:
        await _member.send(embed=embed)
        await ctx.respond(f"Successfully replied to {_member}!")
    except hikari.ForbiddenError:
        await ctx.respond("Could not message that user!")

@gen.command
@lightbulb.option(name="text", description="The content to send!", required=True)
@lightbulb.option(name="name", description="The name of the user which sends the message!", required=False)
@lightbulb.option(name="image_url", description="The avatar of the user which sends the message!", required=False)
@lightbulb.command(name="vent", description="Anonymously vent in the venting channel!", ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def _vent(ctx: lightbulb.SlashContext):
    data = await gen.bot.channels.create(ctx.guild_id, 0, 0, 0, 0)
    if data.vent == 0:
        return await ctx.respond("No Venting channel has been set up in this server!")
    
    vent_channel = gen.bot.cache.get_guild_channel(data.vent) or await gen.bot.rest.fetch_channel(data.vent)
    if not vent_channel:
        return await ctx.respond("An invalid vent channel has been set up!")
    text = ctx._options.get("text")
    if len(text) > 500:
        return await ctx.respond("Exceeded Maximum Character Limit for **TEXT**")
    name = ctx._options.get("name") or random.choice(["CornDog998", "HilariousBlade089", "ZapBolt125"])
    image_url = ctx._options.get("image_url")
    if image_url:
        async with gen.bot.http as ses: 
            async with ses.get(image_url) as r: 
                try:
                    if r.status not in range(200, 299):
                        return await ctx.respond("Could not find that image!")
                    img_or_gif = BytesIO(await r.read()) 
                    b_value = img_or_gif.getvalue()
                except hikari.HTTPError: return await ctx.respond("File size is too big!")
        webhook = await gen.bot.rest.create_webhook(vent_channel.id, name=name, avatar=b_value)
    else:
        webhook = await gen.bot.rest.create_webhook(vent_channel.id, name=name)
    embed = hikari.Embed(description=text, color=hikari.Color.from_rgb(222, 0, 100))
    await webhook.execute(embed=embed)
    return await ctx.respond(f"Successfully vented in {vent_channel.mention}")

@gen.command
@lightbulb.option(name="member", description="The member to get the info of!", required=False, type=hikari.Member)
@lightbulb.command(name="rank", description="Get your experience and level!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def get_rank(ctx: lightbulb.SlashContext):
    member = ctx._options.get("member") or ctx.author
    if not isinstance(member, hikari.Member):
        member = await gen.bot.rest.fetch_member(ctx.guild_id, member.id)
    info = await gen.bot.xp.create(member.id, ctx.guild_id)
    embed = hikari.Embed(title="Level Up!", description=f"XP: {info.xp}\nLevel:{info.level}", colour=member.accent_colour)
    await ctx.respond(embed=embed)



def load(bot: lightbulb.BotApp):
    bot.add_plugin(gen)