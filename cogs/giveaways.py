import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
import asyncio
import random

class Giveaways(commands.Cog):
    def __init__(self, client):
        self.client = client

    def convert(self, time):
        pos = ["с","м","ч","д"]

        time_dict = {"с" : 1, "м" : 60, "ч" : 3600 , "д" : 3600*24}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]

    @commands.group(aliases = ['розыгрыш'])
    async def giveaway(self, ctx):
        pass

    @giveaway.command(aliases = ['создать'])
    
    @commands.has_permissions(administrator = True)
    async def start(self, ctx):
        question1 = nextcord.Embed(title=  "<a:tadatada:928259276823224341> Вопрос №1", timestamp=ctx.message.created_at, color=0x2F3136)
        question1.add_field(name = "Вопрос:", value = f"В каком канале будет проходить розыгрыш?")
        question1.add_field(name = "Пример:", value =f"Упомяните канал, например: {ctx.channel.mention}")
        question1.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
        
        question2 = nextcord.Embed(title=  "<a:tadatada:928259276823224341> Вопрос №2", timestamp=ctx.message.created_at, color=0x2F3136)
        question2.add_field(name = "Вопрос:", value = f"Как долго будет длиться розыгрыш? ")
        question2.add_field(name = "Пример:", value =f"Установите время, пример:\n<число>(с|м|ч|д)")
        question2.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)

        question3 = nextcord.Embed(title=  "<a:tadatada:928259276823224341> Вопрос №3", timestamp=ctx.message.created_at, color=0x2F3136)
        question3.add_field(name = "Вопрос:", value = f"Какой будет приз?")
        question3.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)

        errorEmbed1 = nextcord.Embed(title = '<a:checkoff:928259276273758208> Ошибка', timestamp=ctx.message.created_at, color=0x2F3136)
        errorEmbed1.add_field(name = "Причина:", value = "Вы неверно упомянули канал!")
        errorEmbed1.add_field(name = "Решение:", value = f"{ctx.channel.mention}")
        errorEmbed1.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)

        errorEmbed2 = nextcord.Embed(title = '<a:checkoff:928259276273758208> Ошибка', timestamp=ctx.message.created_at, color=0x2F3136)
        errorEmbed2.add_field(name = "Причина:", value = "Вы неверно установили время!")
        errorEmbed2.add_field(name = "Решение:", value = f"Напишите число и (с|м|ч|д)")
        errorEmbed2.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)

        timeDelay = nextcord.Embed(title = '<a:checkoff:928259276273758208> Ошибка', timestamp=ctx.message.created_at, color=0x2F3136)
        timeDelay.add_field(name = "Причина:", value = "Вы не успели ответить!")
        timeDelay.add_field(name = "Решение:", value = "Успейте ответить, пока не прошло 45 секунд!")
        timeDelay.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)

        questions = [question1, question2, question3]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(embed = i)

            try:
                msg = await self.client.wait_for('message', timeout=45.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(embed = timeDelay)
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(embed = errorEmbed1)
            return

        channel = self.client.get_channel(c_id)
        time = self.convert(answers[1])

        if time == -1:
            await ctx.send(embed = errorEmbed2)
            return
        elif time == -2:
            await ctx.send(f"Отрицательно число не подойдёт!")
            return

        prize = answers[2]
        
        
        await ctx.send(f"Розыгрыш будет проведён в {channel.mention}!")
        
        embed = nextcord.Embed(title = "<a:tadatada:928259276823224341> Розыгрыш!", description = f"{prize}", timestamp=ctx.message.created_at, color=0x2F3136)
        embed.add_field(name = "Создал:", value = ctx.author.mention)
        if time >= 3600:
            if time < 86400:
                embed.set_footer(text = f"Заканчивается через {round(time/3600, 1)} часов")
        if time < 3600:
            if time > 60:
                embed.set_footer(text = f"Заканчивается через {round(time/60, 1)} минут")
            elif time == 60:
                embed.set_footer(text = f"Заканчивается через {round(time/60, 1)} минут")
        if time < 60:
            embed.set_footer(text = f"Заканчивается через {round(time, 1)} секунд")
        if time >= 86400:
            embed.set_footer(text = f"Заканчивается через {round(time/86400, 1)} дней")
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
        my_msg = await channel.send(embed = embed)
        
        await my_msg.add_reaction("🎉")
        
        await asyncio.sleep(time)
        
        new_msg = await channel.fetch_message(my_msg.id)
        
        users = await new_msg.reactions[0].users().flatten()
        
        users.pop(users.index(self.client.user))
        
        if len(users) == 0:
            em = nextcord.Embed(title = '<a:checkoff:928259276273758208> Ошибка', timestamp=ctx.message.created_at, color=0x2F3136)
            em.add_field(name = "Причина:", value = "Никто не участвовал в розыгрыше")
            em.add_field(name = "Решение:", value = "Не делайте розыгрыши на пустых серверах ._.")
            await channel.send(embed = em)
            return
        
        winner = random.choice(users)
        
        newembed = nextcord.Embed(title = "<a:tadatada:928259276823224341> Розыгрыш!", description = f"{prize}", timestamp=ctx.message.created_at, color=0x2F3136)
        newembed.add_field(name = "Создал:", value = ctx.author.mention)
        
        newembed.add_field(name = "<a:tadatada:928259276823224341> Победитель", value = f"{winner.mention}")
        newembed.set_footer(text = f"Заканчивается через {answers[1]}")
        newembed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
        await my_msg.edit(embed = newembed)
        await channel.send(f"Ура!! {winner.mention} выиграл {prize}!")

    @giveaway.command(aliases=['greroll', 'перевыбрать'])
    
    @has_permissions(manage_guild = True)
    async def reroll(self,ctx, channel : nextcord.TextChannel, id_ : int):
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("Айди неверный!\nУкажите канал и айди сообщения!")
            return

        if new_msg.author != self.client.user:
            em = nextcord.Embed(title=  '<a:checkoff:928259276273758208> Ошибка', description = f"([Ссылка]({new_msg.jump_url}))", color=0x2F3136)
            em.add_field(name = "Причина:", value = "Указаное вами сообщение... не моё!")
            em.add_field(name ="Решение", value = "Указывайте айди моего сообщения!")
            em.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
            return await ctx.send(embed = em)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)
        await channel.send(f"<a:tadatada:928259276823224341> Ура!! Новый победитель: {winner.mention}!")

def setup(client):
    client.add_cog(Giveaways(client))
