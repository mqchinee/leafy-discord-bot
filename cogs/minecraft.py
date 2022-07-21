import nextcord
from nextcord.ext import commands
import aiomojang

class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['мкстата'])
    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def mcstats(self, ctx, player: str):
        profile = aiomojang.Player(player)
        try:
            embed = nextcord.Embed(title=f"<a:mc:928259275527184434> Информация про {player}: ", color=0x2F3136)
            embed.add_field(name="Имя: ", value=player)
            embed.add_field(name="UUID: ", value=await profile.uuid, inline=False)
            embed.add_field(name="Скин: ", value="<*>", inline=False)
            embed.set_image(url = await profile.get_skin())
            embed.set_author(name = player, icon_url = await profile.get_skin())
            embed.set_footer(text = "Запросил: {}".format(ctx.author.name), icon_url = ctx.author.display_avatar)
            await ctx.send(embed=embed)
        except aiomojang.exceptions.ApiException:
            return await ctx.send(f"Пользователя с именем {player} не найдено.")

    @commands.command(aliases = ['мкистория'])
    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def mchistory(self, ctx, player: str):
        profile = aiomojang.Player(player)
        embed = nextcord.Embed(title=f"<a:mc:928259275527184434> История имён игрока {player}:", color=0x2F3136)
        i = 1 
        for x in await profile.get_history():
            embed.add_field(name = f"Имя #{i}: ", value = x['name'], inline=False)
            i = i + 1
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Minecraft(client))