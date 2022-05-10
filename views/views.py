import hikari
import miru

class KickView(miru.View):
    def __init__(self):
        self.confirm = False
        super().__init__(timeout=15, autodefer=True)

    @miru.button(label="Kick", style=hikari.ButtonStyle.SUCCESS)
    async def confirm_kick(self, button: miru.Button, ctx: miru.Context) -> None:
        self.confirm = True
        self.stop()
    
    @miru.button(label="Cancel", style=hikari.ButtonStyle.DANGER)
    async def cancel_kick(self, button: miru.Button, ctx: miru.Context) -> None:
        self.stop()

    async def on_timeout(self):
        self.stop()

class BanView(miru.View):
    def __init__(self):
        self.confirm = False
        super().__init__(timeout=15, autodefer=True)
    
    @miru.button(label="Ban", style=hikari.ButtonStyle.SUCCESS)
    async def confirm_ban(self, button: miru.Button, ctx: miru.Context) -> None:
        self.confirm = True
        self.stop()
    
    @miru.button(label="Cancel", style=hikari.ButtonStyle.DANGER)
    async def cancel_ban(self, button: miru.Button, ctx: miru.Context) -> None:
        self.stop()

    async def on_timeout(self):
        self.stop()