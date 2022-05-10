import lightbulb
import hikari
import datetime
import views
from ext import get_hex

class Moderation(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__(name="Moderation Commands", description="Commands to Moderate Members and Servers!")

mod = Moderation()

@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.add_checks(lightbulb.bot_has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@mod.command
@lightbulb.option(name="member", description="The member to warn!", required=True, type=hikari.Member)
@lightbulb.option(name="warning", description="The warning content!", required=False, type=str, default="No reason provided!")
@lightbulb.command(name="warn", description="Warn a member!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def member_warn(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get("member")
    _guild = ctx.get_guild()
    if member == ctx.author: return await ctx.respond("You cannot warn yourself!")
    if member.id == _guild.owner_id: return await ctx.respond("You cannot warn the server owner!")
    reason = ctx._options.get("warning")

    member_data = await mod.bot.warns.create_acc(ctx.author.id, ctx.guild_id, 0)
    guild_data = await mod.bot.info.create_acc(ctx.guild_id, 0, 0)

    if member_data.warns+1 == guild_data.kick_thresh:
        view = views.KickView()
        msg = await ctx.respond(f"{member.mention} will get kicked due to reaching the kick threshold of **{_guild.name}**, do you wish to kick them or warn them?", components=view.build())

        view.start(await msg.message())
        await view.wait()

        if view.confirm:
            kick_embed = hikari.Embed(title=f"You have been kicked from {_guild.name}", description="Reason: Maximum Number of warnings reached!", color=ctx.author.accent_colour).add_field("Kicked By", ctx.author.mention)
            try:
                try:
                    kick_msg = await member.send(embed=kick_embed)
                except (hikari.ForbiddenError, hikari.BadRequestError): pass
                await member.kick(reason=reason)
            except hikari.ForbiddenError:
                await kick_msg.delete()
                return await ctx.respond("I cannot kick that member since they have already reached the maximum number of warns!")
        else:
            await mod.bot.warns.update(ctx.author.id, ctx.guild_id, member_data.warns+1)
            embed = hikari.Embed(title=f"Warned {member} successfully!", description=f"Server: **{_guild.name}**", color=ctx.author.accent_color).add_field(f"Reason", reason)
            await ctx.respond(embed=embed)
    elif member_data.warns+1 == guild_data.ban_thresh:
        
        view = views.BanView()
        msg = await ctx.respond(f"{member.mention} will get banned due to reaching the ban threshold of **{_guild.name}**, do you wish to ban them or warn them?", components=view.build())

        view.start(await msg.message())
        await view.wait()
        if view.confirm:
            ban_embed = hikari.Embed(title=f"You have been banned from {_guild.name}", description="Reason: Maximum Number of warnings reached!", color=ctx.author.accent_colour).add_field("Banned By", ctx.author.mention)
            try:
                try:
                    ban_msg = await member.send(embed=ban_embed)
                except (hikari.ForbiddenError, hikari.BadRequestError): pass
                await member.ban(reason=reason)
            except hikari.ForbiddenError:
                await ban_msg.delete()
                return await ctx.respond("I cannot ban that member since they have already reached the maximum number of warns!")
        else:
            await mod.bot.warns.update(ctx.author.id, ctx.guild_id, member_data.warns+1)
            embed = hikari.Embed(title=f"Warned {member} successfully!", description=f"Server: **{_guild.name}**", color=ctx.author.accent_color).add_field(f"Reason", reason)
            await ctx.respond(embed=embed)

    elif member_data.warns+1 != guild_data.kick_thresh and member_data.warns+1 != guild_data.ban_thresh:
        embed = hikari.Embed(title="You have been Warned!", description=f"Server: **{_guild.name}**", color=ctx.author.accent_color).add_field(f"Reason", reason)
        if guild_data.kick_thresh != 0 and guild_data.ban_thresh != 0:
            warns_before_kick = guild_data.kick_thresh - member_data.warns
            warns_before_ban = guild_data.ban_thresh - member_data.warns
            embed.add_field("Warns before kick", str(warns_before_kick)).add_field("Warns before ban", str(warns_before_ban))
        try:
            warn_msg = await member.send(embed=embed)
            embed.title = f"Warned {member} successfully!"
            await ctx.respond(embed=embed)

        except (hikari.ForbiddenError, hikari.BadRequestError):
            await warn_msg.delete()
            await ctx.respond("Cannot warn that user as their DMs are disabled! **NOTE**: Warning will be recorded automatically")
        finally:
            await mod.bot.warns.update(ctx.author.id, ctx.guild_id, member_data.warns+1)

    elif member_data.warns+1 > guild_data.kick_thresh and member_data.warns+1 < guild_data.ban_thresh:
        view = views.KickView()
        msg = await ctx.respond(f"{member.mention} will get kicked due to passing the kick threshold of **{_guild.name}**, do you wish to kick them or warn them again?", components=view.build())

        view.start(await msg.message())
        await view.wait()
        if view.confirm:
            kick_embed = hikari.Embed(title=f"You have been kicked from {_guild.name}", description="Reason: Maximum Number of warnings reached!", color=ctx.author.accent_colour).add_field("Kicked By", ctx.author.mention)
            try:
                try:
                    kick_msg = await member.send(embed=kick_embed)
                except (hikari.ForbiddenError, hikari.BadRequestError): pass
                await member.kick(reason=reason)
            except hikari.ForbiddenError:
                await kick_msg.delete()
                return await ctx.respond("I cannot kick that member since they have already reached the maximum number of warns!")
        else:
            await mod.bot.warns.update(ctx.author.id, ctx.guild_id, member_data.warns+1)
            embed = hikari.Embed(title=f"Warned {member} successfully!", description=f"Server: **{_guild.name}**", color=ctx.author.accent_color).add_field(f"Reason", reason)
            await ctx.respond(embed=embed)

    elif member_data.warns+1 > guild_data.ban_thresh:
        view = views.BanView()
        msg = await ctx.respond(f"{member.mention} will get banned due to passing the ban threshold of **{_guild.name}**, do you wish to ban them or warn them?", components=view.build())
 
        view.start(await msg.message())
        await view.wait()
        if view.confirm:
            ban_embed = hikari.Embed(title=f"You have been banned from {_guild.name}", description="Reason: Maximum Number of warnings reached!", color=ctx.author.accent_colour).add_field("Banned By", ctx.author.mention)
            try:
                try:
                    ban_msg = await member.send(embed=ban_embed)
                except (hikari.ForbiddenError, hikari.BadRequestError): pass
                await member.ban(reason=reason)
            except hikari.ForbiddenError:
                await ban_msg.delete()
                return await ctx.respond("I cannot ban that member since they have already reached the maximum number of warns!")
        else:
            await mod.bot.warns.update(ctx.author.id, ctx.guild_id, member_data.warns+1)
            embed = hikari.Embed(title=f"Warned {member} successfully!", description=f"Server: **{_guild.name}**", color=ctx.author.accent_color).add_field(f"Reason", reason)
            await ctx.respond(embed=embed)

@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.add_checks(lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@mod.command
@lightbulb.option(name="messages", description="The amount of messages to purge!", required=False, type=int, default=10)
@lightbulb.option(name="channel", description="The channel to purge the messages from!", required=False, type=hikari.TextableGuildChannel)
@lightbulb.command(name="purge", description="Purge messages in a channel!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def purge_messages(ctx: lightbulb.SlashContext):
    msg_count = ctx._options.get("messages") 
    to_purge = msg_count if msg_count <= 50 else 50
    channel: hikari.GuildTextChannel = ctx._options.get("channel") or ctx.get_channel() or await mod.bot.rest.fetch_channel(ctx.channel_id)
    bulk_delete_limit = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)
    iterator = (mod.bot.rest.fetch_messages(channel.id).take_while(lambda message: message.created_at > bulk_delete_limit).limit(to_purge))
    async for messages in iterator.chunk(100): await mod.bot.rest.delete_messages(channel.id, messages)
    await ctx.respond("Messages were deleted successfully!")

@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.add_checks(lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@mod.command
@lightbulb.option(name="member", description="The member to clear the messages of!", required=False, type=hikari.Member)
@lightbulb.option(name="messages", description="The amount of messages to purge!", required=False, type=int, default=5)
@lightbulb.option(name="channel", description="The channel to clear the messages from!", required=False, type=hikari.TextableGuildChannel)
@lightbulb.command(name="clear", description="Clear a specific member's messages from a channel!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def _clear(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get("member") or ctx.author.id
    msg_count = ctx._options.get("messages")
    to_purge = msg_count if msg_count <= 15 else 15
    channel = ctx._options.get("channel") or ctx.get_channel() or await mod.bot.rest.fetch_channel(ctx.channel_id)
    bulk_delete_limit = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)
    iterator = (
        mod.bot.rest.fetch_messages(channel.id)
        .take_while(lambda message: message.created_at > bulk_delete_limit)
        .filter(lambda message: message.author.id == member.id)
        .limit(to_purge)
    )
    async for messages in iterator.chunk(15):
        await mod.bot.rest.delete_messages(channel.id, messages)
    await ctx.respond(f"Successfully Deleted **{member}**'s messages!")

@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_NICKNAMES))
@lightbulb.add_checks(lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_NICKNAMES))
@mod.command
@lightbulb.option(name="member", description="The member to change the nickname of!", required=False, type=hikari.Member)
@lightbulb.option(name="nickname", description="The new nickname, defaults to username!", required=False, type=str)
@lightbulb.command(name="nickname", description="Change a member's nickname!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def change_nicks(ctx: lightbulb.SlashContext):
    _guild = ctx.get_guild()
    member = ctx._options.get("member") or ctx.author 
    
    if not isinstance(member, hikari.Member): 
        member = _guild.get_member(member.id) or await mod.bot.rest.fetch_member(ctx.guild_id, member.id)

    nickname = ctx._options.get("nickname")

    try:
        updated_member = await member.edit(nickname=nickname)
    except hikari.ForbiddenError:
        return await ctx.respond("I cannot change the nickname of that member!")
    
    embed = hikari.Embed(title=f"Updated Profile for {member}", description="Change: **DISPLAY NAME/NICKNAME**", colour=member.accent_colour).set_thumbnail(member.display_avatar_url)

    embed.add_field("Old Nickname", (member.nickname if member.nickname else "No Nickname")).add_field("New Nickname", updated_member.nickname).add_field("Moderator", ctx.author.mention)
    await ctx.respond(embed=embed)

@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.add_checks(lightbulb.bot_has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@mod.command
@lightbulb.option(name="user_id", description="The ID of the member to unban", required=True, type=int)
@lightbulb.option(name="reason", description="The reason to unban", required=False, type=str, default="No reason provided")
@lightbulb.command(name="unban", description="Unban a member from the server!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def _unban(ctx: lightbulb.SlashContext):
    _guild = ctx.get_guild() or await mod.bot.rest.fetch_guild(ctx.guild_id)
    _member = ctx._options.get("member_id")
    _reason = ctx._options.get("reason")
    member = await mod.bot.rest.fetch_user(_member)
    if not member: 
        return await ctx.respond("No member with that ID is existent!")
    try:
        await _guild.unban(_member, reason=_reason)
    except (hikari.BadRequestError, hikari.ForbiddenError, hikari.UnauthorizedError):
        return await ctx.respond("Could not unban that member!")

    embed = hikari.Embed(title=f"Unbanned {member}", description=f"Server: {_guild.name}", colour=ctx.author.accent_colour).set_thumbnail(member.default_avatar_url).add_field("Reason for unban", _reason).add_field("Moderator", ctx.author.mention)
    await ctx.respond(embed=embed)

@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.add_checks(lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@mod.command
@lightbulb.option(name="title", description="The title of the embed!", required=False, type=str)
@lightbulb.option(name="description", description="The description of the embed!", required=True, type=str)
@lightbulb.option(name="colour", description="The colour of the strip of the embed!", required=False, type=str, choices=["red", "blue", "green", "yellow", "orange", "pink", "magenta", "violet", "white", "cyan"])
@lightbulb.option(name="embed_image_url", description="The embed image!", required=False, type=str)
@lightbulb.option(name="anonymous_author", description="Anonymously send the embed!", choices=["Yes", "No"], required=False, type=str, default="no")
@lightbulb.option(name="message", description="The text will be sent in addition to the embed! (will not be embedded!)", type=str, required=False)
@lightbulb.option(name="channel", description="The channel to send the embed in!", type=hikari.TextableGuildChannel, required=False)
@lightbulb.command(name="embed", description="Send text in an embed", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_text(ctx: lightbulb.SlashContext):
    embed_title: str = ctx._options.get("title")
    embed_description: str = ctx._options.get("description")
    embed_colour: str = ctx._options.get("colour")
    embed_image_url: str = ctx._options.get("embed_image_url")
    anonym_author: str = ctx._options.get("anonymous_author")
    embed_addit_message: str = ctx._options.get("message")
    # -------------------------------------------------------
    channel: hikari.TextableGuildChannel = ctx._options.get("channel") or ctx.get_channel()
    if not channel: channel = await mod.bot.rest.fetch_channel(ctx.channel_id)
    # -------------------------------------------------------
    embed = hikari.Embed(description=embed_description)
    if anonym_author.lower() == "no": embed.set_author(name=ctx.author.username, icon=ctx.author.display_avatar_url)
    # -------------------------------------------------------
    if embed_title: embed.title = embed_title
    if embed_colour: embed.colour = get_hex(embed_colour)
    if embed_image_url: embed.set_image(embed_image_url)
    if embed_addit_message: return await channel.send(embed_addit_message, embed=embed)
    return await channel.send(embed=embed)
        

@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.add_checks(lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@mod.command
@lightbulb.option(name="poll_title", description="The title of the poll!", type=str, required=False)
@lightbulb.option(name="poll_description", description="The description of the poll!", type=str, required=False)
@lightbulb.option(name="option_one", description="The first option!", required=True, type=str)
@lightbulb.option(name="option_two", description="The second option!", required=True, type=str)
@lightbulb.option(name="option_three", description="The third option!", required=False, type=str)
@lightbulb.option(name="option_four", description="The fourth option!", required=False, type=str)
@lightbulb.option(name="option_five", description="The fifth option!", required=False, type=str)
@lightbulb.option(name="option_six", description="The sixth option!", required=False, type=str)
@lightbulb.option(name="timed_poll", description="Should the poll have a timeout or not? Results after end if timeouts!", choices=["Yes", "No"], required=False, type=str, default="No")
@lightbulb.command(name="poll", description="Raise a poll!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def create_poll(ctx: lightbulb.SlashContext):
    ...

def load(bot: lightbulb.BotApp):
    bot.add_plugin(mod)