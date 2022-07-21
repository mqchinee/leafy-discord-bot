# Настройка
import nextcord
import typing
import asyncio
import json
import requests
import random
import datetime
import aiohttp
from utils import default, http
import os
import sqlite3
import urllib.parse, urllib.request, re
from nextcord.utils import get
from itertools import cycle
from io import BytesIO
from nextcord.ext import commands, tasks
from nextcord import Member
from nextcord.ext.commands import has_permissions, MissingPermissions, cooldown, BucketType
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import psutil

class Misc(commands.Cog, name ="Misc!"):
	def __init__(self,client):
		self.client = client

	@commands.command(aliases = ['ковид'])
	async def covid(self, ctx, *, country: str):
		async with ctx.channel.typing():
			r = await http.get(f"https://disease.sh/v3/covid-19/countries/{country.lower()}", res_method="json")

			if "message" in r:
				return await ctx.send(f"API отклонило запрос:\n{r['message']}")

			json_data = [
				("Случаев заражения", r["cases"]), ("Смертей", r["deaths"]),
				("Случаев выздоровления", r["recovered"]), ("Активных случаев", r["active"]),
				("Общее критическое состояние", r["critical"]), ("Случаев сегодня", r["todayCases"]),
				("Умерли сегодня", r["todayDeaths"]), ("Выздоровели сегодня", r["todayRecovered"])
			]

			embed = nextcord.Embed(
				description=f"Информация была обновлена: <t:{int(r['updated'] / 1000)}:R>"
			)

			for name, value in json_data:
				embed.add_field(
					name=name, value=f"{value:,}", inline=False if isinstance(value, int) else value
				)

			await ctx.send(
				f"**COVID-19**: статистика :flag_{r['countryInfo']['iso2'].lower()}: "
				f"**{country.capitalize()}** *({r['countryInfo']['iso3']})*",
				embed=embed
			)

	@commands.command(hidden=True, aliases=['cg'])
	@commands.is_owner()
	async def chooseguilds(self, ctx, type1, integer: int):
		if type1 == "b":
			msg = '```java\n'
			msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Участников', 'Название', 'Создатель')
			for guild in self.client.guilds:
				if guild.member_count >= integer:
					msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
			msg += '```'
		elif type1 == "s":
			msg = '```java\n'
			msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Участников', 'Название', 'Создатель')
			for guild in self.client.guilds:
				if guild.member_count < integer:
					msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
			msg += '```'
		else:
			return await ctx.send('._.')
		await ctx.send(msg)

	@commands.command(hidden=True, aliases=['topguilds'])
	@commands.is_owner()
	async def topservers(self, ctx):
		msg = '```java\n'
		msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Участников', 'Название', 'Создатель')
		for guild in self.client.guilds:
			if guild.member_count >= 20:
				msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
		msg += '```'
		await ctx.send(msg)

	@commands.command(hidden=True, aliases=['guilds'])
	@commands.is_owner()
	async def servers(self, ctx):
		msg = '```java\n'
		msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Участников', 'Название', 'Создатель')
		for guild in self.client.guilds:
			if guild.member_count < 20:
				msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
		msg += '```'
		await ctx.send(msg)

	@commands.command()
	@commands.is_owner()
	async def ginfo(self, ctx, id_: int):
		guild = self.client.get_guild(int(id_))
		await ctx.message.delete()
		if guild.icon:
			embed = nextcord.Embed(title=guild.name, timestamp=ctx.message.created_at, colour=nextcord.Colour.blurple())
			embed.set_thumbnail(url=guild.icon)
			embed.set_author(name=guild.owner, icon_url=guild.owner.display_avatar)
			embed.set_footer(text=f'ID: {guild.id}', icon_url=ctx.author.display_avatar)
			embed.add_field(name=f'Участников:', value=guild.member_count)
			embed.add_field(name=f'Создан:', value=default.date(guild.created_at, ago=True))
			await ctx.send(embed=embed)
		if not guild.icon:
			embed = nextcord.Embed(title=guild.name, timestamp=ctx.message.created_at, colour=nextcord.Colour.blurple())
			embed.set_author(name=guild.owner, icon_url=guild.owner.display_avatar)
			embed.set_footer(text=f'ID: {guild.id}', icon_url=ctx.author.display_avatar)
			embed.add_field(name=f'Участников:', value=guild.member_count)
			embed.add_field(name=f'Создан:', value=default.date(guild.created_at, ago=True))
			await ctx.send(embed=embed)


	@ginfo.error
	async def error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

	@servers.error
	async def error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

	@topservers.error
	async def error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

	@commands.command(hidden=True)
	@commands.is_owner()
	async def discriminator(self, ctx, disc: str):

		discriminator = disc
		memberList = ''

		for guild in self.client.guilds:
			for member in guild.members:
				if member.discriminator == discriminator and member.discriminator not in memberList:
					memberList += f'{member}\n'

		if memberList:
			await ctx.send(memberList)
		else:
			await ctx.send(f'Ничего не найдено по запросу {disc}')

	@discriminator.error
	async def error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

	@commands.command()
	@commands.is_owner()
	async def gh(self, ctx):
		await ctx.message.delete()
		await ctx.send('Скажи теперь')
		await asyncio.sleep(1)
		await ctx.send('Скажи мне точно')
		await asyncio.sleep(2)
		await ctx.send('Как всё это понять?')
		await asyncio.sleep(3)
		await ctx.send('Какой-то странный зверь')
		await asyncio.sleep(1)
		await ctx.send('Живёт внутри меня.')
		await asyncio.sleep(2)
		await ctx.send('Я уничтожен, уничтожен')
		await asyncio.sleep(2)
		await ctx.send('Есть лёд, но нет огня.')
		await asyncio.sleep(1)
		await ctx.send('И на исходе дня')
		await asyncio.sleep(1)
		await ctx.send('Твоей улыбки дверь.')
		await asyncio.sleep(3)
		await ctx.send('Иду вперёд я не спеша')
		await asyncio.sleep(1)
		await ctx.send('Мне тяжело дышать')
		await asyncio.sleep(1)
		await ctx.send('Не разрушай нет, не разрушай!')
		await asyncio.sleep(1)
		await ctx.send('Стой!')
		await asyncio.sleep(1)
		await ctx.send('То сильный я, то слаб весьма')
		await asyncio.sleep(1)
		await ctx.send('Спокойный, но схожу с ума')
		await asyncio.sleep(1)
		await ctx.send('В смятении моя душа..')
		await asyncio.sleep(1)
		await ctx.send('Я здесь, я стою, я один в кругу порочном')
		await asyncio.sleep(2)
		await ctx.send('Душа пуста, мир вокруг непрочный.')
		await asyncio.sleep(1)
		await ctx.send('Не усложняй же и не ищи меня.')
		await asyncio.sleep(1)
		await ctx.send('Я знаю точно')
		await asyncio.sleep(1)
		await ctx.send('В придуманный мир я попал невольно')
		await asyncio.sleep(1)
		await ctx.send('Теперь не хочу тебе делать больно')
		await asyncio.sleep(1)
		await ctx.send('Но иногда ты вспоминай меня')
		await asyncio.sleep(1)
		await ctx.send('Таким, каким был я')
		await asyncio.sleep(1)
		await ctx.send('Я в одиночестве вплетён')
		await asyncio.sleep(1)
		await ctx.send('Как в странный и безумный сон')
		await asyncio.sleep(1)
		await ctx.send('И памяти больше нет')
		await asyncio.sleep(1)
		await ctx.send('Лишь только холодный бред')
		await asyncio.sleep(1)
		await ctx.send('Движенья нет!')
		await asyncio.sleep(1)
		await ctx.send('Движенья нет!')
		await asyncio.sleep(1)
		await ctx.send('Движенья нет!')
		await asyncio.sleep(1)
		await ctx.send('Движенья нет!')
		await asyncio.sleep(1)
		await ctx.send('Движенья нет!')
		await asyncio.sleep(1)
		await ctx.send('Движенья нет!')
		await asyncio.sleep(1)
		await ctx.send('И только бред!')
		await asyncio.sleep(3)
		await ctx.send('Я в мире невзрачном')
		await asyncio.sleep(1)
		await ctx.send('Нелепом прозрачном')
		await asyncio.sleep(1)
		await ctx.send('Я сам не свой, во мне другой')
		await asyncio.sleep(1)
		await ctx.send('Он мне чужой, но он со мной')
		await asyncio.sleep(1)
		await ctx.send('То сильный я, то слаб весьма')
		await asyncio.sleep(1)
		await ctx.send('Спокойный, но схожу с ума')
		await asyncio.sleep(1)
		await ctx.send('В смятении моя душа')
		await asyncio.sleep(3)
		await ctx.send('Только')
		await asyncio.sleep(1)
		await ctx.send('Я здесь, я стою, я один в кругу порочном')
		await asyncio.sleep(1)
		await ctx.send('Душа пуста, мир вокруг непрочный')
		await asyncio.sleep(1)
		await ctx.send('Не усложняй же и не ищи меня')
		await asyncio.sleep(1)
		await ctx.send('Я знаю точно')
		await asyncio.sleep(1)
		await ctx.send('В придуманный мир я попал невольно')
		await asyncio.sleep(1)
		await ctx.send('Теперь не хочу тебе делать больно')
		await asyncio.sleep(1)
		await ctx.send('Но иногда ты вспоминай меня')
		await asyncio.sleep(1)
		await ctx.send('Таким, каким был я..')
		await asyncio.sleep(3)
		await ctx.send('Ты только помни.')
		await asyncio.sleep(1)
		await ctx.send('Ты только помни.')
		await asyncio.sleep(1)
		await ctx.send('Ты только помни.')
		await asyncio.sleep(1)
		await ctx.send('Ты только помни.')
		await asyncio.sleep(1)
		await ctx.send('Прими то, что есть, что уже случилось')
		await asyncio.sleep(1)
		await ctx.send('И боготвори, что не изменилось')
		await asyncio.sleep(1)
		await ctx.send('Я только прошу, не забывай меня')

def setup(client):
	client.add_cog(Misc(client))