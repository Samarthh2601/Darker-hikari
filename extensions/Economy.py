import lightbulb
import hikari
import random
import asyncio

class Economy(lightbulb.Plugin):
    def __init__(self):
        self.bot: lightbulb.BotApp
        super().__init__("Economy", "Economy Commands!")
    
eco = Economy()

@eco.command
@lightbulb.command(name="create_account", description="Create an account for economy commands!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def create_acc(ctx: lightbulb.SlashContext):
    new_d = await eco.bot.eco.create(ctx.author.id)
    return await ctx.respond(f"Your account details! Wallet: **{new_d.wallet}** | Bank: **{new_d.bank}**")

@eco.command
@lightbulb.option(name="member", description="The member to check the balance of!", required=False, type=hikari.Member)
@lightbulb.command(name="balance", description="Check wallet and bank balance!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def balance(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get("member") or ctx.author
    data = await eco.bot.eco.create(member.id)
    embed = hikari.Embed(title="Balance!", description=member, colour=ctx.author.accent_colour).add_field("Wallet", data.wallet).add_field("Bank", data.bank)
    if member.avatar_url:
        embed.set_thumbnail(member.avatar_url)
    await ctx.respond(embed=embed)

@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.command(name="beg", description="Beg for Coins!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def beg(ctx: lightbulb.SlashContext):
    c = random.randint(1, 2)
    if c == 1:
        return await ctx.respond("Go find a job or something, good for nothing.")
    user_data = await eco.bot.eco.create(ctx.author.id)
    random_money = random.randint(1, 199)
    await ctx.respond(f"You really got **{random_money}** Dark Coins, lucky you! You now have **{user_data.wallet+random_money}** Dark Coins in your wallet!")
    return await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet+random_money)

@lightbulb.add_cooldown(30.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.command(name="search", description="Search for a few Dark Coins, maybe", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def search(ctx: lightbulb.SlashContext):
    data = await eco.bot.eco.create(ctx.author.id)
    c = random.randint(1, 2)
    await ctx.respond("Searching...")
    await asyncio.sleep(2)
    if c == 1:
        return await ctx.respond("You found nothing!")
    if c == 2:
        await eco.bot.eco.update(ctx.author.id, wallet=data.wallet-500)
        return await ctx.respond("The Dark Police caught you and charged you **500** Dark Coins...")
    r_money = random.randint(100, 499)
    await eco.bot.eco.update(ctx.author.id, wallet=data.wallet+r_money)
    return await ctx.respond(f"Lucky you, found {r_money} Dark Coins! You now have {data.wallet+r_money} Dark Coins in your wallet!")

@lightbulb.add_cooldown(30.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="amount", description="The amount to deposit!", type=int, required=True)
@lightbulb.command(name="deposit", description="Deposit money to the bank from your wallet!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def dep(ctx: lightbulb.SlashContext):
    amount = ctx._options.get("amount")
    user_data = await eco.bot.eco.read(ctx.author.id)
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")
    if amount > user_data.wallet:
        return await ctx.respond(f"The amount of Dark Coins in your wallet are less than the number to deposited! Wallet balance: **{user_data.wallet}**")
    if user_data.wallet-amount < 475:
        return await ctx.respond("You must keep at least **475** Dark Coins in your wallet!")

    await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet-amount, bank=user_data.wallet+amount)
    return await ctx.respond(f"Successfully deposited **{amount}** Dark Coins to your bank! You now have **{user_data.wallet-amount}** Dark Coins in your wallet and **{user_data.bank+amount}** Dark Coins in your bank!")

@lightbulb.add_cooldown(30.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="amount", description="The amount to withdraw!", type=int, required=True)
@lightbulb.command(name="withdraw", description="Withdraw money from the bank to your wallet!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def withdraw(ctx: lightbulb.SlashContext):
    amount = ctx._options.get("amount")
    user_data = await eco.bot.eco.read(ctx.author.id)
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")
    if amount > user_data.bank:
        return await ctx.respond(f"The amount of Dark Coins in your bank is lesser than the amount! Bank balance {user_data.bank}")
    await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet+amount, bank=user_data.bank-amount)
    return await ctx.respond(f"Successfully withdrew **{amount}** Dark Coins from your bank! You now have **{user_data.wallet+amount}** Dark Coins in your wallet and **{user_data.bank-amount}** Dark Coins in your bank!")

@lightbulb.add_cooldown(150.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="member", description="Which member to rob?", type=hikari.Member, required=True)
@lightbulb.command(name="rob", description="Rob another robber (member)!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rob_user(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get("member")
    user_data = await eco.bot.eco.read(ctx.author.id)
    member_data = await eco.bot.eco.create(member.id)
    if member_data.wallet < 500:
        return await ctx.respond(f"**{member}** doesn't even have 500 Dark Coins, not worth it.")
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")
    if user_data.wallet < 500:
        return await ctx.respond("You must have 500 Dark Coins in your wallet to rob others!")
    c = random.randint(1, 4)
    if c == 4:
        return await ctx.respond("You came back empty-handed...how sad.")
    elif c == 3:
        rc = random.randint(1, user_data.wallet)
        await ctx.respond(f"**{member}** caught you while you were robbing them and stole {rc} Dark Coins from you! Your total wallet balance is now **{user_data.wallet-rc}**!")
        await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet-rc)
        await eco.bot.eco.update(member.id, wallet=member_data.wallet+rc)
    elif c == 2 or c == 1:
        rc = random.randint(1, member_data.wallet)
        await ctx.respond(f"You stole {rc} Dark Coins from **{member}**! Your total wallet balance is now **{user_data.wallet+rc}**!")
        await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet+rc)
        await eco.bot.eco.update(member.id, wallet=member_data.wallet-rc)

@lightbulb.add_cooldown(250.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="member", description="The member to heist!", type=hikari.Member, required=True)
@lightbulb.command(name="heist", description="Heist the bank of a member!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def heist_(ctx: lightbulb.SlashContext):
    member = ctx._options.get("member")
    user_data = await eco.bot.eco.read(ctx.author.id)
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")
    member_data = await eco.bot.eco.create(ctx.author.id)
    if member_data.bank < 1000:
        return await ctx.respond(f"**{member}** isn't worth it. They don't even have 1000 Dark Coins in their bank.")
    c = random.randint(1, 4)
    if c == 4 or c == 2:
        return await ctx.respond("You came back empty-handed...how sad.")
    elif c == 3:
        rc = random.randint(1, user_data.bank)
        await ctx.respond(f"**{member}** caught you while you were robbing them and stole {rc} Dark Coins from you! Your total bank balance is now **{user_data.bank-rc}**!")
        await eco.bot.eco.update(ctx.author.id, bank=user_data.bank-rc)
        await eco.bot.eco.update(member.id, bank=member_data.bank+rc)
    elif c == 1:
        rc = random.randint(1, member_data.bank)
        await ctx.respond(f"You stole {rc} Dark Coins from **{member}**! Your total bank balance is now **{user_data.bank+rc}**!")
        await eco.bot.eco.update(ctx.author.id, bank=user_data.bank+rc)
        await eco.bot.eco.update(member.id, bank=member_data.bank-rc)

@lightbulb.add_cooldown(200.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="member", description="The member to send the coins!", type=hikari.Member, required=True)
@lightbulb.option(name="amount", description="The amount of coins to send!", type=int, required=True)
@lightbulb.command(name="send_coins", description="Send coins to another member!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def send_coins(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx._options.get("member")
    amount = ctx._options.get("amount")
    user_data = await eco.bot.eco.read(ctx.author.id)
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")
    if amount > user_data.wallet:
        return await ctx.respond("The amount you're trying to transfer is greater than your wallet balance.")
    await ctx.respond(f"Successfully sent **{member}** {amount} Dark Coin(s)! Your wallet balance is now **{user_data.wallet-amount}**")
    await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet-amount)
    member_data = await eco.bot.eco.create(member.id)
    await eco.bot.eco.update(member.id, wallet=member_data.wallet+(amount))

@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="amount", description="The amount of coins to bet!", type=int, required=True)
@lightbulb.option(name="side", description="Heads or Tails?", type=str, required=True, choices=["Heads", "Tails"])
@lightbulb.command(name="coinflip", description="Flip a coin and get more coins or lost them.", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def cf(ctx: lightbulb.SlashContext):
    amount = ctx._options.get("amount")
    side = ctx._options.get("side")
    user_data = await eco.bot.eco.read(ctx.author.id)
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")
    if amount > user_data.wallet:
        return await ctx.respond("The amount you're trying to bet is more than your wallet balance.")

    c = random.choice(["heads", "tails"])
    await ctx.respond("Flipping a coin for ya...")
    if side.lower() == c:
        await ctx.respond(f"You won! Your wallet balance is now **{user_data.wallet+amount*2}**!")
        return await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet+amount*2)

    await ctx.respond(f"You lost. You wallet balance is now **{user_data.wallet-amount}**!")
    await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet-amount)

@lightbulb.add_cooldown(60.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="amount", description="The amount to bet!", type=int, required=True)
@lightbulb.command(name="bet", description="Bet your coins for greater amounts or lose it!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def bet_coins(ctx: lightbulb.SlashContext):
    amount = ctx._options.get("amount")
    user_data = await eco.bot.eco.read(ctx.author.id)
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")
    if amount > user_data.wallet:
        return await ctx.respond("The amount you're trying to bet is more than your wallet balance.")

    c = random.randint(1, 4)
    if c == 1 or c == 2 or c == 3:
        await ctx.respond(f"You lost! Your wallet balance is now **{user_data.wallet-amount}**")
        return await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet-amount)
    await ctx.respond(f"You won! Your wallet balance is now **{user_data.wallet+(amount*5)}**")
    await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet+(amount*5))

@lightbulb.add_cooldown(30.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="number", description="The number to predict!", required=True, type=int, choices=[1, 2, 3, 4, 5, 6])
@lightbulb.command(name="roll", description="Roll the dice and earn coins!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def roll_(ctx: lightbulb.SlashContext):
    number = ctx._options.get("number")
    user_data = await eco.bot.eco.read(ctx.author.id)
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")    
    c = random.randint(1, 6)
    if c != number:
        return await ctx.respond(f"The dice rolled to **{c}** but you chose the number **{number}**")
    await ctx.respond(f"You won! Your wallet balance is now **{user_data.wallet+200}**")
    await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet+200)

@lightbulb.add_cooldown(30.0, 1, lightbulb.UserBucket)
@eco.command
@lightbulb.option(name="amount", description="The amount to bet!", type=int, required=True)
@lightbulb.command(name="slots", description="Play the Slots minigame and earn coins!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def slots_(ctx: lightbulb.SlashContext):
    amount = ctx._options.get("amount")
    user_data = await eco.bot.eco.read(ctx.author.id)
    if not user_data:
        return await ctx.respond("You do not have an account yet! Run `/create_account` to create one!")
    if amount > user_data.wallet:
        return await ctx.respond("The amount you're trying to bet is more than your wallet balance.")

    opts = [random.choice([":strawberry:", ":apple:", ":mango:"]) for _ in range(3)]    
    if opts[0] == opts[1] and opts[0] == opts[2]:
        await ctx.respond(f"{' | '.join(opts)}, You won! Your wallet balance is now **{user_data.wallet+(amount*3)}**")
        return await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet+(amount*3))
    await ctx.respond(f"{' | '.join(opts)}, You lost! Your wallet balance is now **{user_data.wallet-amount}**!")
    await eco.bot.eco.update(ctx.author.id, wallet=user_data.wallet-amount)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(eco)