import nextcord
import sys
from nextcord.ext import commands


class loadunload(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def coglist(self, ctx):
        embed = nextcord.Embed(title='Список доступных модулей:', description=f'{ctx.author.mention}, список модулей:\n`emoji` `invites` `requests` `voice` `giveaways` `load` `minecraft` `other` `wiki` `roleplay` `channel` `mod` `pictures` `welcome` `levels` `gen` `autorole` `guildlogs` `react` `automod` `misc` `ownertools` `tag` `selfroles`', colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
        embed.set_footer(text=f"Всего модулей: 23", icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"Модуль `{extension}` был успешно загружен!")
        except:
            return await ctx.send("Этот модуль уже загружен либо его не существует!")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        if extension == "load":
            return await ctx.send('Нельзя выгрузить этот модуль!')
        else:
            try:
                self.client.unload_extension(f"cogs.{extension}")
                await ctx.send(f"Модуль `{extension}` был успешно выгружен!")
            except:
                return await ctx.send("Модуль уже выгружен либо его не существует!")

    @commands.command(aliases = ['reload'])
    @commands.is_owner()
    async def reloadd(self, ctx, extension):
        try:
            self.client.unload_extension(f"cogs.{extension}")
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"Модуль `{extension}` был успешно перезагружен!")
        except:
            return await ctx.send("Модуля не существует!")

    @load.error
    async def error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

    @unload.error
    async def error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

    @reloadd.error
    async def error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

    @coglist.error
    async def error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

    @commands.command()
    @commands.is_owner()
    async def reboot(self, ctx):
        await ctx.send('Перезагружаюсь...')
        sys.exit()

    @reboot.error
    async def error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

def setup(client):
    client.add_cog(loadunload(client))