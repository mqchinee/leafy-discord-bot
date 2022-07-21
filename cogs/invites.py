import nextcord
from nextcord.ext import commands


class Invites(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['приглашения'])
    
    async def invcount(self, ctx, user:nextcord.Member=None):
        if user is None:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == ctx.author:
                    total_invites += i.uses
            await ctx.send(f"Вы пригласили {total_invites} пользователей на этот сервер!")
        else:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == user:
                    total_invites += i.uses

            await ctx.send(f"{user.mention} пригласил(а) {total_invites} пользователей на этот сервер!")


def setup(client):
    client.add_cog(Invites(client))