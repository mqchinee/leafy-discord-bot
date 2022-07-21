#Настройка
import nextcord
import typing
import asyncio
import platform
import json
import requests
import random
import datetime
import aiohttp
import os
import sqlite3
import urllib.parse, urllib.request, re
from nextcord.utils import get
from itertools import cycle
from io import BytesIO
from nextcord.ext import commands, tasks
from nextcord import Member, Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext.commands import has_permissions, MissingPermissions, cooldown, BucketType
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import psutil
from modules.components import *
from utils import default, http

ts = 0
tm = 0
th = 0
td = 0

intents = nextcord.Intents.all()
intents.members = True

connection1 = sqlite3.connect('data.db')
cursor1 = connection1.cursor()

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

async def get_prefix(client, message):
	cursor.execute("SELECT prefix FROM prefixes WHERE id = ?", (message.guild.id,))
	data = cursor.fetchone()
	if data:
		return data
	else:
		try:
			cursor.execute("INSERT INTO prefixes (prefix, id) VALUES (?, ?)", ('?', message.guild.id,))
			cursor.execute("SELECT prefix FROM prefixes WHERE id = ?", (message.guild.id,))
			data = cursor.fetchone()
			if data:
				cursor.execute("UPDATE prefixes SET prefix = ? WHERE id = ?", ('?', message.guild.id,))
		except Exception:
			return '?'

client = commands.AutoShardedBot(shard_count=5, command_prefix = get_prefix , intents=intents)
client.remove_command('help')
# Слова
hwords = ['привет бот', 'ку бот', 'здарова бот', 'хай бот', 'приветик бот', 'дратути бот']
awords = ['команды','помощь','что здесь делать?']
gwords = ['пока бот','досвидания бот','удачи бот']
# Страницы (помощь)

# Подключение к консоли
@client.event
async def on_ready():   
	await client.change_presence(activity=nextcord.Streaming(name=f"?help | leafy.cf | v3.7.3", url="https://www.twitch.tv/twitch"))
	uptimeCounter.start()
	cursor.execute("""CREATE TABLE IF NOT EXISTS users (
		name TEXT,
		id INT,
		cash BIGINT,
		rep INT,
		lvl INT,
		gamesplayed INT,
		bank BIGINT
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
		role_id INT,
		id INT,
		cost BIGINT
		)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS prefixes (
		prefix TEXT,
		id INT
		)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS gmoney (
		guild INT,
		cash BIGINT,
		name TEXT
		)""")
	
	for guild in client.guilds:
		if cursor.execute(f"SELECT guild FROM gmoney WHERE guild = ?", (guild.id, )).fetchone() is None:
			cursor.execute(f"INSERT INTO gmoney VALUES (?, 0, ?)", (guild.id, guild.name))
		else:
			pass
		for member in guild.members:
			if cursor.execute(f"SELECT id FROM users WHERE id = ?", (member.id, )).fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES (?, ?, 0, 0, 1, 0, 0)", (str(member), member.id))
			if cursor1.execute(f"SELECT user_id FROM users WHERE user_id = ? AND guild_id = ?", (member.id, member.guild.id,)).fetchone() is None:
				cursor1.execute(f"INSERT INTO users VALUES (?, 0, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ?)", (str(member), member.id, member.guild.id,))
			else:
				pass
	connection1.commit()
	connection.commit()
	print("-------------------")
	print('Бот онлайн')
	print("-------------------")
	print(f"Присоединился как {client.user.name}")
	print(f"Версия API: {nextcord.__version__}")
	print("-------------------")
	print(f"Создатель: mqchinee#1422")
	print("-------------------")
	print(f"Серверов: {len(client.guilds)}")
	print("-------------------")
	channelstart = client.get_channel(934409321733849108)
	embed=nextcord.Embed(title='Запуск', description=f'Присоединился как:\n`{client.user.name}`\nВерсия API:\n`{nextcord.__version__}`\nСерверов:\n`{len(client.guilds)}`\nШардов (Кластеров):\n`5`\nПинг:\n`{client.latency*1000} мс`', color=0x2F3136)
	embed.add_field(name='Нагрузка ЦПУ:', value=f'`{psutil.cpu_percent()}%`', inline=True)
	embed.add_field(name='Нагрузка ОЗУ:', value=f'`{psutil.virtual_memory()[2]}%`', inline=True)
	embed.add_field(name='Пользователей:', value=f'`{len(set(client.get_all_members()))}`', inline=False)
	embed.add_field(name='Каналов:', value=f'`{len(set(client.get_all_channels()))}`', inline=False)
	embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	await channelstart.send(embed=embed)
	
# Префикс
@client.event
async def on_guild_join(guild):
	channelguild = client.get_channel(934413579174686781)
	await channelguild.send(embed=nextcord.Embed(title='Бот добавлен', description=f'Информация: `{guild.name}` | `{guild.id}` | `{guild.owner}`\nСерверов: {len(client.guilds)}', color=0x2F3136))
	if guild.icon:
		embed = nextcord.Embed(title=guild.name, timestamp=datetime.datetime.now(), colour=nextcord.Colour.blurple())
		embed.set_thumbnail(url=guild.icon)
		embed.set_author(name=guild.owner, icon_url=guild.owner.display_avatar)
		embed.set_footer(text=f'ID: {guild.id}', icon_url=client.user.display_avatar)
		embed.add_field(name=f'Участников:', value=guild.member_count)
		embed.add_field(name=f'Создан:', value=default.date(guild.created_at, ago=True))
		await channelguild.send(embed=embed)
	if not guild.icon:
		embed = nextcord.Embed(title=guild.name, timestamp=datetime.datetime.now(), colour=nextcord.Colour.blurple())
		embed.set_author(name=guild.owner, icon_url=guild.owner.display_avatar)
		embed.set_footer(text=f'ID: {guild.id}', icon_url=client.user.display_avatar)
		embed.add_field(name=f'Участников:', value=guild.member_count)
		embed.add_field(name=f'Создан:', value=default.date(guild.created_at, ago=True))
		await channelguild.send(embed=embed)
	cursor.execute("INSERT INTO prefixes (prefix, id) VALUES (?, ?)", ('?', guild.id,))
	connection.commit()

	for guild in client.guilds:
		if cursor.execute(f"SELECT guild FROM gmoney WHERE guild = ?", (guild.id, )).fetchone() is None:
			cursor.execute(f"INSERT INTO gmoney VALUES (?, 0, ?)", (guild.id, guild.name))
			connection.commit()
		else:
			pass

	for member in guild.members:
		if cursor.execute(f"SELECT id FROM users WHERE id = ?", (member.id, )).fetchone() is None:
			cursor.execute(f"INSERT INTO users VALUES (?, ?, 0, 0, 1, 0, 0)", (str(member), member.id))
			connection.commit()
		if cursor1.execute(f"SELECT user_id FROM users WHERE user_id = ? AND guild_id = ?", (member.id, member.guild.id,)).fetchone() is None:
			cursor1.execute(f"INSERT INTO users VALUES (?, 0, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ?)", (str(member), member.id, member.guild.id,))
			connection1.commit()
		else:
			pass


	for channel in guild.text_channels:
		if channel.permissions_for(guild.me).send_messages:
			emb = nextcord.Embed(title = '👋 Спасибо, что пригласили меня!', description = '<:9294passed:926412397080629249> Привет, меня зовут Leafy.', colour = nextcord.Colour.from_rgb(255,255,255))
			emb.add_field(name='Что я могу?', value='`Я - универсальный бот!`\n**Я могу**:\n`Настройка сервера` `Модерация` `Информация` `Развлечения` `Манипуляции с картинками` `РП` `Экономика` `Розыгрыши` `Приветственные каналы` `Межсерверная система уровней` `Временные голосовые каналы` `NSFW`', inline=False)
			emb.add_field(name='Мой стандартный префикс:', value='`?`', inline=False)
			emb.add_field(name='Связь:', value='`mqchine#1422`', inline=False)
			emb.set_thumbnail(url = client.user.display_avatar)
			emb.set_author(name = guild.name, icon_url = guild.icon)
			emb.set_image(url='https://st3.depositphotos.com/32100976/34458/i/600/depositphotos_344586092-stock-photo-anime-wallpapers-black-white-anime.jpg')
			view = nextcord.ui.View()
			item = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "Сервер",emoji = "👑", url = "https://discord.gg/CT8VekA57Z")
			item2 = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "ВКонтакте",emoji = "🧭", url = "https://vk.com/kykarekman")
			item3 = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "Github",emoji = "🐱", url = "https://github.com/mqchinee")
			item4 = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "Сайт",emoji = "✅", url = "https://leafy.cf/")
			view.add_item(item)
			view.add_item(item2)
			view.add_item(item3)
			view.add_item(item4)
			await channel.send(embed=emb, view=view)
		break

@client.event
async def on_guild_remove(guild):
	channelguild = client.get_channel(934413579174686781)
	await channelguild.send(embed=nextcord.Embed(title='Бот удалён', description=f'Информация: `{guild.name}` | `{guild.id}` | `{guild.owner}`\nСерверов: {len(client.guilds)}', color=0x2F3136))
	if guild.icon:
		embed = nextcord.Embed(title=guild.name, timestamp=datetime.datetime.now(), colour=nextcord.Colour.blurple())
		embed.set_thumbnail(url=guild.icon)
		embed.set_author(name=guild.owner, icon_url=guild.owner.display_avatar)
		embed.set_footer(text=f'ID: {guild.id}', icon_url=client.user.display_avatar)
		embed.add_field(name=f'Участников:', value=guild.member_count)
		embed.add_field(name=f'Создан:', value=default.date(guild.created_at, ago=True))
		await channelguild.send(embed=embed)
	if not guild.icon:
		embed = nextcord.Embed(title=guild.name, timestamp=datetime.datetime.now(), colour=nextcord.Colour.blurple())
		embed.set_author(name=guild.owner, icon_url=guild.owner.display_avatar)
		embed.set_footer(text=f'ID: {guild.id}', icon_url=client.user.display_avatar)
		embed.add_field(name=f'Участников:', value=guild.member_count)
		embed.add_field(name=f'Создан:', value=default.date(guild.created_at, ago=True))
		await channelguild.send(embed=embed)
	cursor.execute("SELECT prefix FROM prefixes WHERE id = ?", (guild.id,))
	data = cursor.fetchone()
	if data:
		cursor.execute("DELETE FROM prefixes WHERE id = ?", (guild.id,))
	connection.commit()

@client.command(aliases=['префикс'])

async def setprefix(ctx, prefix=None):
	if (not ctx.author.guild_permissions.manage_channels):
		await ctx.send('<a:checkoff:928259276273758208> Недостаточно прав!')
		return

	if prefix is None:
		return await ctx.send('Нельзя указывать пустоту, если вы хотите префикс с пробелом, напишите текст в кавычках.. пример: ?setprefix "leafy "')

	cursor.execute("SELECT prefix FROM prefixes WHERE id = ?", (ctx.guild.id,))
	data = cursor.fetchone()
	if data:
		cursor.execute("UPDATE prefixes SET prefix = ? WHERE id = ?", (prefix, ctx.guild.id,))
		await ctx.send(f'<a:checkon:928259275090972772> Префикс бота изменён на `{prefix}`')
	else:
		cursor.execute("INSERT INTO prefixes (prefix, id) VALUES (?, ?)", ('?', ctx.guild.id,))
		cursor.execute("SELECT prefix FROM prefixes WHERE id = ?", (ctx.guild.id,))
		data = cursor.fetchone()
		if data:
			cursor.execute("UPDATE prefixes SET prefix = ? WHERE id = ?", (prefix, ctx.guild.id,))
			await ctx.send(f'<a:checkon:928259275090972772> Префикс бота изменён на `{prefix}`')
		else:
			return

	connection.commit()

# Привет!
@client.command( pass_context = True , aliases=['привет'])

async def hello(ctx, amount = 1):
	await ctx.channel.purge(limit=1)
	author = ctx.message.author
	await ctx.send(f'Привет, {author.mention}')

@client.command(aliases=['полотно'])
@commands.cooldown(1,20, commands.BucketType.guild)
async def paint(ctx):
	await ctx.message.delete()
	await ctx.send(f'{ctx.author.mention}\n||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||')
	await asyncio.sleep(1)
	await ctx.send(f'||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||')
	await asyncio.sleep(1)
	await ctx.send(f'||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||')
	await asyncio.sleep(1)
	await ctx.send(f'||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||')
	await asyncio.sleep(1)
	await ctx.send(f'||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||')
	await asyncio.sleep(1)
	await ctx.send(f'||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||')
	await asyncio.sleep(1)
	await ctx.send(f'||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||')
	await asyncio.sleep(1)
	await ctx.send(f'||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||||:white_large_square:||')

# Ответы
@client.event
async def on_message(message):
	dbhelp = sqlite3.connect('server.db')
	cursorhelp = dbhelp.cursor()
	cursorhelp.execute("SELECT prefix FROM prefixes WHERE id = ?", (message.guild.id,))
	resulthelp = cursorhelp.fetchone()
	msg = message.content.lower()
	await client.process_commands(message)
	if msg in hwords:
		await message.channel.send('Привет, чего хотел?')
	if msg in awords:
		await message.channel.send(f'Для просмора функционала напишите {str(resulthelp[0])}help !')
	if msg in gwords:
		await message.channel.send('Пока!')

	if client.user in message.mentions:
		if not message.author.bot:
			if message.reference is None:
				embed=nextcord.Embed(title='Эй!', description='Привет, меня зовут **Лифи**!\nЯ универсальный бот, ведь **мне доступны**:\n`Настройка сервера` `Модерация` `Информация` `Развлечения` `Манипуляции с картинками` `РП` `Экономика` `Розыгрыши` `Приветственные каналы` `Межсерверная система уровней` `Временные голосовые каналы` `NSFW`', color=0x2F3136)
				embed.add_field(name='Мой префикс на этом сервере:', value=f'**{str(resulthelp[0])}**', inline=False)
				embed.add_field(name='Полезное:', value=f'{str(resulthelp[0])}help | Вызвать меню помощи\n{str(resulthelp[0])}info | Настройки текущего сервера\nСайт: [Тык](https://www.leafy.cf)\n[Сервер поддержки](https://discord.gg/CT8VekA57Z)', inline=False)
				embed.set_thumbnail(url=client.user.display_avatar)
				await message.channel.send(embed=embed)

@client.event
async def on_member_join(member):
	if cursor.execute(f"SELECT id FROM users WHERE id = ?", (member.id, )).fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES (?, ?, 0, 0, 1, 0, 0)", (str(member), member.id))
		connection.commit()
	if cursor1.execute(f"SELECT user_id FROM users WHERE user_id = ? AND guild_id = ?", (member.id, member.guild.id,)).fetchone() is None:
		cursor1.execute(f"INSERT INTO users VALUES (?, 0, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ?)", (str(member), member.id, member.guild.id,))
		connection1.commit()
	else:
		pass

# Тест команд для овнера!
@client.command()
@commands.is_owner()
async def dev(ctx):
	await ctx.send('<a:checkon:928259275090972772> Эта команда тестовая, она предназначена для проверки доступности использования команд. Если вы смогли вызвать это сообщение, то вы владелец бота!')

# Сервер инфо
@client.command()
@commands.is_owner()
async def reloadprefix(ctx):
	for guild in client.guilds:
		cursor.execute("DELETE FROM prefixes WHERE id = ?", (guild.id,))
		cursor.execute("INSERT INTO prefixes (prefix, id) VALUES (?, ?)", ('?', guild.id,))
		connection.commit()
		await ctx.message.add_reaction("<a:checkon:928259275090972772>")

@client.command()
@commands.is_owner()
async def reloadprefixto(ctx):
	for guild in client.guilds:
		cursor.execute("DELETE FROM prefixes WHERE id = ?", (guild.id,))
		cursor.execute("INSERT INTO prefixes (prefix, id) VALUES (?, ?)", ('$', guild.id,))
		connection.commit()
		await ctx.message.add_reaction("<a:checkon:928259275090972772>")

@client.group(invoke_without_command=True)
async def bch(ctx):
	pass

@bch.command()
@commands.is_owner()
async def username(ctx, *, name: str):
	try:
		await client.user.edit(username=name)
		await ctx.send(f"Моё имя было изменено на: `{name}`")
	except discord.HTTPException as err:
		await ctx.send(err)

@bch.command()
@commands.is_owner()
async def nickname(ctx, *, name: str = None):
	try:
		await ctx.guild.me.edit(nick=name)
		if name:
			await ctx.send(f"Мой никнейм на этом сервере был изменён на: `{name}`")
		else:
			await ctx.send("Мой никнейм был убран.")
	except Exception as err:
			await ctx.send(err)

@bch.command()
@commands.is_owner()
async def avatar(ctx, url: str = None):
	if url is None and len(ctx.message.attachments) == 1:
		url = ctx.message.attachments[0].url
	else:
		url = url.strip("<>") if url else None

	try:
		bio = await http.get(url, res_method="read")
		await client.user.edit(avatar=bio)
		await ctx.send(f"Аватарка изменена. Ссылка:\n{url}")
	except aiohttp.InvalidURL:
		await ctx.send("Ошибка, неверная ссылка...")
	except nextcord.InvalidArgument:
		await ctx.send("Ссылка плохая :(")
	except nextcord.HTTPException as err:
		await ctx.send(err)

@client.command(aliases=['сервер'])

async def server(ctx):
	verify = ""
	if ctx.guild.verification_level == nextcord.VerificationLevel.low:
		verify = "Низкий"
	elif ctx.guild.verification_level == nextcord.VerificationLevel.medium:
		verify = "Средний"
	elif ctx.guild.verification_level == nextcord.VerificationLevel.high:
		verify = "Высокий"
	elif ctx.guild.verification_level == nextcord.VerificationLevel.highest:
		verify = "Очень высокий"
	elif ctx.guild.verification_level == nextcord.VerificationLevel.none:
		verify = "Отсутствует"

	offlinecounter = 0
	dndcounter = 0
	idlecounter = 0
	onlinecounter = 0
	invisiblecounter = 0

	textcounter = 0
	voicecounter = 0
	categorycounter = 0

	for member in ctx.guild.members:
		if member.status == nextcord.Status.online:
			onlinecounter += 1
		elif member.status == nextcord.Status.dnd:
			dndcounter += 1
		elif member.status == nextcord.Status.idle:
			idlecounter += 1
		elif member.status == nextcord.Status.offline:
			offlinecounter += 1
		elif member.status == nextcord.Status.invisible:
			invisiblecounter += 1

	for channel in ctx.guild.channels:
		if channel.type == ChannelType.text:
			textcounter += 1
		elif channel.type == ChannelType.voice:
			voicecounter += 1
		elif channel.type == ChannelType.category:
			categorycounter += 1

	owner = ctx.guild.owner
	role_count = len(ctx.guild.roles)
	if ctx.guild.icon:
		embed = nextcord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
		embed.add_field(name='Название:', value=f'`{ctx.guild.name}`', inline = False)
		embed.add_field(name='Владелец:', value=f'{owner.mention}', inline = False)
		embed.add_field(name='Участников:', value=f'`{ctx.guild.member_count}`', inline = False)
		embed.add_field(name='Уровень верификации:', value=str(verify), inline = False)
		embed.add_field(name='Высшая роль:', value=f'`{ctx.guild.roles[-2]}`', inline = False)
		embed.add_field(name='Ролей:', value=f'`{str(role_count)}`', inline = False)
		embed.add_field(name='Создан:', value=default.date(ctx.guild.created_at, ago=True), inline = False)
		embed.add_field(name='Сортировка по статусам:', value=f'<:1415online:926414278322442270> В сети: `{onlinecounter + idlecounter + dndcounter}`\n<:5251onlinestatus:926412397047070730> Онлайн: `{onlinecounter}`\n<:4572discordidle:926414279861743646> Неактивен: `{idlecounter}`\n<:5163dndstatus:926412396816388166> Не беспокоить: `{dndcounter}`\n<:2179offlinestatus:926412396589899787> Не в сети: `{offlinecounter}`', inline=False)
		embed.add_field(name='Каналов:', value=f'📜 Всего каналов: `{textcounter + voicecounter}`\n💬 Текстовых: `{textcounter}`\n🔊 Голосовых: `{voicecounter}`\n🌀 Категорий: `{categorycounter}`')
		embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		embed.set_thumbnail(url=ctx.guild.icon.url)
	else:
		embed = nextcord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
		embed.add_field(name='Название:', value=f'`{ctx.guild.name}`', inline = False)
		embed.add_field(name='Владелец:', value=f'{owner.mention}', inline = False)
		embed.add_field(name='Участников:', value=f'`{ctx.guild.member_count}`', inline = False)
		embed.add_field(name='Уровень верификации:', value=str(verify), inline = False)
		embed.add_field(name='Высшая роль:', value=f'`{ctx.guild.roles[-2]}`', inline = False)
		embed.add_field(name='Ролей:', value=f'`{str(role_count)}`', inline = False)
		embed.add_field(name='Создан:', value=default.date(ctx.guild.created_at, ago=True), inline = False)
		embed.add_field(name='Сортировка по статусам:', value=f'<:1415online:926414278322442270> В сети: `{onlinecounter + idlecounter + dndcounter}`\n<:5251onlinestatus:926412397047070730> Онлайн: `{onlinecounter}`\n<:4572discordidle:926414279861743646> Неактивен: `{idlecounter}`\n<:5163dndstatus:926412396816388166> Не беспокоить: `{dndcounter}`\n<:2179offlinestatus:926412396589899787> Не в сети: `{offlinecounter}`', inline=False)
		embed.add_field(name='Каналов:', value=f'📜 Всего каналов: `{textcounter + voicecounter}`\n💬 Текстовых: `{textcounter}`\n🔊 Голосовых: `{voicecounter}`\n🌀 Категорий: `{categorycounter}`')
		embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	await ctx.send(embed=embed)

# Музыка еее!

# Инфо о пользователе
@client.command(name="user", aliases=['юзер'])
async def user(ctx,user:nextcord.Member):
	isbot = ''
	if user.bot:
		isbot = 'Да'
	if not user.bot:
		isbot = 'Нет'

	rlist = []
	for role in user.roles:
		if role.name != "@everyone":
			if len(rlist) < 15:
				rlist.append(role.mention)

	b = ", ".join(rlist)

	if not rlist:
		embed = nextcord.Embed(color=0x2F3136, timestamp=ctx.message.created_at)
		embed.set_author(name=f"<a:checkon:928259275090972772> Информация о: - {user}"),
		embed.set_thumbnail(url=user.display_avatar),
		embed.set_footer(text=f'{ctx.author}',
			icon_url=ctx.author.display_avatar)
		embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		embed.add_field(name='ID:',value=user.id,inline=False)
		embed.add_field(name='Имя:',value=user.display_name,inline=False)
		embed.add_field(name='Аккаунт создан:',value=default.date(user.created_at, ago=True),inline=False)
		embed.add_field(name='Вошел на сервер:',value=default.date(user.joined_at, ago=True),inline=False)
		embed.add_field(name='Бот',value=isbot,inline=False)
		await ctx.send(embed=embed)
	else:
		embed = nextcord.Embed(description='Количество отображаемых ролей снижено до 15!', color=0x2F3136, timestamp=ctx.message.created_at)
		embed.set_author(name=f"<a:checkon:928259275090972772> Информация о: - {user}"),
		embed.set_thumbnail(url=user.display_avatar),
		embed.set_footer(text=f'{ctx.author}',
			icon_url=ctx.author.display_avatar)
		embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		embed.add_field(name='ID:',value=user.id,inline=False)
		embed.add_field(name='Имя:',value=user.display_name,inline=False)
		embed.add_field(name='Аккаунт создан:',value=default.date(user.created_at, ago=True),inline=False)
		embed.add_field(name='Вошел на сервер:',value=default.date(user.joined_at, ago=True),inline=False)
		embed.add_field(name='Бот',value=isbot,inline=False)
		embed.add_field(name=f'Роли: ({len(rlist)})',value=''.join([b]),inline=False)
		embed.add_field(name='Высшая роль:',value=user.top_role.mention,inline=False)
		await ctx.send(embed=embed)
	

# Аватар
@client.command(aliases=['аватар'])

async def avatar(ctx, member: nextcord.Member=None):
	await ctx.message.delete()
	if member == None:
		member = ctx.author

	icon_url = member.display_avatar
	avatarEmbed = nextcord.Embed(title = f"<a:checkon:928259275090972772> Аватарка {member.name}", color=0x2F3136)
	avatarEmbed.set_image(url = f"{icon_url}")
	avatarEmbed.timestamp = ctx.message.created_at
	avatarEmbed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	avatarEmbed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	await ctx.send(embed = avatarEmbed)
 


# Ошибки.
@client.event
async def on_command_error(ctx, error):
	dbhelp = sqlite3.connect('server.db')
	cursorhelp = dbhelp.cursor()
	cursorhelp.execute("SELECT prefix FROM prefixes WHERE id = ?", (ctx.guild.id,))
	resulthelp = cursorhelp.fetchone()
	if isinstance(error, commands.BadArgument):
		await ctx.send(f'<a:checkoff:928259276273758208> Неверный аргумент.\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`')
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'<a:checkoff:928259276273758208> Отсутствует нужный аргумент.\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>` ')
	elif isinstance(error, commands.DisabledCommand):
		await ctx.send(f'<a:checkoff:928259276273758208> Эта команда отключена.\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`')
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send(f'<a:checkoff:928259276273758208> Недостаточно прав!\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`')
	elif isinstance(error, commands.CommandOnCooldown):
		cd = round(error.retry_after)
		hours = str(cd // 3600)
		minutes = str(round(cd / 60, 1))
		em = nextcord.Embed(title=f"<a:checkoff:928259276273758208> Погодите-ка, кулдаун!",description=f"Попробуйте снова через `{hours}` часов (`{minutes}` минут)", color=0x2F3136)
		em.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		em.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		await ctx.send(embed=em)
	error1 = getattr(error, "original", error) 
	if isinstance(error1, nextcord.Forbidden):
		await ctx.send(f'<a:checkoff:928259276273758208> Кажется, у меня нет прав.\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`')
		channelerror = client.get_channel(934411732527493120)
		await channelerror.send(embed=nextcord.Embed(title='Ошибка', description=f'`{error}`\nСервер: {ctx.guild.name} | {ctx.guild.id} | {ctx.guild.owner}', color=0x2F3136))

# Помощь (new)
@client.command(aliases=['помощь'])

async def help(ctx, *, module=None):
	counter = 0
	for command in client.commands:
		counter += 1
	dbhelp = sqlite3.connect('server.db')
	cursorhelp = dbhelp.cursor()
	cursorhelp.execute("SELECT prefix FROM prefixes WHERE id = ?", (ctx.guild.id,))
	resulthelp = cursorhelp.fetchone()
	p = str(resulthelp[0])

	page1 = nextcord.Embed(title="<:4246serverdiscovery:926412396967366666> Сервер", description=f'**Страница #1**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page1.add_field(name=f'```{str(resulthelp[0])}help [помощь]```', value='```❓ Помощь по отдельной команде```', inline=True)
	page1.add_field(name=f'```{str(resulthelp[0])}lock [закрыть]```', value='```🔒 Заблокировать текущий канал```', inline=True)
	page1.add_field(name=f'```{str(resulthelp[0])}unlock [открыть]```', value='```🔓 Разблокировать текущий канал```', inline=False)
	page1.add_field(name=f'```{str(resulthelp[0])}tcreate [тсоздать]```', value='```✅ Создать текстовый канал```', inline=True)
	page1.add_field(name=f'```{str(resulthelp[0])}tremove [тудалить]```', value='```❎ Удалить текстовый канал```', inline=True)
	page1.add_field(name=f'```{str(resulthelp[0])}vcreate [всоздать]```', value='```✅ Создать голосовой канал```', inline=False)
	page1.add_field(name=f'```{str(resulthelp[0])}vremove [вудалить]```', value='```❎ Удалить голосовой канал```', inline=True)
	page1.add_field(name=f'```{str(resulthelp[0])}ccreate [ксоздать]```', value='```✅ Создать категорию```', inline=True)
	page1.add_field(name=f'```{str(resulthelp[0])}cremove [кудалить]```', value='```❎ Удалить категорию```', inline=False)
	page1.add_field(name=f'```{str(resulthelp[0])}setprefix [префикс]```', value='```⚙️ Изменить префикс бота на этом сервере```', inline=True)
	page1.add_field(name=f'```{str(resulthelp[0])}invite [пригласить]```', value='```▶️ Пригласить бота на сервер!```', inline=True)
	page1.add_field(name=f'```{str(resulthelp[0])}info [инфо]```', value='```🔨 Настройки текущего сервера```', inline=False)
	page1.add_field(name=f'```{str(resulthelp[0])}reactionrole [роли-по-реакции]```', value='```📘 Роли за реакции```', inline=False)

	page2 = nextcord.Embed(title="<:6453banhammer:926414282072154123> Модерация", description=f'**Страница #2**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page2.add_field(name=f'```{str(resulthelp[0])}clear [очистить]```', value='```🗑️ Очистка сообщений в чате```', inline=True)
	page2.add_field(name=f'```{str(resulthelp[0])}kick [кик]```', value='```🦵 Выгнать пользователя сервера```', inline=True)
	page2.add_field(name=f'```{str(resulthelp[0])}ban [бан]```', value='```🔨 Забанить пользователя сервера```', inline=False)
	page2.add_field(name=f'```{str(resulthelp[0])}unban [разбан]```', value='```⛏️ Разбанить пользователя сервера```', inline=True)
	page2.add_field(name=f'```{str(resulthelp[0])}mute [мьют]```', value='```🤐 Замутить пользователя```', inline=True)
	page2.add_field(name=f'```{str(resulthelp[0])}timeout add [таймаут добавить]```', value='```🤐 Выдать таймаут пользователю```', inline=False)
	page2.add_field(name=f'```{str(resulthelp[0])}timeout remove [таймаут убрать]```', value='```🤐 Снять таймаут пользователю```', inline=True)
	page2.add_field(name=f'```{str(resulthelp[0])}unmute [размьют]```', value='```😐 Размутить пользователя```', inline=True)
	page2.add_field(name=f'```{str(resulthelp[0])}slow [слоумод]```', value='```❄ Установить медленный режим```', inline=False)
	page2.add_field(name=f'```{str(resulthelp[0])}autorole add [авто-роль добавить]```', value='```📜 Добавить авто-роль```', inline=True)
	page2.add_field(name=f'```{str(resulthelp[0])}autorole reset [авто-роль убрать]```', value='```📜 Сбросить авто-роль```', inline=True)
	page2.add_field(name=f'```{str(resulthelp[0])}nick [ник]```', value='```📋 Сменить ник пользователя (для сброса: --reset)```', inline=False)
	page2.add_field(name=f'```{str(resulthelp[0])}automod link [авто-мод ссылка]```', value='```🤖 Бот удаляет все сообщения, которые содержат приглашения (кроме сообщений создателя)```', inline=False)

	page3 = nextcord.Embed(title="<:9656stats:926412396992540702> Утилиты", description=f'**Страница #3**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page3.add_field(name=f'```{str(resulthelp[0])}user [юзер]```', value='```📲 Информация о пользователе!```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}help [помощь]```', value='```🗒 Вызывает это меню```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}server [сервер]```', value='```📋 Информация о сервере!```', inline=False)
	page3.add_field(name=f'```{str(resulthelp[0])}avatar [аватар]```', value='```🔗 Вывести аватар пользователя.```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}embed [вложение]```', value='```📜 Создать вложение. (<название> | <описание>)```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}ping [пинг]```', value='```🏓 Скорость отклика бота```', inline=False)
	page3.add_field(name=f'```{str(resulthelp[0])}yt [ютуб]```', value='```🔎 Поиск видео с YouTube```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}wiki [вики]```', value='```🔎 Поиск статьи на Wikipedia```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}invcount [приглашения]```', value='```🔨 Узнать сколько вы пригласили пользователей на этот сервер```', inline=False)
	page3.add_field(name=f'```{str(resulthelp[0])}mcstats [мкстата]```', value='```🧊 Поиск информации о игроке (Minecraft)```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}mchistory [мкистория]```', value='```🧊 Поиск истории ников игрока (Minecraft)```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}stats [статистика]```', value='```🤖 Статистика бота```', inline=False)
	page3.add_field(name=f'```{str(resulthelp[0])}devs [разработчики]```', value='```📋 Разработчики```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}banner [баннер]```', value='```🔗 Вывести баннер сервера```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}econvert [эмоджи-конверт]```', value='```💚 Конвертировать эмоджи в картинку```', inline=False)
	page3.add_field(name=f'```{str(resulthelp[0])}report [репорт]```', value='```😠 Пожаловаться на пользователя```', inline=True)
	page3.add_field(name=f'```{str(resulthelp[0])}suggest [предложить]```', value='```✋ Отправить сообщение разработчику```', inline=True)

	page4 = nextcord.Embed(title="<a:bob:928259277414604841> Развлечения", description=f'**Страница #4**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page4.add_field(name=f'```{str(resulthelp[0])}hello [привет]```', value='```👋 Привет, бот```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}8b [шар]```', value='```🎱 Магический шар```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}rickroll [риклолл]```', value='```💃 Never Gonna Give You Up```', inline=False)
	page4.add_field(name=f'```{str(resulthelp[0])}meme [мем]```', value='```😆 Время рандомных мемов с Reddit```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}fox [лиса]```', value='```🦊 Лисички!```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}uno [уно]```', value='```🗣 Говоришь на меня - переводишь на себя.```', inline=False)
	page4.add_field(name=f'```{str(resulthelp[0])}roll [кости]```', value='```🎲 Кинуть кости```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}coin [монетка]```', value='```🪙 Подбросить монетку```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}clove [совместимость]```', value='```💌 Проверить совместимость двух пользователей```', inline=False)
	page4.add_field(name=f'```{str(resulthelp[0])}code [код]```', value='```🤖 Отправить сообщение в стиле кода Python```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}password [пароль]```', value='```✋ Генератор паролей!```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}emoji [эмоджи]```', value='```🖼️ Найти эмоджи```', inline=False)
	page4.add_field(name=f'```{str(resulthelp[0])}elist [эмоджи-список]```', value='```😘 Загрузить список эмоджи```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}esearch [эмоджи-искать]```', value='```😐 Отправить три первые эмоджи```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}esteal [украсть-эмоджи]```', value='```💚 Украсть эмоджи с сервера```', inline=False)
	page4.add_field(name=f'```{str(resulthelp[0])}emojify [эмоджифай]```', value='```💚 Конвертировать текст в эмоджи```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}gen enable [ген включить]```', value='```✋ Включить авто-генерацию сообщений```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}gen disable [ген выключить]```', value='```😛 Выключить авто-генерацию сообщений```', inline=False)
	page4.add_field(name=f'```{str(resulthelp[0])}covid [ковид]```', value='```🖼️ Статистика Covid-19```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}joke [шутка]```', value='```🖼️ Рандомная шутка```', inline=True)
	page4.add_field(name=f'```{str(resulthelp[0])}paint [полотно]```', value='```🖌️ Создать полотно для рисования```', inline=False)
	page4.add_field(name=f'```Мой говорящий Бен!```', value='```.бен <вопрос>```', inline=False)

	page5 = nextcord.Embed(title="<:8509peepohappygun:926415464303845386> Картинки", description=f'**Страница #5**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page5.add_field(name=f'```{str(resulthelp[0])}wanted [розыск]```', value='```🖼️ Постер "Живым или мёртвым"```', inline=True)
	page5.add_field(name=f'```{str(resulthelp[0])}rip [могила]```', value='```🖼️ Могила```', inline=True)
	page5.add_field(name=f'```{str(resulthelp[0])}sponge [губка]```', value='```🖼️ Рядом с Губкой```', inline=False)
	page5.add_field(name=f'```{str(resulthelp[0])}wtf [что]```', value='```🖼️ WTF?```', inline=True)
	page5.add_field(name=f'```{str(resulthelp[0])}dog [пёс]```', value='```🖼️ Собака```', inline=True)
	page5.add_field(name=f'```{str(resulthelp[0])}cat [кот]```', value='```🖼️ Кошка```', inline=False)
	page5.add_field(name=f'```{str(resulthelp[0])}duck [утка]```', value='```🖼️ Утка```', inline=True)
	page5.add_field(name=f'```{str(resulthelp[0])}fire [пожар]```', value='```🖼️ Пожар```', inline=True)

	page6 = nextcord.Embed(title="<a:pepedance:928259162503270440> Roleplay", description=f'**Страница #6**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page6.add_field(name=f'```{str(resulthelp[0])}hug [обнять]```', value='```🤗 Обнять пользователя```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}kiss [поцеловать]```', value='```😘 Поцеловать пользователя```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}ghoul [гуль]```', value='```🖤 1000-7```', inline=False)
	page6.add_field(name=f'```{str(resulthelp[0])}lewd [смутиться]```', value='```🤭 Смутиться```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}slap [ударить]```', value='```🤜 Ударить пользователя```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}lick [лизнуть]```', value='```😛 Лизнуть пользователя```', inline=False)
	page6.add_field(name=f'```{str(resulthelp[0])}pat [погладить]```', value='```✋ Погладить пользователя```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}angry [злиться]```', value='```😠 Разозлиться на пользователя```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}custom [кастом]```', value='```🤖 Создать своё действие```', inline=False)
	page6.add_field(name=f'```{str(resulthelp[0])}feed [покормить]```', value='```🍕 Покормить пользователя```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}wag [хвост]```', value='```✨ Повилять хвостом```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}scream [кричать]```', value='```😱 Закричать```', inline=False)
	page6.add_field(name=f'```{str(resulthelp[0])}drunk [напиться]```', value='```🤤 Опьянеть```', inline=True)
	page6.add_field(name=f'```{str(resulthelp[0])}dance [танцевать]```', value='```💃 Танцевать```', inline=True)

	page7 = nextcord.Embed(title="<:coinleafy:927841623667269663> Экономика", description=f'**Страница #7**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page7.add_field(name=f'```{str(resulthelp[0])}bal [баланс]```', value='```🪙 Узнать баланс пользователя```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}bag [мешок]```', value='```🪙 Ежедневный мешок с деньгами```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}shop buy [магазин купить]```', value='```🪙 Купить роль с магазина```', inline=False)
	page7.add_field(name=f'```{str(resulthelp[0])}shop add [магазин добавить]```', value='```🪙 Добавить роль в магазин```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}shop remove [магазин убрать]```', value='```🪙 Убрать роль из магазина```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}shop [магазин]```', value='```🪙 Магазин```', inline=False)
	page7.add_field(name=f'```{str(resulthelp[0])}lb cash [лб наличные]```', value='```🪙 Таблица лидеров (наличные)```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}lb bank [лб банк]```', value='```🪙 Таблица лидеров (банк)```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}lb treasury [лб казна]```', value='```🪙 Таблица лидеров (казна)```', inline=False)
	page7.add_field(name=f'```{str(resulthelp[0])}send [отправить]```', value='```🪙 Перекинуть пользователю деньги```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}rob [ограбить]```', value='```🪙 Попытаться ограбить пользователя```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}deposit [депозит]```', value='```🪙 Положить деньги на банковский счёт```', inline=False)
	page7.add_field(name=f'```{str(resulthelp[0])}withdraw [снять]```', value='```🪙 Снять деньги с банковского счёта```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}slot [слоты]```', value='```🪙 Сыграть на слот-машине```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}guess [угадать]```', value='```🪙 Сыграть в игру чисел```', inline=False)
	page7.add_field(name=f'```{str(resulthelp[0])}robbery [ограбление]```', value='```🪙 Попытаться ограбить банк```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}work [работа]```', value='```🪙 Работа```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}treasury [казна]```', value='```🪙 Казна сервера```', inline=False)
	page7.add_field(name=f'```{str(resulthelp[0])}treasury take [казна взять]```', value='```🪙 Взять деньги с казны```', inline=True)
	page7.add_field(name=f'```{str(resulthelp[0])}treasury deposit [казна положить]```', value='```🪙 Положить деньги в казну```', inline=True)

	page8 = nextcord.Embed(title="<a:tadatada:928259276823224341> Розыгрыши", description=f'**Страница #8**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page8.add_field(name=f'```{str(resulthelp[0])}giveaway start [розыгрыш создать]```', value='```🎉 Начать розыгрыш```', inline=False)
	page8.add_field(name=f'```{str(resulthelp[0])}giveaway reroll [розыгрыш перевыбрать]```', value='```🎉 Выбрать нового победителя```', inline=True)

	page9 = nextcord.Embed(title="<a:wave1:929685841280897075> Сообщения при входе", description=f'**Страница #9**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page9.add_field(name=f'```{str(resulthelp[0])}welcome hellochannel [приветствия вход-канал]```', value='```👋 Установить канал при входе```', inline=True)
	page9.add_field(name=f'```{str(resulthelp[0])}welcome byechannel [приветствия выход-канал]```', value='```👋 Установить канал при выходе```', inline=True)
	page9.add_field(name=f'```{str(resulthelp[0])}welcome message [приветствия сообщение]```', value='```👋 Установить сообщение```', inline=False)
	page9.add_field(name=f'```{str(resulthelp[0])}welcome look [приветствия просмотр]```', value='```👋 Посмотреть как будут выглядеть сообщения```', inline=True)
	page9.add_field(name=f'```{str(resulthelp[0])}welcome reset [приветствия сбросить]```', value='```👋 Отключить сообщения```', inline=True)

	page10 = nextcord.Embed(title="⬆️ Межсерверная система уровней", description=f'**Страница #10**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)\n*Предоставленные ниже функции находятся в бета-тесте!*', color=0x2F3136)
	page10.add_field(name=f'```{str(resulthelp[0])}rank [ранг]```', value='```📜 Статистика пользователя```', inline=True)
	page10.add_field(name=f'```{str(resulthelp[0])}level enable [уровни включить]```', value='```📜 Включить систему уровней```', inline=True)
	page10.add_field(name=f'```{str(resulthelp[0])}level disable [уровни выключить]```', value='```📜 Отключить систему уровней```', inline=False)
	page10.add_field(name=f'```{str(resulthelp[0])}level channel [уровни канал]```', value='```📜 Установить канал для уведомлений```', inline=True)
	page10.add_field(name=f'```{str(resulthelp[0])}level dm [уровни лс]```', value='```📜 Установить ЛС как канал для уведомлений```', inline=True)
	page10.add_field(name=f'```{str(resulthelp[0])}level leaderboard [уровни лидеры]```', value='```📜 Вывести список лидеров```', inline=False)

	page11 = nextcord.Embed(title=f"<:voice:928259275401347105> Временный голосовой канал", description=f'**Страница #11**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page11.add_field(name=f'```{str(resulthelp[0])}vc create [гк создать]```', value='```🔊 Создать временный голосовой канал```', inline=True)
	page11.add_field(name=f'```{str(resulthelp[0])}vc setlimit [гк установить-лимит]```', value='```🔊 Установить лимит для всех каналов```', inline=True)
	page11.add_field(name=f'```{str(resulthelp[0])}vc lock [гк заблокировать]```', value='```🔊 Закрыть свой канал```', inline=False)
	page11.add_field(name=f'```{str(resulthelp[0])}vc unlock [гк разблокировать]```', value='```🔊 Открыть свой канал```', inline=True)
	page11.add_field(name=f'```{str(resulthelp[0])}vc limit [гк лимит]```', value='```🔊 Установить лимит для своего канала```', inline=True)
	page11.add_field(name=f'```{str(resulthelp[0])}vc name [гк имя]```', value='```🔊 Сменить имя своего канала```', inline=False)
	page11.add_field(name=f'```{str(resulthelp[0])}vc permit [гк позволить]```', value='```🔊 Позволить пользователю подключаться к вашему каналу```', inline=True)
	page11.add_field(name=f'```{str(resulthelp[0])}vc claim [гк забрать]```', value='```🔊 Стать владельцем пустого канала```', inline=True)
	page11.add_field(name=f'```{str(resulthelp[0])}vc reject [гк запретить]```', value='```🔊 Запретить пользователю подключаться к вашему каналу```', inline=False)

	page12 = nextcord.Embed(title="📖 Тэги", description=f'**Страница #12**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)\n*Предоставленные ниже функции находятся в бета-тесте!*', color=0x2F3136)
	page12.add_field(name=f'```{str(resulthelp[0])}tag [тэг]```', value='```📖 Вызвать тэг```', inline=True)
	page12.add_field(name=f'```{str(resulthelp[0])}tag add [тэг добавить]```', value='```📖 Добавить тэг```', inline=True)
	page12.add_field(name=f'```{str(resulthelp[0])}tag remove [тэг убрать]```', value='```📖 Убрать тэг```', inline=False)
	page12.add_field(name=f'```{str(resulthelp[0])}tag list [тэг список]```', value='```📖 Вывести список тэгов```', inline=True)

	page13 = nextcord.Embed(title="<:2898picodediamante:939195860032577577> Майнкрафт", description=f'**Страница #13**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
	page13.add_field(name=f'```{str(resulthelp[0])}mine [копать]```', value='```⛏️ Пойти в шахту```', inline=True)
	page13.add_field(name=f'```{str(resulthelp[0])}furn [переплавить]```', value='```⛏️ Переплавить руду```', inline=True)
	page13.add_field(name=f'```{str(resulthelp[0])}convert [конверт]```', value='```⛏️ Конвертировать слитки в деньги```', inline=False)
	page13.add_field(name=f'```{str(resulthelp[0])}craft [крафт]```', value='```⛏️ Крафт```', inline=True)
	page13.add_field(name=f'```{str(resulthelp[0])}inventory [инвентарь]```', value='```⛏️ Инвентарь```', inline=True)
	page13.add_field(name=f'```{str(resulthelp[0])}coinsend [м-отправить]```', value='```⛏️ Отправить монеты другому пользователю```', inline=False)
	page13.add_field(name=f'```{str(resulthelp[0])}leaders [лидеры]```', value='```⛏️ Список лидеров на вашем сервере```', inline=True)
	page13.add_field(name=f'```{str(resulthelp[0])}oreshop [м-магазин]```', value='```⛏️ Вывести магазин ролей```', inline=True)
	page13.add_field(name=f'```{str(resulthelp[0])}oreshop add [м-магазин добавить]```', value='```⛏️ Добавить роль в магазин```', inline=False)
	page13.add_field(name=f'```{str(resulthelp[0])}oreshop remove [м-магазин убрать]```', value='```⛏️ Убрать роль с магазина```', inline=True)
	page13.add_field(name=f'```{str(resulthelp[0])}oreshop buy [м-магазин купить]```', value='```⛏️ Купить роль с магазина```', inline=True)

	if module == "guild":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page1)
	elif module == "mod":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page2)
	elif module == "utils":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page3)
	elif module == "fun":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page4)
	elif module == "pictures":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page5)
	elif module == "rp":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page6)
	elif module == "economic":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page7)
	elif module == "giveaway":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page8)
	elif module == "channels":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page9)
	elif module == "lvl":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page10)
	elif module == "voice":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page11)
	elif module == "tags":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page12)
	elif module == "minecraft":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page13)
	elif module == "paginator":
		client.help_pages = [page1, page2, page3, page4, page5, page6, page7, page8, page9, page10, page11, page12, page13]
		await ctx.message.delete()
		buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
		current = 0
		msg = await ctx.send(embed=client.help_pages[current])

		for button in buttons:
			await msg.add_reaction(button)

		while True:
			try:
				reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

			except asyncio.TimeoutError:
				return print("test")

			else:
				previous_page = current

			if reaction.emoji == u"\u23EA":
				current = 0

			elif reaction.emoji == u"\u2B05":
				if current > 0:
					current -= 1

			elif reaction.emoji == u"\u27A1":
				if current < len(client.help_pages)-1:
					current += 1

			elif reaction.emoji == u"\u23E9":
				current = len(client.help_pages)-1

			for button in buttons:
				await msg.remove_reaction(button, ctx.author)

			if current != previous_page:
				await msg.edit(embed=client.help_pages[current])

	elif module == "сервер":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page1)
	elif module == "майнкрафт":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page13)
	elif module == "модерация":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page2)
	elif module == "утилиты":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page3)
	elif module == "развлечения":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page4)
	elif module == "картинки":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page5)
	elif module == "рп":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page6)
	elif module == "экономика":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page7)
	elif module == "розыгрыши":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page8)
	elif module == "каналы":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page9)
	elif module == "уровни":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page10)
	elif module == "голос":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page11)
	elif module == "тэги":
		await ctx.message.delete()
		bbeb = nextcord.Embed(title="Помощь", description="Список отправлен вам в ЛС!", color=0x2F3136)
		await ctx.send(embed=bbeb)
		await ctx.author.send(embed=page12)
	elif module == "страницы":
		client.help_pages = [page1, page2, page3, page4, page5, page6, page7, page8, page9, page10, page11, page12]
		await ctx.message.delete()
		buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
		current = 0
		msg = await ctx.send(embed=client.help_pages[current])

		for button in buttons:
			await msg.add_reaction(button)

		while True:
			try:
				reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

			except asyncio.TimeoutError:
				return print("test")

			else:
				previous_page = current

			if reaction.emoji == u"\u23EA":
				current = 0

			elif reaction.emoji == u"\u2B05":
				if current > 0:
					current -= 1

			elif reaction.emoji == u"\u27A1":
				if current < len(client.help_pages)-1:
					current += 1

			elif reaction.emoji == u"\u23E9":
				current = len(client.help_pages)-1

			for button in buttons:
				await msg.remove_reaction(button, ctx.author)

			if current != previous_page:
				await msg.edit(embed=client.help_pages[current])

	elif module == None:
		await ctx.message.delete()
		p = str(resulthelp[0])
		helpemb = nextcord.Embed(title="Помощь", description=f"<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)\n[Сервер поддержки](https://discord.gg/CT8VekA57Z)\nДоступные модули:", color=0x2F3136)
		helpemb.add_field(name=f"> <:4246serverdiscovery:926412396967366666> Сервер ➲ {str(resulthelp[0])}help guild [сервер]", value=f'`{p}lock` `{p}unlock` `{p}tcreate` `{p}tremove` `{p}vcreate` `{p}vremove` `{p}ccreate` `{p}cremove` `{p}setprefix` `{p}invite` `{p}info` `{p}reactionrole`', inline=False)
		helpemb.add_field(name=f"> <:6453banhammer:926414282072154123> Модерация ➲ {p}help mod [модерация]", value=f'`{p}clear` `{p}kick` `{p}ban` `{p}unban` `{p}mute` `{p}unmute` `{p}slow` `{p}autorole` `{p}autorole add` `{p}autorole reset` `{p}nick` `{p}timeout add` `{p}timeout remove` `{p}automod link`', inline=False)
		helpemb.add_field(name=f"> <:9656stats:926412396992540702> Утилиты ➲ {p}help utils [утилиты]", value=f'`{p}user` `{p}help` `{p}server` `{p}avatar` `{p}embed` `{p}ping` `{p}yt` `{p}wiki` `{p}invcount` `{p}mcstats` `{p}mchistory` `{p}stats` `{p}devs` `{p}banner` `{p}econvert` `{p}report` `{p}suggest`', inline=False)
		helpemb.add_field(name=f"> <a:bob:928259277414604841> Развлечения ➲ {p}help fun [развлечения]", value=f'`{p}hello` `{p}8b` `{p}rickroll` `{p}meme` `{p}fox` `{p}uno` `{p}roll` `{p}coin` `{p}clove` `{p}code` `{p}password` `{p}emoji` `{p}elist` `{p}esearch` `{p}esteal` `{p}emojify` `{p}gen enable` `{p}gen disable` `{p}joke` `{p}covid` `{p}paint`', inline=False)
		helpemb.add_field(name=f"> <:8509peepohappygun:926415464303845386> Картинки ➲ {p}help pictures [картинки]", value=f'`{p}wanted` `{p}rip` `{p}sponge` `{p}wtf` `{p}dog` `{p}cat` `{p}duck` `{p}fire`', inline=False)
		helpemb.add_field(name=f"> <a:pepedance:928259162503270440> Roleplay ➲ {p}help rp [рп]", value=f'`{p}hug` `{p}kiss` `{p}ghoul` `{p}lewd` `{p}slap` `{p}lick` `{p}pat` `{p}angry` `{p}custom` `{p}feed` `{p}wag` `{p}dance` `{p}scream` `{p}drunk`', inline=False)
		helpemb.add_field(name=f"> <:coinleafy:927841623667269663> Экономика ➲ {p}help economic [экономика]", value=f'`{p}bal` `{p}bag` `{p}shop add` `{p}shop remove` `{p}shop buy` `{p}shop` `{p}lb cash` `{p}lb bank` `{p}lb treasury` `{p}send` `{p}rob` `{p}deposit` `{p}withdraw` `{p}slot` `{p}guess` `{p}robbery` `{p}work` `{p}treasury` `{p}treasury take` `{p}treasury deposit`', inline=False)
		helpemb.add_field(name=f"> <a:tadatada:928259276823224341> Розыгрыши ➲ {p}help giveaway [розыгрыши]", value=f'`{p}giveaway start` `{p}giveaway reroll`', inline=False)
		helpemb.add_field(name=f"> <a:wave1:929685841280897075> Приветственные каналы ➲ {p}help channels [каналы]", value=f'`{p}welcome hellochannel` `{p}welcome byechannel` `{p}welcome message` `{p}welcome look` `{p}welcome reset`', inline=False)
		helpemb.add_field(name=f"> ⬆️ Система уровней ➲ {p}help lvl [уровни]", value=f'`{p}rank` `{p}level enable` `{p}level disable` `{p}level channel` `{p}level dm` `{p}level leaderboard`', inline=False)
		helpemb.add_field(name=f"> <:voice:928259275401347105> Временные голосовые каналы ➲ {p}help voice [голос]", value=f'`{p}vc create` `{p}vc setlimit` `{p}vc lock` `{p}vc unlock` `{p}vc limit` `{p}vc name` `{p}vc permit` `{p}vc claim` `{p}vc reject`', inline=False)
		helpemb.add_field(name=f"> 🔞 NSFW ➲ Нет страницы", value=f'`{p}hentai` `{p}porn` `{p}cock` `{p}boobs` `{p}ass` `{p}doggystyle` `{p}blowjob` `{p}pussy`', inline=False)
		helpemb.add_field(name=f"> 📖 Тэги ➲ {p}help tags [тэги]", value=f'`{p}tag` `{p}tag add` `{p}tag remove` `{p}tag list`', inline=False)
		helpemb.add_field(name=f"> <:2898picodediamante:939195860032577577> Майнкрафт ➲ {p}help minecraft [майнкрафт]", value=f'`{p}mine` `{p}furn` `{p}convert` `{p}craft` `{p}inventory` `{p}coinsend` `{p}leaders` `{p}oreshop` `{p}oreshop add` `{p}oreshop remove` `{p}oreshop buy`', inline=False)
		helpemb.add_field(name=f"> 📜 Стандартное меню ➲ {p}help paginator [страницы]", value=f'`{p}help paginator`', inline=False)
		helpemb.add_field(name=f"> :question: BETA ➲ Нет страницы", value=f'`Пока что ничего не находится в бета-тесте!`', inline=False)
		helpemb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		helpemb.set_footer(text=f"Всего команд: {counter} • Вместе со скрытыми!", icon_url=ctx.author.display_avatar)
		view = HelpCommandView()
		await ctx.send(embed=helpemb, view=view)
	elif module == 'help':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}help | Вызывает меню помощи'))
	elif module == 'avatar':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}avatar (пользователь) | Присылает аватарку пользователя'))
	elif module == 'ban':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}ban <пользователь> (причина) | Банит пользователя на сервере'))
	elif module == 'cat':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}cat (пользователь) | Прикрепляет аватарку пользователя на фотографию кошки'))
	elif module == 'lock':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}lock | Закрывает текущий канал'))
	elif module == 'unlock':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}unlock | Открывает текущий канал'))
	elif module == 'nick':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}nick <пользователь> <ник> | Меняет ник пользователя (используйте --reset чтобы сбросить ник)'))
	elif module == 'tcreate':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}tcreate <название> | Создает текстовый канал'))
	elif module == 'tremove':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}tremove <название> | Удаляет текстовый канал'))
	elif module == 'vcreate':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}vcreate <название> | Создает голосовой канал'))
	elif module == 'vremove':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}vremove <название> | Удаляет голосовой канал'))
	elif module == 'ccreate':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}ccreate <название> | Создает категорию'))
	elif module == 'cremove':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}cremove <название> | Удаляет категорию'))
	elif module == 'setprefix':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}setprefix <префикс> | Устанавливает ваш префикс на данном сервере'))
	elif module == 'invite':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}invite | Ссылка чтобы пригласить бота на сервер'))
	elif module == 'help':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}help <команда> | Отдельная помощь по команде'))
	elif module == 'kick':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}kick <пользователь> (причина) | Выгоняет пользователя с сервера'))
	elif module == 'mute':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}mute <пользователь> (причина) | Мутит пользователя на сервере'))
	elif module == 'unban':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}unban <пользователь> | Разбанивает пользователя на сервере'))
	elif module == 'unmute':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}unmute <пользователь> | Размучивает пользователя на сервере'))
	elif module == 'slow':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}slow <секунд> | Устанавливает медленный режим'))
	elif module == 'user':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}user <пользователь> | Выводит информацию о пользователе'))
	elif module == 'embed':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}embed (название) | (описание) | Создает вложение'))
	elif module == 'server':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}server | Выводит информацию о текущем сервере'))
	elif module == 'ping':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}ping | Выводит скорость отклика бота'))
	elif module == 'yt':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}yt <текст> | Поиск видео на YouTube'))
	elif module == 'hello':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}hello | Бот поприветствует вас'))
	elif module == '8b':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}8b <вопрос> | Магический шар ответит на ваш вопрос (да или нет)'))
	elif module == 'rickroll':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}rickroll | Рик Эстли станцует для вас'))
	elif module == 'meme':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}meme | Присылает рандомный мем с Reddit'))
	elif module == 'fox':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}fox | Присылает рандомное фото лисы'))
	elif module == 'uno':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}uno | Присылает реверсивную карту с Uno'))
	elif module == 'hentai':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}hentai | ( ͡° ͜ʖ ͡°)'))
	elif module == 'wanted':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}wanted (пользователь) | Прикрепляет аватарку пользователя на постер о преступнике'))
	elif module == 'rip':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}rip (пользователь) | Прикрепляет аватарку пользователя на фотографию могилы'))
	elif module == 'fire':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}fire (пользователь) | Прикрепляет аватарку пользователя на фотографию кошки'))
	elif module == 'duck':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}duck (пользователь) | Прикрепляет аватарку пользователя на фотографию утки'))
	elif module == 'dog':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}dog (пользователь) | Прикрепляет аватарку пользователя на фотографию собаки'))
	elif module == 'sponge':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}sponge (пользователь) | Прикрепляет аватарку пользователя на фотографию Губки Боба'))
	elif module == 'hug':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}hug <пользователь> (комментарий) | Обнять пользователя'))
	elif module == 'kiss':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}kiss <пользователь> (комментарий) | Поцеловать пользователя'))
	elif module == 'ghoul':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}ghoul (комментарий) | Отбросить чувства'))
	elif module == 'lewd':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}lewd (комментарий) | Магический шар ответит на ваш вопрос (да или нет)'))
	elif module == 'lick':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}lick <пользователь> (комментарий) | Лизнуть пользователя'))
	elif module == 'pat':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}pat <пользователь> (комментарий) | Погладить пользователя'))
	elif module == 'slap':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}slap <пользователь> (комментарий) | Ударить пользователя'))
	elif module == 'clear':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}clear (количество) | Удаляет заданное кол-во сообщений (если не указывать ничего, удалится 100 сообщений)'))
	elif module == 'reactrole':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}reactrole <эмоджи> <@роль> <сообщение> | Роли по реакции'))
	elif module == 'poll':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}poll <сообщение> | Создаёт опрос'))
	elif module == 'roll':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}roll | Кидает кости'))
	elif module == 'coin':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}coin <орёл / решка> | Подбрасывает монетку!'))
	elif module == 'clove':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}clove <пользователь> <пользователь> | Проверка совместимости'))
	elif module == 'bag':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}bag | Ежедневный мешок денег'))
	elif module == 'bal':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}bal (пользователь) | Узнать баланс пользователя'))
	elif module == 'shop add':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}shop add <роль> <цена> | Добавить роль в магазин ролей'))
	elif module == 'shop remove':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}shop remove <роль> | Убрать роль с магазина ролей'))
	elif module == 'shop':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}shop | Вывести магазин ролей'))
	elif module == 'lb cash':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}lb cash | Вывести таблицу лидеров (по наличным)'))
	elif module == 'lb bank':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}lb bank | Вывести таблицу лидеров (по деньгам в банке)'))
	elif module == 'send':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}send <пользователь> <сумма> | Отправить деньги пользователю'))
	elif module == 'rob':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}rob <пользователь> | Попытаться ограбить пользователя'))
	elif module == 'deposit':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}deposit <сумма> | Положить деньги на банковский счёт'))
	elif module == 'withdraw':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}withdraw <сумма> | Снять деньги с банковского счёта'))
	elif module == 'slot':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}slot | Сыграть в игру "Слоты"'))
	elif module == 'guess':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}guess | Сыграть в игру чисел'))
	elif module == 'robbery':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}robbery | Попытаться ограбить банк'))
	elif module == 'work':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}work | Пойти на работу'))
	elif module == 'shop buy':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}shop buy <роль> | Купить роль с магазина'))
	elif module == 'treasury':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}treasury | Казна сервера'))
	elif module == 'treasury take':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}treasury take <сумма> | Взять деньги с казны'))
	elif module == 'treasury deposit':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}treasury deposit <сумма> | Положить деньги в казну'))
	elif module == 'wiki':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}wiki <текст> | Поискать статью на Wikipedia'))
	elif module == 'mcstats':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}mcstats <имя> | Поискать информацию об игроке Minecraft'))
	elif module == 'mchistory':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}mchistory <имя> | Поискать историю имён игрока Minecraft'))
	elif module == 'code':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}code <текст> | Отправить сообщение в стиле кода Python'))
	elif module == 'password':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}password <числосимволов> | Сгенерировать надёжный пароль'))
	elif module == 'giveaway start':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}giveaway start | Начать розыгрыш'))
	elif module == 'giveaway reroll':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}giveaway reroll <канал> <айди> | Выбрать нового победителя'))
	elif module == 'emoji':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}emoji <текст> | Ищет эмоджи по вашему запросу'))
	elif module == 'elist':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}elist <текст> | Отправляет список эмоджи по вашему запросу'))
	elif module == 'esearch':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}esearch <текст> | Отправляет первые три эмоджи по вашему запросу'))
	elif module == 'invcount':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}invcount (пользователь) | Узнать сколько пользователей вы пригласили на этот сервер'))
	elif module == 'esteal':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}esteal <ссылка> <название> | Добавить эмоджи по ссылке'))
	elif module == 'rank':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}rank (пользователь) | Вывести статистику пользователя'))
	elif module == 'gen enable':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}gen enable | Включить авто-генерацию сообщений'))
	elif module == 'gen disable':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}gen disable | Выключить авто-генерацию сообщений'))
	elif module == 'welcome hellochannel':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}welcome hellochannel <#канал> | Установить канал приветствий'))
	elif module == 'welcome byechannel':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}welcome byechannel <#канал> | Установить канал прощаний'))
	elif module == 'welcome message':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}welcome message <текст> | Сменить текст сообщения'))
	elif module == 'welcome look':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}welcome look | Посмотреть как будут выглядеть сообщения'))
	elif module == 'welcome reset':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}welcome reset | Отключить сообщения при входе и выходе'))
	elif module == 'emojify':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}emojify <текст> | Конвертировать текст в эмоджи'))
	elif module == 'autorole add':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}autorole add <роль> | Добавить авто-роль при входе.'))
	elif module == 'autorole reset':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}autorole reset | Сбросить авто-роль.'))
	elif module == 'level enable':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}level enable | Включить систему уровней на текущем сервере.'))
	elif module == 'level disable':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}level disable | Выключить систему уровней на текущем сервере.'))
	elif module == 'level channel':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}level channel <канал> | Установить канал для уведомлений про повышение уровня.'))
	elif module == 'level dm':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}level dm | Установить личные сообщения как канал для уведомлений про повышение уровня.'))
	elif module == 'info':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}info | Настройки текущего сервера.'))
	elif module == 'joke':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}joke | Случайная шутка.'))
	elif module == 'timeout add':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}timeout add <@пользователь> <время (например: 10m - 10 минут)> (причина) | Выдать таймаут пользователю (формат: s, m, h, d - секунды, минуты, часы, дни)'))
	elif module == 'timeout remove':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}timeout remove <@пользователь> | Снять таймаут пользователю'))
	elif module == 'covid':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}covid <страна> | Статистика Covid-19 (пример: {p}covid Ukraine)'))
	elif module == 'econvert':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}econvert <эмоджи> | Конвертирует эмоджи в картинку'))
	elif module == 'report':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}report <пользователь> <причина> | Пожаловаться на пользователя'))
	elif module == 'warn':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}warn <пользователь> <причина> | Выдать пред пользователю'))
	elif module == 'unwarn':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}unwarn <пользователь> <номер> | Снять пред пользователю'))
	elif module == 'warns':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}warns <пользователь> | Вывести список предупреждений пользователя'))
	elif module == 'warnlimit':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}warnlimit <2-15> | Установить лимит предов'))
	elif module == 'warnpunishment':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}warnpunishment <0-2> | Установить наказание при достижении лимита\n`0 - Таймаут (2 часа)`\n`1 - Бан`\n`2 - Кик`'))
	elif module == 'suggest':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}suggest <текст> | Отправить сообщение разработчику'))
	elif module == 'tag':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}tag <название> | Вывести тэг'))
	elif module == 'tag add':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}tag add <команда> <название> <контент> | Добавить тэг'))
	elif module == 'tag remove':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}tag remove <название> | Убрать тэг'))
	elif module == 'tag list':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}tag list | Вывести список тэгов'))
	elif module == 'automod link':
		await ctx.send(embed=nextcord.Embed(description=f'Использование: {p}automod link | Вкл/выкл блокировку приглашений на сервере!'))
	else:
		p = str(resulthelp[0])
		await ctx.send(embed=nextcord.Embed(title='Ошибка', description=f'{ctx.author.mention}, Вы неверно указали **модуль** или **команду**.\n`Для просмотра списка модулей и команд, напишите` **{p}help**\n\n*Если команда есть, но помощи по ней нет, обратитесь к mqchinee#1422 ({p}devs)*'))


# Розыгрыши
@client.command(aliases=['инфо'])
async def info(ctx):
	dbhelp = sqlite3.connect('server.db')
	cursorhelp = dbhelp.cursor()
	cursorhelp.execute("SELECT prefix FROM prefixes WHERE id = ?", (ctx.guild.id,))
	resulthelp = cursorhelp.fetchone()
	db1 = sqlite3.connect("levellog.db")
	cursor1 = db1.cursor()
	cursor1.execute("SELECT channel_log FROM log WHERE guild_log = ?", (ctx.guild.id,))
	result1 = cursor1.fetchone()

	db3 = sqlite3.connect('welcome.db')
	cursor3 = db3.cursor()
	cursor3.execute(f"SELECT channel_id_h FROM welcome WHERE guild_id = {ctx.guild.id}")
	result3 =  cursor3.fetchone()
	db4 = sqlite3.connect('welcome.db')
	cursor4 = db4.cursor()
	cursor4.execute(f"SELECT channel_id_b FROM welcome WHERE guild_id = {ctx.guild.id}")
	result4 =  cursor4.fetchone()
	leveldb = sqlite3.connect("levellog.db")
	lvlcursor = leveldb.cursor()
	lvlcursor.execute("SELECT disabled_id FROM disable WHERE disabled_id = ?", (ctx.guild.id,))
	lvlresult = lvlcursor.fetchone()
	db5 = sqlite3.connect('generator.db')
	cursor5 = db5.cursor()
	cursor5.execute("SELECT id FROM enabled WHERE id = ?", (ctx.guild.id,))
	data5 = cursor5.fetchone()

	p = str(resulthelp[0])
	await ctx.message.delete()
	embed = nextcord.Embed(title="Бот на этом сервере", description=f'**{p}help** | Меню помощи\n**{p}invite** | Пригласить меня\n**Сайт** | [Жми сюда](https://www.leafy.cf)\n[Сервер поддержки](https://discord.gg/CT8VekA57Z)', color=0x2F3136)
	embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	embed.set_footer(text=ctx.guild.name, icon_url=ctx.author.display_avatar)
	if lvlresult:
		embed.add_field(name="Главное", value=f'<:1415online:926414278322442270> Префикс на этом сервере: **{p}**\n<:1415online:926414278322442270> Язык: **ru-RU**\n<:1415online:926414278322442270> Система уровней: **Отключена**', inline=False)
	if not lvlresult:
		embed.add_field(name="Главное", value=f'<:1415online:926414278322442270> Префикс на этом сервере: **{p}**\n<:1415online:926414278322442270> Язык: **ru-RU**\n<:1415online:926414278322442270> Система уровней: **Включена**', inline=False)
	if result1:
		embed.add_field(name="Система уровней", value=f"<:1415online:926414278322442270> Канал для уведомлений: <#{str(result1[0])}>", inline=False)
	if not result1:
		embed.add_field(name="Система уровней", value=f"<:1415online:926414278322442270> Канал для уведомлений: `Личные сообщения`", inline=False)
	if result3:
		embed.add_field(name='Канал при входе', value=f"<:1415online:926414278322442270> Канал уведомлений при входе: <#{str(result3[0])}>", inline=False)
	if not result3:
		embed.add_field(name='Канал при входе', value=f"<:1415online:926414278322442270> Канал уведомлений при входе **не установлен**.", inline=False)
	if result4:
		embed.add_field(name='Канал при выходе', value=f"<:1415online:926414278322442270> Канал уведомлений при выходе: <#{str(result4[0])}>", inline=False)
	if not result4:
		embed.add_field(name='Канал при выходе', value=f"<:1415online:926414278322442270> Канал уведомлений при выходе **не установлен**.", inline=False)
	if data5:
		embed.add_field(name='Авто-генерация сообщений при ответе', value=f"<:1415online:926414278322442270> Авто-генерация сообщений: **Включена**", inline=False)
	if not data5:
		embed.add_field(name='Авто-генерация сообщений при ответе', value=f"<:1415online:926414278322442270> Авто-генерация сообщений: **Отключена**", inline=False)
	await ctx.send(embed=embed)

# Шар
@client.command(aliases=['8b', 'шар'])

async def eightball(ctx, *, question):
	await ctx.channel.purge(limit=1)
	responses = [":white_check_mark: Я вижу... да!",
	":negative_squared_cross_mark: Я вижу... нет!",
	":question: Лучше не говорить сейчас об этом.",
	":negative_squared_cross_mark: Мой ответ - нет.",
	":question: Не могу сейчас предсказать..",
	":question: Не зацикливайся на этом.",
	":question: Попробуй снова!",
	":negative_squared_cross_mark: Мои источники говорят нет!",
	":white_check_mark: Конечно!",
	":white_check_mark: Вероятнее всего - да!",
	":white_check_mark: Да.",
	":white_check_mark: Моё мнение - да!",
	":negative_squared_cross_mark: Скорее всего - нет.",
	":negative_squared_cross_mark: Даже не думай!"]
	emb = nextcord.Embed(title='Магический шар!', timestamp=ctx.message.created_at, color=0x2F3136)
	emb.add_field(name='Вопрос:', value=f'{question}', inline=False)
	emb.add_field(name='Ответ:', value=f'{random.choice(responses)}')
	emb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	await ctx.send(embed=emb)

# Embed
@client.command(aliases=['вложение'])

async def embed(ctx, *, content: str):
	await ctx.channel.purge(limit=1)
	title, description = content.split('|')
	embed = nextcord.Embed(title=title, description=description, color=0x2F3136, timestamp=ctx.message.created_at)
	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	await ctx.send(embed=embed)

# Fun
@client.command(aliases=['рикролл'])

async def rickroll(ctx):
	embed=nextcord.Embed(title="Ты зарикроллен!", url="", description="**Рик Эстли станцует для тебя!**", color=0x2F3136)
	embed.set_image(url="https://c.tenor.com/u9XnPveDa9AAAAAM/rick-rickroll.gif")
	await ctx.reply(embed=embed)

@client.command(pass_context=True, aliases=['мем'])

async def meme(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=['лиса'])

async def fox(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/foxes/new.json?sort=foxes') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

# NSFW
@client.command(pass_context=True, aliases=['хентай'])
@commands.is_nsfw()

async def hentai(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/hentai/new.json?sort=hentai') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@hentai.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')

@client.command(pass_context=True, aliases=['грудь'])
@commands.is_nsfw()

async def boobs(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/boobs/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@boobs.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')

@client.command(pass_context=True, aliases=['задница'])
@commands.is_nsfw()

async def ass(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/ass/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@ass.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')

@client.command(pass_context=True, aliases=['анал'])
@commands.is_nsfw()

async def anal(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/anal/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@anal.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')

@client.command(pass_context=True, aliases=['член'])
@commands.is_nsfw()

async def cock(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/cock/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@cock.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')

@client.command(pass_context=True, aliases=['порно'])
@commands.is_nsfw()

async def porn(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@porn.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')

@client.command(pass_context=True)
@commands.is_nsfw()

async def blowjob(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/blowjobs/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@blowjob.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')

@client.command(pass_context=True)
@commands.is_nsfw()

async def doggystyle(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/Doggystyle_NSFW/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@doggystyle.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')

@client.command(pass_context=True, aliases=['вагина'])
@commands.is_nsfw()

async def pussy(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/pussy/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@pussy.error
async def error(ctx, error):
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду можно использовать только в NSFW-каналах!')



# Ютуб
@client.command(aliases=['ютуб'])

async def yt(msg, *, search):
	query_string = urllib.parse.urlencode({
		"search_query": search
	})
	html_content = urllib.request.urlopen(
		"http://www.youtube.com/results?" + query_string
	)
	search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
	await msg.send("http://www.youtube.com/watch?v=" + search_results[0])

# Say
@client.command()
@commands.is_owner()
async def say(ctx, *, arg):
	await ctx.message.delete()
	await ctx.send(arg)

# Инвайт
@client.command(aliases=['пригласить'])

async def invite(ctx):
	await ctx.message.delete()
	emb = nextcord.Embed(title='<a:checkon:928259275090972772> Пригласить меня на сервер!', description=f'[Приглашение с правами админинстратора](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=applications.commands%20bot)\n[Рекомендованное приглашение](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=1644972474359&scope=bot%20applications.commands)', color=0x2F3136, timestamp=ctx.message.created_at)
	emb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	emb.set_thumbnail(url=client.user.display_avatar)
	await ctx.send(embed=emb)


@client.command(aliases=['предложить'])
@commands.cooldown(1, 3600, commands.BucketType.user)
async def suggest(ctx, *, arg):
	await ctx.message.delete()
	user = await client.fetch_channel(935588621724041276)
	emb = nextcord.Embed(title='Новое сообщение', description=f'{ctx.message.author} написал вам:', timestamp=ctx.message.created_at, color=0x2F3136)
	emb.add_field(name='Сообщение:', value=arg, inline = False)
	emb.add_field(name='Сервер:', value=f'`{ctx.guild.name}` | `{ctx.guild.id}` | {ctx.guild.owner.mention}', inline=False)
	emb.set_thumbnail(url=ctx.author.display_avatar)
	await user.send(embed=emb)
	await ctx.send(embed=nextcord.Embed(title='Сообщение разработчику!', description=f'{ctx.message.author.mention}, ваше сообщение было доставлено!\n Сообщение: {arg}', color=0x2F3136))

# DM
@client.command()
@commands.is_owner()
async def dm(ctx, arg, *, text):
	await ctx.message.delete()
	user = await client.fetch_user(f"{arg}")
	emb = nextcord.Embed(title='<a:checkon:928259275090972772> Вы получили сообщение от разработчика!', description='Мой разработчик отправил вам сообщение!', timestamp=ctx.message.created_at, color=0x2F3136)
	emb.add_field(name='<a:checkon:928259275090972772> Сообщение:', value=f'{text}')
	await user.send(embed=emb)
	await ctx.send(f'<a:checkon:928259275090972772> Вы ответили пользователю {arg}\nСообщение: {text}')

# Дев-меню
@client.command()
@commands.is_owner()
async def devmenu(ctx):
	dbhelp = sqlite3.connect('server.db')
	cursorhelp = dbhelp.cursor()
	cursorhelp.execute("SELECT prefix FROM prefixes WHERE id = ?", (ctx.guild.id,))
	resulthelp = cursorhelp.fetchone()
	p = str(resulthelp[0])
	await ctx.message.delete()
	emb = nextcord.Embed(title='Меню разработчика', description=f'*Команды ниже доступны только разработчику*\n`{p}dev` `{p}dm` `{p}say` `{p}toggle` `{p}kitty` `{p}strs` `{p}broadcast` `{p}inmessage` `{p}go` `{p}inv` `{p}cp` `{p}award` `{p}take` `{p}set` `{p}gsset` `{p}repset` `{p}load` `{p}unload` `{p}reload` `{p}coglist` `{p}leave` `{p}guilds` `{p}discriminator` `{p}bch nickname`  `{p}bch username`  `{p}bch avatar` `{p}reloadprefix` `{p}reloadprefixto` `{p}gh` `{p}evl` `{p}evlt` `{p}devb` `{p}deva` `{p}devk` `{p}devd` `{p}gaward` `{p}reboot` `{p}topguilds` `{p}cg`', color=0x2F3136, timestamp=ctx.message.created_at)
	emb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	emb.set_footer(text='Всего команд: 36', icon_url=ctx.author.display_avatar)
	await ctx.send(embed=emb)

# toggle
@client.command()
@commands.is_owner()
async def toggle(ctx, *, command):
	command=client.get_command(command)
	if command == None:
		await ctx.send('<a:checkoff:928259276273758208> Команда не найдена')
	elif ctx.command == command:
		await ctx.send('<a:checkoff:928259276273758208> Вы не можете отключить данную команду')
	else:
		command.enabled = not command.enabled
		ternary = "включена" if command.enabled else "выключена"
		await ctx.send(f'Команда {command.qualified_name} была {ternary}')

@client.command()

async def lol(ctx):
	await ctx.send('lul')

# stats
@tasks.loop(seconds=10.0)
async def uptimeCounter():
	global ts, tm, th, td
	ts += 10
	if ts == 60:
		ts = 0
		tm += 1
		if tm == 60:
			tm = 0
			th += 1
			if th == 24:
				th = 0
				td += 1

@uptimeCounter.before_loop
async def beforeUptimeCounter():
	await client.wait_until_ready()

@client.command(aliases=['разработчики'])
async def devs(ctx):
	view = DevelopersCommandView()
	await ctx.message.delete()
	embed=nextcord.Embed(title='Разработчики',  description='Мы разрабатываем Leafy!\n[Сервер поддержки](https://discord.gg/CT8VekA57Z)', color=0x2F3136)
	embed.add_field(name='#1 | mqchinee#1422', value='Статус: `Создатель`\nКомментарий: `Надеюсь, вам нравится Лифи!`')
	embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/748494305005535253/9f9d0a5927b00f4916c0e6f6b1456779.png?size=1024')
	await ctx.send(f"{ctx.author.mention}", embed=embed, view=view)

@client.command(aliases=['статистика'])
async def stats(ctx):
	global ts, tm, th, td
	shard_id = ctx.guild.shard_id
	shard = client.get_shard(shard_id)
	shard_name = str(shard_id)
	shard_servers = len([guild for guild in client.guilds if guild.shard_id == shard_id])
	embed = nextcord.Embed(title='Моя статистика:', timestamp=ctx.message.created_at, color=0x2F3136)
	embed.add_field(name='Аптайм:', value = f"Дней: `{td}`\nЧасов: `{th}`\nМинут: `{tm}`\nСекунд: `{ts}`", inline=False)
	embed.add_field(name='Пинг:', value=f"`{round(client.latency*1000)}мс`", inline=False)
	embed.add_field(name='Нагрузка ЦПУ:', value=f'`{psutil.cpu_percent()}%`', inline=False)
	embed.add_field(name='Нагрузка ОЗУ:', value=f'`{psutil.virtual_memory()[2]}%`', inline=False)
	embed.add_field(name='Версии:', value=f'Версия бота: `v3.7.3`\nВерсия Python: `{platform.python_version()}`\nВерсия Nextcord: `{str(nextcord.__version__)}`\nПлатформа: `{platform.platform(aliased=True, terse=True)} {platform.machine()} ({platform.processor()})`', inline=False)
	embed.add_field(name='Серверов:', value=f'`{len(client.guilds)}`', inline=False)
	embed.add_field(name='Пользователей:', value=f'`{len(set(client.get_all_members()))}`', inline=False)
	embed.add_field(name='Каналов:', value=f'`{len(set(client.get_all_channels()))}`', inline=False)
	embed.add_field(name='Шард на вашем сервере:', value=f'Номер: `#{shard_name}`\nПинг: `{round(shard.latency*1000)} мс`\nСерверов на этом шарде: `{shard_servers}`', inline=False)
	embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	embed.set_thumbnail(url=client.user.display_avatar)
	await ctx.send(embed=embed)

# devmenu ошибки
@devmenu.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@toggle.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@say.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@dm.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@dev.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@reloadprefix.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

# Слоумод
@client.command(aliases=['слоумод'])

@commands.has_permissions(ban_members=True)
async def slow(ctx, time: int):
	if (not ctx.author.guild_permissions.manage_channels):
		await ctx.send('<a:checkoff:928259276273758208> Недостаточно прав!')
		return
	try:
		if time == 0:
			await ctx.send('<a:checkon:928259275090972772> Медленный режим выключен!')
			await ctx.channel.edit(slowmode_delay=0)
		elif time > 21600:
			await ctx.send('<a:checkoff:928259276273758208> Вы не можете устанавливать время больше 6-ти часов!')
			return
		else:
			await ctx.channel.edit(slowmode_delay=time)
			await ctx.send(f'<a:checkon:928259275090972772> Вы установили медленный режим на {time} секунд!')
	except Exception:
		await print('Упс!')

# esteal
@client.command(aliases=['украсть-эмоджи'])

@commands.cooldown(1, 5, commands.BucketType.guild)
@commands.has_permissions(ban_members=True)
async def esteal(ctx, url:str, *, name):
	guild = ctx.guild
	async with aiohttp.ClientSession() as ses:
		async with ses.get(url) as r:
			try:
				imgOrGif = BytesIO(await r.read())
				bValue = imgOrGif.getvalue()
				if r.status in range(200, 299):
					emoji = await guild.create_custom_emoji(image=bValue, name=name)
					await ctx.send('<a:checkon:928259275090972772> Эмоджи добавлено!')
					await ses.close()
				else:
					await ctx.send(f'({r.status}) Ошибка что-ли ._.')
			except nextcord.HTTPExeption:
				await ctx.send('Короче ты нуб, ничего не работает')

# Ник
@client.command(pass_context=True, aliases=['ник'])

@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: nextcord.Member, *, nickname):
	if nickname == '--reset':
		await member.edit(nick=None)
		await ctx.message.delete()
		emb = nextcord.Embed(title='Сброс ника!', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Сбросил ник:', value=ctx.author.mention, inline=False)
		emb.add_field(name='<a:checkon:928259275090972772> Кому сбросили:', value=member.mention, inline=False)
		emb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		await ctx.send(embed=emb)
	else:
		await ctx.message.delete()
		await member.edit(nick=nickname)
		emb = nextcord.Embed(title='Смена ника!', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Изменил ник:', value=ctx.author.mention, inline=False)
		emb.add_field(name='<a:checkon:928259275090972772> Кому изменили:', value=member.mention, inline=False)
		emb.add_field(name='<a:checkon:928259275090972772> Ник:', value=nickname, inline=False)
		emb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		await ctx.send(embed=emb)

# Cat
@client.command(pass_context=True)
@commands.is_owner()
async def kitty(ctx):
	embed = nextcord.Embed(title="", description="", color=0x2F3136)
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/cats/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@kitty.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Котики только разработчику!')

# Сервера
@client.command(pass_context=True)
@commands.is_owner()
async def strs(ctx):
	gguild = client.guilds
	em = nextcord.Embed(title='Информация о серверах', description=str(client.guilds), timestamp=ctx.message.created_at, color=0x2F3136)
	em.add_field(name='Кол-во', value=f'{str(len(client.guilds))}')
	await ctx.send(embed=em)

@strs.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

# Опрос
@client.command(aliases=['опрос'])

@commands.has_permissions(manage_nicknames=True)
async def poll(ctx,*,message):
	await ctx.message.delete()
	emb=nextcord.Embed(title="Опрос!", description=f"{message}", color=0x2F3136, timestamp=ctx.message.created_at)
	emb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	msg=await ctx.channel.send(embed=emb)
	await msg.add_reaction('👍')
	await msg.add_reaction('👎')

@client.command(pass_context=True)
@commands.is_owner()
async def broadcast(ctx, *, msg):
	await ctx.send(f'Сообщение: `{msg}`\n<a:checkon:928259275090972772> Отправлено!')
	for server in client.guilds:
		for channel in server.text_channels:
			try:
				await channel.send(msg)
			except Exception:
				continue
			else:
				break

@broadcast.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@client.command(aliases=['кости'])

async def roll(ctx):
	await ctx.message.delete()
	await ctx.send(f':game_die: {ctx.author.mention} бросил кости!\n:game_die: Выпало: **{random.randint(1,6)}**')

@client.command(aliases=['совместимость'])

async def clove(ctx, m1: nextcord.Member, m2: nextcord.Member):
	await ctx.message.delete()
	embed = nextcord.Embed(title='❤️ Совместимость!', description=f'💝 {m1.mention} и {m2.mention} совместимы на {random.randint(0,100)}%', colour=nextcord.Colour.red(), timestamp = ctx.message.created_at, color=0x2F3136)
	embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	await ctx.send(embed=embed) #await ctx.send(f'{ctx.author.mention},f Использование: {p}?coin орёл | решка')

@client.command(aliases=['монетка'])

async def coin(ctx, arg):
	resp = ['выпал орёл!', 'выпала решка!'] 
	if arg == 'орёл':
		await ctx.send(f'{ctx.author.mention}, подбрасываю монетку.')
		await asyncio.sleep(3)
		await ctx.send(f'{ctx.author.mention}, {random.choice(resp)}\nВы поставили на: `орёл`')
	elif arg == 'решка':
		await ctx.send(f'{ctx.author.mention}, подбрасываю монетку.')
		await asyncio.sleep(3)
		await ctx.send(f'{ctx.author.mention}, {random.choice(resp)}\nВы поставили на: `решка`')

@client.command()
@commands.is_owner()
async def inmessage(ctx):
	await ctx.message.delete()
	emb = nextcord.Embed(title = '👋 Спасибо, что пригласили меня!', description = '<:9294passed:926412397080629249> Привет, меня зовут Leafy.', color=0x2F3136)
	emb.add_field(name='Что я могу?', value='`Я - универсальный бот!`\n**Я могу**:\n`Настройка сервера` `Модерация` `Информация` `Развлечения` `Манипуляции с картинками` `РП` `Экономика` `Розыгрыши` `Приветственные каналы` `Межсерверная система уровней` `Временные голосовые каналы` `NSFW`', inline=False)
	emb.add_field(name='Мой стандартный префикс:', value='`?`', inline=False)
	emb.add_field(name='Связь:', value='`mqchine#1422`', inline=False)
	emb.set_thumbnail(url = client.user.display_avatar)
	emb.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon)
	emb.set_image(url='https://st3.depositphotos.com/32100976/34458/i/600/depositphotos_344586092-stock-photo-anime-wallpapers-black-white-anime.jpg')
	view = nextcord.ui.View()
	item = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "Сервер",emoji = "👑", url = "https://discord.gg/CT8VekA57Z")
	item2 = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "ВКонтакте",emoji = "🧭", url = "https://vk.com/kykarekman")
	item3 = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "Github",emoji = "🐱", url = "https://github.com/mqchinee")
	item4 = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "Сайт",emoji = "✅", url = "https://leafy.cf/")
	view.add_item(item)
	view.add_item(item2)
	view.add_item(item3)
	view.add_item(item4)
	await ctx.send(embed=emb, view = view)

@inmessage.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@client.command()
@commands.is_owner()
async def go(ctx, member: nextcord.Member=None):
	await ctx.message.delete()
	if member == None:
		member = ctx.author
		m = nextcord.Embed(title='Go kitty go!', description=f'{member.mention}, ну а чё, кошечка!', colour=nextcord.Colour.red())
		m.set_image(url='https://c.tenor.com/jFn8sS1Et-0AAAAd/cat.gif')
		await ctx.send(embed=m)
	else:
		m = nextcord.Embed(title='Go kitty go!', description=f'{member.mention}, ну а чё, кошечка!', colour=nextcord.Colour.red())
		m.set_image(url='https://c.tenor.com/jFn8sS1Et-0AAAAd/cat.gif')
		await ctx.send(embed=m)

@go.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Команда не найдена.')

@client.command()
@commands.is_owner()
async def inv(ctx, arg):
		discord_guild = client.get_guild(int(arg))
		link = await discord_guild.text_channels[0].create_invite()
		user = await client.fetch_user(748494305005535253)
		e = nextcord.Embed(title='<a:checkon:928259275090972772> Ссылка для вступления на сервер!', color=0x2F3136)
		await user.send(embed=e)
		await user.send(link)

@inv.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@client.command()
@commands.is_owner()
async def cp(ctx, mode, *, arg):
	if mode == "guilds":
		await client.change_presence(activity=nextcord.Streaming(name=f"{str(len(client.guilds))} серверов!", url="https://www.twitch.tv/twitch"))
		await ctx.send(f"<a:checkon:928259275090972772> Статус бота изменён на:\nТип: {mode}")
	elif mode == "--reset":
		await client.change_presence(activity=nextcord.Streaming(name=f"?help | leafy.cf | v3.7.3", url="https://www.twitch.tv/twitch"))
		await ctx.send("<a:checkon:928259275090972772> Статус бота сброшен!")
	elif mode == "users":
		await client.change_presence(activity=nextcord.Streaming(name=f"{len(set(client.get_all_members()))} пользователей!", url="https://www.twitch.tv/twitch"))
		await ctx.send(f"<a:checkon:928259275090972772> Статус бота изменён на:\nТип: {mode}")
	elif mode == "playing":
		await client.change_presence(activity=nextcord.Game(arg))
		await ctx.send(f"<a:checkon:928259275090972772> Статус бота изменён на:\n `{arg}`\nТип: {mode}")
	elif mode == 'streaming':
		await client.change_presence(activity=nextcord.Streaming(name=f"{arg}", url="https://www.twitch.tv/twitch"))
		await ctx.send(f"<a:checkon:928259275090972772> Статус бота изменён на:\n `{arg}`\nТип: {mode}")
	elif mode == "listening":
		await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{arg}"))
		await ctx.send(f"<a:checkon:928259275090972772> Статус бота изменён на:\n `{arg}`\nТип: {mode}")
	elif mode == "watching":
		await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{arg}"))
		await ctx.send(f"<a:checkon:928259275090972772> Статус бота изменён на:\n `{arg}`\nТип: {mode}")
	else:
		await ctx.send(f'<a:checkoff:928259276273758208> Доступные режимы:\n`playing`, `streaming`, `watching`, `listening`, `--reset`, `guilds`, `users`')

@cp.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

# Экономика!
@client.command(aliases = ['bal', 'cash', 'баланс'])

async def __balance(ctx, member: nextcord.Member = None):
	if member is None:
		await ctx.send(embed= nextcord.Embed(
			title='Баланс',
			description=f"""Баланс пользователя {ctx.author.mention} составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}** <:coinleafy:927841623667269663>\nРепутация: **{cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**\nИгр сыграно: **{cursor.execute("SELECT gamesplayed FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**\nБанк: **{cursor.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}** <:coinleafy:927841623667269663>""",
			color=0x2F3136,
			timestamp=ctx.message.created_at
		))
	else:
		await ctx.send(embed= nextcord.Embed(
			title='Баланс',
			description=f"""Баланс пользователя {member.mention} составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}** <:coinleafy:927841623667269663>\nРепутация: **{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**\nИгр сыграно: **{cursor.execute("SELECT gamesplayed FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**\nБанк: **{cursor.execute("SELECT bank FROM users WHERE id = {}".format(member.id)).fetchone()[0]}** <:coinleafy:927841623667269663>""",
			color=0x2F3136,
			timestamp=ctx.message.created_at
		))

@client.command(aliases = ['award', 'aw'])
@commands.is_owner()
async def __award(ctx, member: nextcord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя, которому хотите выдать деньги!')
	else:
		if amount is None:
			await ctx.send(f'{ctx.author.mention}, укажите сумму!')
		elif amount < 1:
			await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
			connection.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@__award.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@client.command(aliases = ['set', 's'])
@commands.is_owner()
async def __set(ctx, member: nextcord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя, которому хотите установить баланс!')
	else:
		if amount is None:
			await ctx.send(f'{ctx.author.mention}, укажите сумму!')
		elif amount < 0:
			await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
		else:
			cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(amount, member.id))
			connection.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@__set.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@client.command(aliases = ['take', 'tk'])
@commands.is_owner()
async def __take(ctx, member: nextcord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя, у которого хотите забрать деньги')
	else:
		if amount is None:
			await ctx.send(f'{ctx.author.mention}, укажите сумму!')
		elif amount < 1:
			await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
		else:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, member.id))
			connection.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@__take.error
async def error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

@client.group(name='shop', invoke_without_command=True, aliases=['магазин'])

async def __shop(ctx):
	dbhelp = sqlite3.connect('server.db')
	cursorhelp = dbhelp.cursor()
	cursorhelp.execute("SELECT prefix FROM prefixes WHERE id = ?", (ctx.guild.id,))
	resulthelp = cursorhelp.fetchone()
	p = str(resulthelp[0])
	e = nextcord.Embed(title='Магазин ролей', timestamp=ctx.message.created_at, color=0x2F3136)
	e.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	e.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)

	for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
		if ctx.guild.get_role(row[0]) != None:
			e.add_field(name = f"Стоимость: {row[1]} <:coinleafy:927841623667269663>", value=f"Вы приобретете роль: {ctx.guild.get_role(row[0]).mention}\n`Если вы не можете упомянуть роль, напишите:\n{p}shop buy <@&{ctx.guild.get_role(row[0]).id}>`", inline=False)
		else:
			pass

	await ctx.send(embed=e)

@__shop.command(aliases=['add', 'добавить'])

@commands.has_permissions( administrator = True )
async def __ashop(ctx, role: nextcord.Role = None, cost: int = None):
	if role is None:
		await ctx.send(f'{ctx.author.mention}, укажите роль!')
	else:
		if cost is None:
			await ctx.send(f'{ctx.author.mention}, укажите цену!')
		elif cost < 0:
			await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
		else:
			cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
			connection.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@__shop.command(aliases=['remove', 'убрать'])

@commands.has_permissions( administrator = True )
async def __rshop(ctx, role: nextcord.Role = None):
	if role is None:
		await ctx.send(f'{ctx.author.mention}, укажите роль!')
	else:
		cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
		connection.commit()

		await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@__shop.command(aliases=['buy', 'купить'])

async def __buy(ctx, role: nextcord.Role = None):
	if role is None:
		await ctx.send(f'{ctx.author.mention}, укажите роль!')
	else:
		if role in ctx.author.roles:
			await ctx.send('У вас уже есть эта роль!')
		elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
		else:
			await ctx.author.add_roles(role)
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
			cursor.execute("UPDATE gmoney SET cash = cash + {} WHERE guild = {}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.guild.id))
			connection.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@client.command(aliases = ['send', 'отправить'])

async def __send(ctx, member: nextcord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя, которому хотите перекинуть деньги!')
	else:
		if amount is None:
			await ctx.send(f'{ctx.author.mention}, укажите сумму!')
		elif amount < 1:
			await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
		elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < amount:
			await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@client.command(aliases=['rep', 'реп'])

@commands.cooldown(1, 18000, commands.BucketType.user)
async def __rep(ctx, member: nextcord.Member = None):
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя!')
	else:
		if member.id == ctx.author.id:
			await ctx.send(f'{ctx.author.mention}, вы не можете указать самого себя')
		else:
			cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, member.id))
			connection.commit()
			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@client.command(aliases=['bag', 'мешок'])

@commands.cooldown(1, 43200, commands.BucketType.user)
async def __bag(ctx):
	cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(3500, ctx.author.id))
	connection.commit()
	await ctx.message.add_reaction('<a:checkon:928259275090972772>')
	e = nextcord.Embed(title='Ежедневный мешочек!', description=f'{ctx.author.mention}, Вы получили **3500** <:coinleafy:927841623667269663>', timestamp=ctx.message.created_at, color=0x2F3136)
	e.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	e.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	await ctx.send(embed=e)

@client.command(aliases=['угадать'])

async def guess(ctx):
	cursor.execute("UPDATE users SET gamesplayed = gamesplayed + {} WHERE id = {}".format(1, ctx.author.id))
	if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < 500:
		await ctx.send(f'{ctx.author.mention}, чтобы играть, вы должны иметь не менее **500** <:coinleafy:927841623667269663> на балансе!')
	else:
		await ctx.send(f"{ctx.author.mention}, угадай число от 1 до 6!\n**Если ты угадаешь, ты получишь 2000 <:coinleafy:927841623667269663>, если нет - потеряешь 500 <:coinleafy:927841623667269663>**")
		numbers = ["1", "2", "3", "4", "5", "6"]
		choice = random.choice(numbers)
		answer = await client.wait_for("message")
		if answer.content == choice:
			await ctx.send(f"{ctx.author.mention}, ты угадал правильное число!\n**Ты получаешь 2000** <:coinleafy:927841623667269663>")
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(2000, ctx.author.id))
			connection.commit()
		else:
			await ctx.send(f"{ctx.author.mention}, ты проиграл! Число, которое я загадала - {choice}\n**Ты потерял 500** <:coinleafy:927841623667269663>")
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(500, ctx.author.id))
			connection.commit()

@client.command(aliases=['слоты'])

async def slot(ctx):
	cursor.execute("UPDATE users SET gamesplayed = gamesplayed + {} WHERE id = {}".format(1, ctx.author.id))
	if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < 250:
		await ctx.send(f'{ctx.author.mention}, чтобы играть, вы должны иметь не менее **250** <:coinleafy:927841623667269663> на балансе!')
	else:
		tst = ['<:8420moderationvhigh:926414280826421248>', '<:1486moderationvhighest:926414280394412033>', '<:3337moderationvmedium:926414280415395890>']
		first = random.choice(tst)
		second = random.choice(tst)
		third = random.choice(tst)
		test1 = random.choice(tst)
		test2 = random.choice(tst)
		test3 = random.choice(tst)
		test4 = random.choice(tst)
		test5 = random.choice(tst)
		test6 = random.choice(tst)
		e = nextcord.Embed(title='Слоты!', description=f'{test1} | {test2} | {test3}\n{first} | {second} | {third} ⬅️\n {test4} | {test5} | {test6}', timestamp=ctx.message.created_at, color=0x2F3136)
		e.set_author(name=client.user.name, icon_url=client.user.display_avatar)
		e.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		await ctx.send(embed=e)
		if first == second == third:
			await ctx.send(f"{ctx.author.mention}, ты победил!\nДжекпот! Ты получаешь 1000 <:coinleafy:927841623667269663>")
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(1000, ctx.author.id))
			connection.commit()
		elif first == third:
			await ctx.send(f"{ctx.author.mention}, ты победил!\nТы получаешь 150 <:coinleafy:927841623667269663> (Теряешь 250 <:coinleafy:927841623667269663>)")
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(250, ctx.author.id))
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(150, ctx.author.id))
			connection.commit()
		elif first == second:
			await ctx.send(f"{ctx.author.mention}, ты победил!\nТы получаешь 150 <:coinleafy:927841623667269663> (Теряешь 250 <:coinleafy:927841623667269663>)")
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(250, ctx.author.id))
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(150, ctx.author.id))
			connection.commit()
		elif second == third:
			await ctx.send(f"{ctx.author.mention}, ты победил!\nТы получаешь 150 <:coinleafy:927841623667269663> (Теряешь 250 <:coinleafy:927841623667269663>)")
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(250, ctx.author.id))
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(150, ctx.author.id))
			connection.commit()
		else:
			await ctx.send(f"{ctx.author.mention}, ты проиграл!\nТы потерял 500 <:coinleafy:927841623667269663>")
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(500, ctx.author.id))
			connection.commit()

@client.command(aliases=['ограбление'])

async def robbery(ctx):
	cursor.execute("UPDATE users SET gamesplayed = gamesplayed + {} WHERE id = {}".format(1, ctx.author.id))
	if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < 1000:
		await ctx.send(f'{ctx.author.mention}, чтобы играть, вы должны иметь не менее **1000** <:coinleafy:927841623667269663> на балансе!')
	else:
		tst = ["Удачно", "Неудачно"]
		first = random.choice(tst)
		second = random.choice(tst)
		third = random.choice(tst)
		if first == second == third:
			emb = nextcord.Embed(title='Процесс ограбления банка!', description=f'`{first}`,`{second}`,`{third}`\n<a:checkon:928259275090972772> Вам удалось ограбить банк! Ваш счёт удваивается! <:coinleafy:927841623667269663>', color=0x2F3136)
			emb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
			emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
			await ctx.send(embed=emb)
			cursor.execute("UPDATE users SET cash = cash * {} WHERE id = {}".format(2, ctx.author.id))
			connection.commit()
		else:
			emb = nextcord.Embed(title='Процесс ограбления банка!', description=f'`{first}`,`{second}`,`{third}`\n<a:checkoff:928259276273758208> Вам не удалось ограбить банк! Ваш счёт поделён на 4! <:coinleafy:927841623667269663>', color=0x2F3136)
			emb.set_author(name=client.user.name, icon_url=client.user.display_avatar)
			emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
			await ctx.send(embed=emb)
			cursor.execute("UPDATE users SET cash = cash / {} WHERE id = {}".format(4, ctx.author.id))
			connection.commit()

@client.group(name='lb', invoke_without_command=True, aliases=['лб'])

async def lb(ctx):
	await ctx.send('<a:checkoff:928259276273758208> Пожалуйста, укажите:\nlb `cash` для отображения доски лидеров по наличным\nlb `bank` для отображения доски лидеров по банковскому счёту\n lb `treasury` для отображения доски лидеров по казне')

@lb.command(aliases=['cash', 'наличные'])

async def __leader(ctx):
	embed = nextcord.Embed(title='Топ 12 богачей! (наличные)', colour=nextcord.Colour.green())
	embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	counter = 0

	for row in cursor.execute("SELECT name, cash, gamesplayed FROM users ORDER BY cash DESC LIMIT 12"):
		counter += 1
		embed.add_field(name=f'# {counter} | {row[0]}', value=f'Баланс: {row[1]} <:coinleafy:927841623667269663>\nИгр сыграно: {row[2]}')

	await ctx.send(embed=embed)

@client.command(aliases = ['repset', 'reps'])
@commands.is_owner()
async def __repset(ctx, member: nextcord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя, которому хотите установить репутацию!')
	else:
		if amount is None:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		elif amount < 0:
			await ctx.send(f'{ctx.author.mention}, нельзя указывать число ниже 0!')
		else:
			cursor.execute("UPDATE users SET rep = {} WHERE id = {}".format(amount, member.id))
			connection.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@client.command(aliases = ['gsset', 'gss'])
@commands.is_owner()
async def __gsset(ctx, member: nextcord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя, которому хотите установить кол-во игр!')
	else:
		if amount is None:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		elif amount < 0:
			await ctx.send(f'{ctx.author.mention}, нельзя указывать число ниже 0!')
		else:
			cursor.execute("UPDATE users SET gamesplayed = {} WHERE id = {}".format(amount, member.id))
			connection.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@client.command(aliases=['work', 'работа'])

@commands.cooldown(2, 18000, commands.BucketType.user)
async def __work(ctx):
	money = random.randint(1000,2500)
	cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(money, ctx.author.id))
	connection.commit()
	await ctx.message.add_reaction('<a:checkon:928259275090972772>')
	works = ['строителем','поваром','разносчиком пиццы','гримером','гитаристом','няней','парикмахером','касиром','дворником','охранником']
	hours = random.randint(2,12)
	e = nextcord.Embed(title='Работа!', description=f'<a:checkon:928259275090972772> {ctx.author.mention}, Вы поработали {random.choice(works)} на протяжении {hours}-х часов и получили **{money}** <:coinleafy:927841623667269663>', timestamp=ctx.message.created_at, color=0x2F3136)
	e.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	e.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	await ctx.send(embed=e)

@client.command(aliases = ['deposit', 'депозит'])

async def __deposit(ctx, amount: int = None):
	if amount is None:
		await ctx.send(f'{ctx.author.mention}, укажите сумму!')
	elif amount < 1:
		await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
	elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < amount:
		await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
	else:
		cursor.execute("UPDATE users SET bank = bank + {} WHERE id = {}".format(amount, ctx.author.id))
		cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
		connection.commit()

		await ctx.message.add_reaction('<a:checkon:928259275090972772>')    

@client.command(aliases = ['withdraw', 'снять'])

async def __withdraw(ctx, amount: int = None):
	if amount is None:
		await ctx.send(f'{ctx.author.mention}, укажите сумму!')
	elif amount < 1:
		await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
	elif cursor.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < amount:
		await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
	else:
		cursor.execute("UPDATE users SET bank = bank - {} WHERE id = {}".format(amount, ctx.author.id))
		cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, ctx.author.id))
		connection.commit()

		await ctx.message.add_reaction('<a:checkon:928259275090972772>')    

@client.command(aliases = ['rob', 'ограбить'])

@commands.cooldown(2, 10000, commands.BucketType.user)
async def __rob(ctx, member: nextcord.Member = None):
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя, которого хотите ограбить!')
	elif member is ctx.author:
		await ctx.send(f'{ctx.author.mention}, вы не можете ограбить сами себя!')
	else:
		if cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0] < 800:
			await ctx.send("У этого пользователя слишком мало денег, нету чего грабить!")
		else:
			rob = random.randint(50,800)
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(rob, member.id))
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rob, ctx.author.id))
			connection.commit()

			e = nextcord.Embed(title='Ограбление', description=f'<a:checkon:928259275090972772> Вы ограбили {member.mention} и получили **{rob}** <:coinleafy:927841623667269663>', timestamp=ctx.message.created_at, color=0x2F3136)
			await ctx.send(embed=e)

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@lb.command(aliases=['bank', 'банк'])

async def __leaderbank(ctx):
	embed = nextcord.Embed(title='Топ 12 богачей! (банк)', colour=nextcord.Colour.green())
	embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	counter = 0

	for row in cursor.execute("SELECT name, bank, gamesplayed FROM users ORDER BY bank DESC LIMIT 12"):
		counter += 1
		embed.add_field(name=f'# {counter} | {row[0]}', value=f'Банк: {row[1]} <:coinleafy:927841623667269663>\nИгр сыграно: {row[2]}')

	await ctx.send(embed=embed)

@client.group(name='treasury', invoke_without_command=True, aliases=['казна'])

async def __treasury(ctx):
	e = nextcord.Embed(title='Казна сервера', description=f"""Казна **{ctx.guild.name}** составляет **{cursor.execute("SELECT cash FROM gmoney WHERE guild = {}".format(ctx.guild.id)).fetchone()[0]}** <:coinleafy:927841623667269663>""", timestamp=ctx.message.created_at, color=0x2F3136)
	await ctx.send(embed=e)

@__treasury.command(aliases = ['take', 'взять'])

@commands.has_permissions(administrator=True)
async def __ttake(ctx, amount: int = None):
	if amount is None:
		await ctx.send(f'{ctx.author.mention}, укажите сумму!')
	elif amount < 1:
		await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
	elif cursor.execute("SELECT cash FROM gmoney WHERE guild = {}".format(ctx.guild.id)).fetchone()[0] < amount:
		await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
	else:
		cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, ctx.author.id))
		cursor.execute("UPDATE gmoney SET cash = cash - {} WHERE guild = {}".format(amount, ctx.guild.id))
		connection.commit()

		await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@__treasury.command(aliases = ['deposit', 'положить'])

async def __tdep(ctx, amount: int = None):
	if amount is None:
		await ctx.send(f'{ctx.author.mention}, укажите сумму!')
	elif amount < 1:
		await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
	elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < amount:
		await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
	else:
		cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
		cursor.execute("UPDATE gmoney SET cash = cash + {} WHERE guild = {}".format(amount, ctx.guild.id))
		connection.commit()

		await ctx.message.add_reaction('<a:checkon:928259275090972772>')


@lb.command(aliases=['treasury', 'казна'])

async def __leadertreas(ctx):
	embed = nextcord.Embed(title='Топ 12 серверов! (казна)', colour=nextcord.Colour.green())
	embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	counter = 0

	for row in cursor.execute("SELECT name, cash FROM gmoney ORDER BY cash DESC LIMIT 12"):
		counter += 1
		embed.add_field(name=f'# {counter} | {str(row[0])}', value=f'Баланс: {row[1]} <:coinleafy:927841623667269663>', inline=False)

	await ctx.send(embed=embed)

@client.command(aliases = ['gaward', 'gaw'])
@commands.is_owner()
async def __gaward(ctx, amount: int = None):
	cursor.execute("UPDATE gmoney SET cash = cash + {} WHERE guild = {}".format(amount, ctx.guild.id))
	сonnection.commit()
	await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@client.command()
@commands.is_owner()
async def test(ctx):
	view = HelpCommandView()
	await ctx.send("Помощь!", view=view)

@client.command(aliases=['копать'])
@commands.cooldown(125, 10800, commands.BucketType.user)
async def mine(ctx):
	cursor1.execute("SELECT pickaxe FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data = cursor1.fetchone()

	if data[0] == 0:
		chance = [1, 2, 3, 4, 5]
		up = random.choice(chance)
		res = random.randint(1, 8)
		wood = up*res

		cursor1.execute("UPDATE users SET wood = wood + ? WHERE user_id = ? AND guild_id = ?", (wood, ctx.author.id, ctx.guild.id,))

		emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

		emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb1.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

		emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb2.add_field(name='Вы накопали:', value=f'**{wood}** <:8343oaklog:939195860422623252>')
		emb2.add_field(name='Инструмент:', value=f'**Рука**')
		emb2.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

		msg = await ctx.send(embed=emb)
		await asyncio.sleep(1)
		await msg.edit(embed=emb1)
		await asyncio.sleep(1)
		await msg.edit(embed=emb2)
	elif data[0] == 1:
		chance = [1, 2, 3, 4, 5]
		up = random.choice(chance)
		res = random.randint(1, 8)
		wood = up*res

		chance1 = [1, 2, 3]
		up1 = random.choice(chance1)
		res1 = random.randint(1, 5)
		wood1 = up1*res1

		cursor1.execute("UPDATE users SET cobblestone = cobblestone + ? WHERE user_id = ? AND guild_id = ?", (wood, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET coal = coal + ? WHERE user_id = ? AND guild_id = ?", (wood1, ctx.author.id, ctx.guild.id,))

		emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

		emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb1.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

		emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb2.add_field(name='Вы накопали:', value=f'**{wood}** <:6939cobblestone:939195860456210502>\n**{wood1}** <:9359_MCcoal:939195859894169600>')
		emb2.add_field(name='Инструмент:', value=f'<:4065_Wood_Pick:939195859801870387>')
		emb2.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

		msg = await ctx.send(embed=emb)
		await asyncio.sleep(1)
		await msg.edit(embed=emb1)
		await asyncio.sleep(1)
		await msg.edit(embed=emb2)
	elif data[0] == 2:
		chance = [1, 2, 3, 4, 5, 6, 7]
		up = random.choice(chance)
		res = random.randint(1, 10)
		wood = up*res

		chance1 = [1, 2, 3, 4]
		up1 = random.choice(chance1)
		res1 = random.randint(1, 7)
		wood1 = up1*res1

		chance2 = [1, 2]
		up2 = random.choice(chance2)
		res2 = random.randint(1, 3)
		wood2 = up2*res2

		cursor1.execute("UPDATE users SET cobblestone = cobblestone + ? WHERE user_id = ? AND guild_id = ?", (wood, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET coal = coal + ? WHERE user_id = ? AND guild_id = ?", (wood1, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET iron_ore = iron_ore + ? WHERE user_id = ? AND guild_id = ?", (wood2, ctx.author.id, ctx.guild.id,))

		emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

		emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb1.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

		emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb2.add_field(name='Вы накопали:', value=f'**{wood}** <:6939cobblestone:939195860456210502>\n**{wood1}** <:9359_MCcoal:939195859894169600>\n**{wood2}** <:unnamed:939195859919331428>')
		emb2.add_field(name='Инструмент:', value=f'<:2465stonepickaxe:939195860124860487>')
		emb2.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

		msg = await ctx.send(embed=emb)
		await asyncio.sleep(1)
		await msg.edit(embed=emb1)
		await asyncio.sleep(1)
		await msg.edit(embed=emb2)
	elif data[0] == 3:
		chance = [1, 2, 3, 4, 5, 6, 7, 8]
		up = random.choice(chance)
		res = random.randint(1, 11)
		wood = up*res

		chance1 = [1, 2, 3, 4, 5]
		up1 = random.choice(chance1)
		res1 = random.randint(1, 8)
		wood1 = up1*res1

		chance2 = [1, 2, 3]
		up2 = random.choice(chance2)
		res2 = random.randint(1, 4)
		wood2 = up2*res2

		chance3 = [1, 2, 3]
		up3 = random.choice(chance3)
		res3 = random.randint(1, 4)
		wood3 = up3*res3

		chance4 = [1, 2]
		up4 = random.choice(chance4)
		res4 = random.randint(1, 2)
		wood4 = up4*res4

		cursor1.execute("UPDATE users SET cobblestone = cobblestone + ? WHERE user_id = ? AND guild_id = ?", (wood, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET coal = coal + ? WHERE user_id = ? AND guild_id = ?", (wood1, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET iron_ore = iron_ore + ? WHERE user_id = ? AND guild_id = ?", (wood2, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET gold_ore = gold_ore + ? WHERE user_id = ? AND guild_id = ?", (wood3, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET diamonds = diamonds + ? WHERE user_id = ? AND guild_id = ?", (wood4, ctx.author.id, ctx.guild.id,))

		emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

		emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb1.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

		emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb2.add_field(name='Вы накопали:', value=f'**{wood}** <:6939cobblestone:939195860456210502>\n**{wood1}** <:9359_MCcoal:939195859894169600>\n**{wood2}** <:unnamed:939195859919331428>\n**{wood3} <:gold_ore:939195859747356692>**\n**{wood4}** <:8946_diamond:939195860389081119>')
		emb2.add_field(name='Инструмент:', value=f'<:irnpic:939223290105454632>')
		emb2.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

		msg = await ctx.send(embed=emb)
		await asyncio.sleep(1)
		await msg.edit(embed=emb1)
		await asyncio.sleep(1)
		await msg.edit(embed=emb2)
	elif data[0] == 4:
		chance = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		up = random.choice(chance)
		res = random.randint(1, 12)
		wood = up*res

		chance1 = [1, 2, 3, 4, 5, 6]
		up1 = random.choice(chance1)
		res1 = random.randint(1, 9)
		wood1 = up1*res1

		chance2 = [1, 2, 3, 4]
		up2 = random.choice(chance2)
		res2 = random.randint(1, 5)
		wood2 = up2*res2

		chance3 = [1, 2, 3, 4]
		up3 = random.choice(chance3)
		res3 = random.randint(1, 5)
		wood3 = up3*res3

		chance4 = [1, 2, 3]
		up4 = random.choice(chance4)
		res4 = random.randint(1, 3)
		wood4 = up4*res4

		cursor1.execute("UPDATE users SET cobblestone = cobblestone + ? WHERE user_id = ? AND guild_id = ?", (wood, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET coal = coal + ? WHERE user_id = ? AND guild_id = ?", (wood1, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET iron_ore = iron_ore + ? WHERE user_id = ? AND guild_id = ?", (wood2, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET gold_ore = gold_ore + ? WHERE user_id = ? AND guild_id = ?", (wood3, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET diamonds = diamonds + ? WHERE user_id = ? AND guild_id = ?", (wood4, ctx.author.id, ctx.guild.id,))

		emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

		emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb1.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

		emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb2.add_field(name='Вы накопали:', value=f'**{wood}** <:6939cobblestone:939195860456210502>\n**{wood1}** <:9359_MCcoal:939195859894169600>\n**{wood2}** <:unnamed:939195859919331428>\n**{wood3} <:gold_ore:939195859747356692>**\n**{wood4}** <:8946_diamond:939195860389081119>')
		emb2.add_field(name='Инструмент:', value=f'<:1153goldpickaxe:939195860007415868>')
		emb2.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

		msg = await ctx.send(embed=emb)
		await asyncio.sleep(1)
		await msg.edit(embed=emb1)
		await asyncio.sleep(1)
		await msg.edit(embed=emb2)
	elif data[0] == 5:
		chance = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		up = random.choice(chance)
		res = random.randint(1, 13)
		wood = up*res

		chance1 = [1, 2, 3, 4, 5, 6, 7]
		up1 = random.choice(chance1)
		res1 = random.randint(1, 10)
		wood1 = up1*res1

		chance2 = [1, 2, 3, 4, 5]
		up2 = random.choice(chance2)
		res2 = random.randint(1, 6)
		wood2 = up2*res2

		chance3 = [1, 2, 3, 4, 5]
		up3 = random.choice(chance3)
		res3 = random.randint(1, 6)
		wood3 = up3*res3

		chance4 = [1, 2, 3, 4]
		up4 = random.choice(chance4)
		res4 = random.randint(1, 4)
		wood4 = up4*res4

		chance5 = [1, 2, 3]
		up5 = random.choice(chance5)
		res5 = random.randint(1, 3)
		wood5 = up5*res5

		chance6 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		up6 = random.choice(chance6)
		res6 = random.randint(1, 13)
		wood6 = up6*res6

		cursor1.execute("UPDATE users SET cobblestone = cobblestone + ? WHERE user_id = ? AND guild_id = ?", (wood, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET coal = coal + ? WHERE user_id = ? AND guild_id = ?", (wood1, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET iron_ore = iron_ore + ? WHERE user_id = ? AND guild_id = ?", (wood2, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET gold_ore = gold_ore + ? WHERE user_id = ? AND guild_id = ?", (wood3, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET diamonds = diamonds + ? WHERE user_id = ? AND guild_id = ?", (wood4, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET debris_ore = debris_ore + ? WHERE user_id = ? AND guild_id = ?", (wood5, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET netherack = netherack + ? WHERE user_id = ? AND guild_id = ?", (wood6, ctx.author.id, ctx.guild.id,))

		emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

		emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb1.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

		emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb2.add_field(name='Вы накопали:', value=f'**{wood}** <:6939cobblestone:939195860456210502>\n**{wood1}** <:9359_MCcoal:939195859894169600>\n**{wood2}** <:unnamed:939195859919331428>\n**{wood3} <:gold_ore:939195859747356692>**\n**{wood4}** <:8946_diamond:939195860389081119>\n**{wood5}** <:Ancient_Debris_top_texture_JE1_B:939195860317798480>\n**{wood6}** <:8159netherrack:939195860653334618>')
		emb2.add_field(name='Инструмент:', value=f'<:2898picodediamante:939195860032577577>')
		emb2.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

		msg = await ctx.send(embed=emb)
		await asyncio.sleep(1)
		await msg.edit(embed=emb1)
		await asyncio.sleep(1)
		await msg.edit(embed=emb2)
	elif data[0] == 6:
		chance = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		up = random.choice(chance)
		res = random.randint(1, 13)
		wood = up*res

		chance1 = [1, 2, 3, 4, 5, 6, 7]
		up1 = random.choice(chance1)
		res1 = random.randint(1, 10)
		wood1 = up1*res1

		chance2 = [1, 2, 3, 4, 5]
		up2 = random.choice(chance2)
		res2 = random.randint(1, 6)
		wood2 = up2*res2

		chance3 = [1, 2, 3, 4, 5]
		up3 = random.choice(chance3)
		res3 = random.randint(1, 6)
		wood3 = up3*res3

		chance4 = [1, 2, 3, 4, 5, 6]
		up4 = random.choice(chance4)
		res4 = random.randint(1, 6)
		wood4 = up4*res4

		chance5 = [1, 2, 3, 4, 5]
		up5 = random.choice(chance5)
		res5 = random.randint(1, 5)
		wood5 = up5*res5

		chance6 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		up6 = random.choice(chance6)
		res6 = random.randint(1, 13)
		wood6 = up6*res6

		cursor1.execute("UPDATE users SET cobblestone = cobblestone + ? WHERE user_id = ? AND guild_id = ?", (wood, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET coal = coal + ? WHERE user_id = ? AND guild_id = ?", (wood1, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET iron_ore = iron_ore + ? WHERE user_id = ? AND guild_id = ?", (wood2, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET gold_ore = gold_ore + ? WHERE user_id = ? AND guild_id = ?", (wood3, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET diamonds = diamonds + ? WHERE user_id = ? AND guild_id = ?", (wood4, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET debris_ore = debris_ore + ? WHERE user_id = ? AND guild_id = ?", (wood5, ctx.author.id, ctx.guild.id,))
		cursor1.execute("UPDATE users SET netherack = netherack + ? WHERE user_id = ? AND guild_id = ?", (wood6, ctx.author.id, ctx.guild.id,))

		emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

		emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb1.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

		emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb2.add_field(name='Вы накопали:', value=f'**{wood}** <:6939cobblestone:939195860456210502>\n**{wood1}** <:9359_MCcoal:939195859894169600>\n**{wood2}** <:unnamed:939195859919331428>\n**{wood3} <:gold_ore:939195859747356692>**\n**{wood4}** <:8946_diamond:939195860389081119>\n**{wood5}** <:Ancient_Debris_top_texture_JE1_B:939195860317798480>\n**{wood6}** <:8159netherrack:939195860653334618>')
		emb2.add_field(name='Инструмент:', value=f'<:2082_Netherite_pickaxe:939195859910934568>')
		emb2.set_author(name='Копаем...', icon_url=client.user.display_avatar)
		emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

		msg = await ctx.send(embed=emb)
		await asyncio.sleep(1)
		await msg.edit(embed=emb1)
		await asyncio.sleep(1)
		await msg.edit(embed=emb2)
	connection1.commit()

@client.command(aliases=['инвентарь'])
async def inventory(ctx):
	pick = ""

	cursor1.execute("SELECT pickaxe FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data = cursor1.fetchone()
	if data[0] == 0:
		pick = "Рука"
	elif data[0] == 1:
		pick = "<:4065_Wood_Pick:939195859801870387>"
	elif data[0] == 2:
		pick = "<:2465stonepickaxe:939195860124860487>"
	elif data[0] == 3:
		pick = "<:irnpic:939223290105454632>"
	elif data[0] == 4:
		pick = "<:1153goldpickaxe:939195860007415868>"
	elif data[0] == 5:
		pick = "<:2898picodediamante:939195860032577577>"
	elif data[0] == 6:
		pick = "<:2082_Netherite_pickaxe:939195859910934568>"

	cursor1.execute("SELECT coins FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data1 = cursor1.fetchone()

	cursor1.execute("SELECT wood FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data2 = cursor1.fetchone()

	cursor1.execute("SELECT iron_ore FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data3 = cursor1.fetchone()

	cursor1.execute("SELECT gold_ore FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data4 = cursor1.fetchone()

	cursor1.execute("SELECT debris_ore FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data5 = cursor1.fetchone()

	cursor1.execute("SELECT iron FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data6 = cursor1.fetchone()

	cursor1.execute("SELECT gold FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data7 = cursor1.fetchone()

	cursor1.execute("SELECT coal FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data8 = cursor1.fetchone()

	cursor1.execute("SELECT diamonds FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data9 = cursor1.fetchone()

	cursor1.execute("SELECT emerald FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data10 = cursor1.fetchone()

	cursor1.execute("SELECT cobblestone FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data11 = cursor1.fetchone()

	cursor1.execute("SELECT netherack FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data12 = cursor1.fetchone()

	cursor1.execute("SELECT netherite FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data13 = cursor1.fetchone()

	emb = nextcord.Embed(title='Инвентарь ' + str(ctx.author), description=f'Инструмент: {pick}\n\n🪙 {str(data1[0])}, <:8343oaklog:939195860422623252> {str(data2[0])}, <:unnamed:939195859919331428> {str(data3[0])}\n\n <:gold_ore:939195859747356692> {str(data4[0])}, <:Ancient_Debris_top_texture_JE1_B:939195860317798480> {str(data5[0])}, <:1532iron:939195860317773856> {str(data6[0])}\n\n <:3621gold:939195860129042452> {str(data7[0])}, <:9359_MCcoal:939195859894169600> {str(data8[0])}, <:8946_diamond:939195860389081119> {str(data9[0])}\n\n <:6410emerald:939195860141621258> {str(data10[0])}, <:6939cobblestone:939195860456210502> {str(data11[0])}, <:8159netherrack:939195860653334618> {str(data12[0])}\n\n<:2352nether:939195860032573460> {str(data13[0])}', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
	emb.set_author(name='Инвентарь...', icon_url=client.user.display_avatar)
	await ctx.send(embed=emb)

@client.command(aliases=['крафт'])
async def craft(ctx, arg=None):
	pick = ""

	cursor1.execute("SELECT pickaxe FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	data = cursor1.fetchone()
	if data[0] == 0:
		pick = "Рука"
	elif data[0] == 1:
		pick = "<:4065_Wood_Pick:939195859801870387>"
	elif data[0] == 2:
		pick = "<:2465stonepickaxe:939195860124860487>"
	elif data[0] == 3:
		pick = "<:irnpic:939223290105454632>"
	elif data[0] == 4:
		pick = "<:1153goldpickaxe:939195860007415868>"
	elif data[0] == 5:
		pick = "<:2898picodediamante:939195860032577577>"
	elif data[0] == 6:
		pick = "<:2082_Netherite_pickaxe:939195859910934568>"

	if arg == None:
		emb = nextcord.Embed(title='Крафт', description=f'Инструмент: {pick}\n\n<:4065_Wood_Pick:939195859801870387> wood - 250 <:8343oaklog:939195860422623252>\n\n<:2465stonepickaxe:939195860124860487> stone - 500 <:6939cobblestone:939195860456210502>\n\n<:irnpic:939223290105454632> iron - 750 <:1532iron:939195860317773856>\n\n<:1153goldpickaxe:939195860007415868> gold - 750 <:3621gold:939195860129042452>\n\n<:2898picodediamante:939195860032577577> diamond - 1000 <:8946_diamond:939195860389081119>\n\n<:2082_Netherite_pickaxe:939195859910934568> netherite - 1250 <:2352nether:939195860032573460>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Крафт...', icon_url=client.user.display_avatar)
	elif arg == 'wood':
		cursor1.execute("SELECT wood FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
		data = cursor1.fetchone()
		if data[0] >= 250:
			cursor1.execute("UPDATE users SET wood = wood - 250 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			cursor1.execute("UPDATE users SET pickaxe = 1 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			emb = nextcord.Embed(title='Крафт', description=f'Инструмент скрафчен: <:4065_Wood_Pick:939195859801870387>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
			emb.set_author(name='Крафт...', icon_url=client.user.display_avatar)
		else:
			await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
	elif arg == 'stone':
		cursor1.execute("SELECT cobblestone FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
		data = cursor1.fetchone()
		if data[0] >= 500:
			cursor1.execute("UPDATE users SET cobblestone = cobblestone - 500 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			cursor1.execute("UPDATE users SET pickaxe = 2 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			emb = nextcord.Embed(title='Крафт', description=f'Инструмент скрафчен: <:2465stonepickaxe:939195860124860487>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
			emb.set_author(name='Крафт...', icon_url=client.user.display_avatar)
		else:
			await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
	elif arg == 'iron':
		cursor1.execute("SELECT iron FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
		data = cursor1.fetchone()
		if data[0] >= 750:
			cursor1.execute("UPDATE users SET iron = iron - 750 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			cursor1.execute("UPDATE users SET pickaxe = 3 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			emb = nextcord.Embed(title='Крафт', description=f'Инструмент скрафчен: <:irnpic:939223290105454632>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
			emb.set_author(name='Крафт...', icon_url=client.user.display_avatar)
		else:
			await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
	elif arg == 'gold':
		cursor1.execute("SELECT gold FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
		data = cursor1.fetchone()
		if data[0] >= 750:
			cursor1.execute("UPDATE users SET gold = gold - 750 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			cursor1.execute("UPDATE users SET pickaxe = 4 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			emb = nextcord.Embed(title='Крафт', description=f'Инструмент скрафчен: <:1153goldpickaxe:939195860007415868>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
			emb.set_author(name='Крафт...', icon_url=client.user.display_avatar)
	elif arg == 'diamond':
		cursor1.execute("SELECT diamonds FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
		data = cursor1.fetchone()
		if data[0] >= 1000:
			cursor1.execute("UPDATE users SET diamonds = diamonds - 1000 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			cursor1.execute("UPDATE users SET pickaxe = 5 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			emb = nextcord.Embed(title='Крафт', description=f'Инструмент скрафчен: <:2898picodediamante:939195860032577577>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
			emb.set_author(name='Крафт...', icon_url=client.user.display_avatar)
	elif arg == 'netherite':
		cursor1.execute("SELECT netherite FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
		data = cursor1.fetchone()
		if data[0] >= 1250:
			cursor1.execute("UPDATE users SET netherite = netherite - 1250 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			cursor1.execute("UPDATE users SET pickaxe = 6 WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			emb = nextcord.Embed(title='Крафт', description=f'Инструмент скрафчен: <:2082_Netherite_pickaxe:939195859910934568>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
			emb.set_author(name='Крафт...', icon_url=client.user.display_avatar)
		else:
			await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
	else:
		emb = nextcord.Embed(title='Крафт', description=f'Инструмент: {pick}\n\n<:4065_Wood_Pick:939195859801870387> wood - 250 <:8343oaklog:939195860422623252>\n\n<:2465stonepickaxe:939195860124860487> stone - 500 <:6939cobblestone:939195860456210502>\n\n<:irnpic:939223290105454632> iron - 750 <:1532iron:939195860317773856>\n\n<:1153goldpickaxe:939195860007415868> gold - 750 <:3621gold:939195860129042452>\n\n<:2898picodediamante:939195860032577577> diamond - 1000 <:8946_diamond:939195860389081119>\n\n<:2082_Netherite_pickaxe:939195859910934568> netherite - 1250 <:2352nether:939195860032573460>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Крафт...', icon_url=client.user.display_avatar)
	await ctx.send(embed=emb)
	connection1.commit()

@client.command(aliases=['переплавить'])
async def furn(ctx, res: str=None, amount: int=None):
	if res == 'iron':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT iron_ore FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			cursor1.execute("SELECT coal FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data8 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько железа.")
			else:
				if data8[0] < amount * 8:
					return await ctx.send(f"{ctx.author.mention}, недостаточно угля.")
				else:
					cursor1.execute("UPDATE users SET iron = iron + ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
					cursor1.execute("UPDATE users SET iron_ore = iron_ore - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
					cursor1.execute("UPDATE users SET coal = coal - ? WHERE user_id = ? AND guild_id = ?", (amount*8, ctx.author.id, ctx.guild.id,))

					emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

					emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb1.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

					emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb2.add_field(name='Вы переплавили:', value=f'**{amount}** <:unnamed:939195859919331428> , вам понадобилось **{amount*8}** <:9359_MCcoal:939195859894169600>')
					emb2.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

					msg = await ctx.send(embed=emb)
					await asyncio.sleep(1)
					await msg.edit(embed=emb1)
					await asyncio.sleep(1)
					await msg.edit(embed=emb2)
	elif res == 'gold':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT gold_ore FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			cursor1.execute("SELECT coal FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data8 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько золота.")
			else:
				if data8[0] < amount * 12:
					return await ctx.send(f"{ctx.author.mention}, недостаточно угля.")
				else:
					cursor1.execute("UPDATE users SET gold = gold + ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
					cursor1.execute("UPDATE users SET gold_ore = gold_ore - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
					cursor1.execute("UPDATE users SET coal = coal - ? WHERE user_id = ? AND guild_id = ?", (amount*12, ctx.author.id, ctx.guild.id,))

					emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

					emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb1.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

					emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb2.add_field(name='Вы переплавили:', value=f'**{amount}** <:gold_ore:939195859747356692> , вам понадобилось **{amount*12}** <:9359_MCcoal:939195859894169600>')
					emb2.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

					msg = await ctx.send(embed=emb)
					await asyncio.sleep(1)
					await msg.edit(embed=emb1)
					await asyncio.sleep(1)
					await msg.edit(embed=emb2)
	elif res == 'debris':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT debris_ore FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			cursor1.execute("SELECT coal FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data8 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько обломков.")
			else:
				if data8[0] < amount * 20:
					return await ctx.send(f"{ctx.author.mention}, недостаточно угля.")
				else:
					cursor1.execute("UPDATE users SET netherite = netherite + ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
					cursor1.execute("UPDATE users SET debris_ore = debris_ore - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
					cursor1.execute("UPDATE users SET coal = coal - ? WHERE user_id = ? AND guild_id = ?", (amount*20, ctx.author.id, ctx.guild.id,))

					emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

					emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb1.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

					emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
					emb2.add_field(name='Вы переплавили:', value=f'**{amount}** <:Ancient_Debris_top_texture_JE1_B:939195860317798480> , вам понадобилось **{amount*20}** <:9359_MCcoal:939195859894169600>')
					emb2.set_author(name='Переплавляем...', icon_url=client.user.display_avatar)
					emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

					msg = await ctx.send(embed=emb)
					await asyncio.sleep(1)
					await msg.edit(embed=emb1)
					await asyncio.sleep(1)
					await msg.edit(embed=emb2)
	else:	
		emb = nextcord.Embed(title='Переплавка', description=f'<:unnamed:939195859919331428> iron (1) - 8 <:9359_MCcoal:939195859894169600>\n\n<:gold_ore:939195859747356692> gold (1) - 12 <:9359_MCcoal:939195859894169600>\n\n<:Ancient_Debris_top_texture_JE1_B:939195860317798480> debris (1) - 20 <:9359_MCcoal:939195859894169600>', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Переплавка...', icon_url=client.user.display_avatar)
		await ctx.send(embed=emb)
	connection1.commit()

@client.command(aliases=['конверт'])
async def convert(ctx, res: str=None, amount: int=None):
	if res == 'iron':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT iron FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько железа.")
			else:
				cursor1.execute("UPDATE users SET iron = iron - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
				cursor1.execute("UPDATE users SET coins = coins + ? WHERE user_id = ? AND guild_id = ?", (amount*4, ctx.author.id, ctx.guild.id,))

				emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

				emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb1.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

				emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb2.add_field(name='Вы получили:', value=f'**{amount*4}** :coin: , вам понадобилось **{amount}** <:1532iron:939195860317773856>')
				emb2.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

				msg = await ctx.send(embed=emb)
				await asyncio.sleep(1)
				await msg.edit(embed=emb1)
				await asyncio.sleep(1)
				await msg.edit(embed=emb2)
	elif res == 'gold':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT gold FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько золота.")
			else:
				cursor1.execute("UPDATE users SET gold = gold - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
				cursor1.execute("UPDATE users SET coins = coins + ? WHERE user_id = ? AND guild_id = ?", (amount*4, ctx.author.id, ctx.guild.id,))

				emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

				emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb1.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

				emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb2.add_field(name='Вы получили:', value=f'**{amount*4}** :coin: , вам понадобилось **{amount}** <:3621gold:939195860129042452>')
				emb2.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

				msg = await ctx.send(embed=emb)
				await asyncio.sleep(1)
				await msg.edit(embed=emb1)
				await asyncio.sleep(1)
				await msg.edit(embed=emb2)
	elif res == 'cobblestone':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT cobblestone FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько булыжника.")
			else:
				cursor1.execute("UPDATE users SET cobblestone = cobblestone - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
				cursor1.execute("UPDATE users SET coins = coins + ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))

				emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

				emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb1.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

				emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb2.add_field(name='Вы получили:', value=f'**{amount}** :coin: , вам понадобилось **{amount}** <:6939cobblestone:939195860456210502>')
				emb2.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

				msg = await ctx.send(embed=emb)
				await asyncio.sleep(1)
				await msg.edit(embed=emb1)
				await asyncio.sleep(1)
				await msg.edit(embed=emb2)
	elif res == 'netherrack':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT netherack FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько адского камня.")
			else:
				cursor1.execute("UPDATE users SET netherack = netherack - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
				cursor1.execute("UPDATE users SET coins = coins + ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))

				emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

				emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb1.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

				emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb2.add_field(name='Вы получили:', value=f'**{amount}** :coin: , вам понадобилось **{amount}** <:8159netherrack:939195860653334618>')
				emb2.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

				msg = await ctx.send(embed=emb)
				await asyncio.sleep(1)
				await msg.edit(embed=emb1)
				await asyncio.sleep(1)
				await msg.edit(embed=emb2)
	elif res == 'diamonds':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT diamonds FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько алмазов.")
			else:
				cursor1.execute("UPDATE users SET diamonds = diamonds - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
				cursor1.execute("UPDATE users SET coins = coins + ? WHERE user_id = ? AND guild_id = ?", (amount*8, ctx.author.id, ctx.guild.id,))

				emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

				emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb1.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

				emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb2.add_field(name='Вы получили:', value=f'**{amount*8}** :coin: , вам понадобилось **{amount}** <:8946_diamond:939195860389081119>')
				emb2.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

				msg = await ctx.send(embed=emb)
				await asyncio.sleep(1)
				await msg.edit(embed=emb1)
				await asyncio.sleep(1)
				await msg.edit(embed=emb2)
	elif res == 'netherite':
		if not amount or amount <= 0:
			await ctx.send(f'{ctx.author.mention}, укажите число!')
		else:
			cursor1.execute("SELECT netherite FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
			data3 = cursor1.fetchone()
			if data3[0] < amount:
				return await ctx.send(f"{ctx.author.mention}, у вас нет столько незерита.")
			else:
				cursor1.execute("UPDATE users SET netherite = netherite - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
				cursor1.execute("UPDATE users SET coins = coins + ? WHERE user_id = ? AND guild_id = ?", (amount*12, ctx.author.id, ctx.guild.id,))

				emb = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775581413386/1.png')

				emb1 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb1.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb1.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775753383966/2.png')

				emb2 = nextcord.Embed(title=ctx.author, color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
				emb2.add_field(name='Вы получили:', value=f'**{amount*12}** :coin: , вам понадобилось **{amount}** <:2352nether:939195860032573460>')
				emb2.set_author(name='Конвертируем...', icon_url=client.user.display_avatar)
				emb2.set_image(url='https://cdn.discordapp.com/attachments/934423919874670643/939438775916969984/3.png')

				msg = await ctx.send(embed=emb)
				await asyncio.sleep(1)
				await msg.edit(embed=emb1)
				await asyncio.sleep(1)
				await msg.edit(embed=emb2)
	else:	
		emb = nextcord.Embed(title='Конвертирование', description=f'<:1532iron:939195860317773856> iron (1) - 4 :coin:\n<:3621gold:939195860129042452> gold (1) - 4 :coin:\n<:6939cobblestone:939195860456210502> cobblestone (1) - 1 :coin:\n<:8159netherrack:939195860653334618> netherrack (1) - 1 :coin:\n<:8946_diamond:939195860389081119> diamonds (1) - 8 :coin:\n<:2352nether:939195860032573460> netherite (1) - 12 :coin:', color=nextcord.Color.blurple(), timestamp=ctx.message.created_at)
		emb.set_author(name='Конвертирование...', icon_url=client.user.display_avatar)
		await ctx.send(embed=emb)
	connection1.commit()

@client.command(aliases = ['coinsend', 'м-отправить'])
async def __coinsend(ctx, member: nextcord.Member = None, amount: int = None):
	cursor1.execute("SELECT coins FROM users WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id,))
	datac = cursor1.fetchone()
	if member is None:
		await ctx.send(f'{ctx.author.mention}, укажите пользователя, которому хотите перекинуть деньги!')
	else:
		if amount is None:
			return await ctx.send(f'{ctx.author.mention}, укажите сумму!')
		elif amount < 1:
			return await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
		if datac[0] < amount:
			return await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
		else:
			cursor1.execute("UPDATE users SET coins = coins + ? WHERE user_id = ? AND guild_id = ?", (amount, member.id, ctx.guild.id,))
			cursor1.execute("UPDATE users SET coins = coins - ? WHERE user_id = ? AND guild_id = ?", (amount, ctx.author.id, ctx.guild.id,))
			connection1.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@client.command(aliases=['leaders', 'лидеры'])
async def __fleader(ctx):
	embed = nextcord.Embed(title='Топ 12 богачей на этом сервере!', colour=nextcord.Colour.blurple())
	embed.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	counter = 0

	for row in cursor1.execute("SELECT name, coins FROM users WHERE guild_id = ? ORDER BY coins DESC LIMIT 12", (ctx.guild.id,)):
		counter += 1
		embed.add_field(name=f'# {counter} | {row[0]}', value=f'Баланс: {row[1]} :coin:')
	await ctx.send(embed=embed)

@client.group(name='oreshop', invoke_without_command=True, aliases=['м-магазин'])

async def __oreshop(ctx):
	e = nextcord.Embed(title='Магазин ролей', timestamp=ctx.message.created_at, color=nextcord.Color.blurple())
	e.set_author(name=client.user.name, icon_url=client.user.display_avatar)
	e.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
	cursor1.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id))
	data = cursor1.fetchone()

	if data:
		for row in cursor1.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
			if ctx.guild.get_role(row[0]) != None:
				e.add_field(name = f"Стоимость: {row[1]} :coin:", value=f"Вы приобретете роль: {ctx.guild.get_role(row[0]).mention}\n`Если вы не можете упомянуть роль, напишите:\nore!shop buy <@&{ctx.guild.get_role(row[0]).id}>`", inline=False)
			else:
				pass

		await ctx.send(embed=e)
	if not data:
		await ctx.send('Магазин пуст.')

@__oreshop.command(aliases=['add', 'добавить'])

@commands.has_permissions( administrator = True )
async def __ashop(ctx, role: nextcord.Role = None, cost: int = None):
	if role is None:
		await ctx.send(f'{ctx.author.mention}, укажите роль!')
	else:
		if cost is None:
			await ctx.send(f'{ctx.author.mention}, укажите цену!')
		elif cost < 0:
			await ctx.send(f'{ctx.author.mention}, нельзя указывать сумму ниже 0!')
		else:
			cursor1.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
			connection1.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@__oreshop.command(aliases=['remove', 'убрать'])

@commands.has_permissions( administrator = True )
async def __rshop(ctx, role: nextcord.Role = None):
	if role is None:
		await ctx.send(f'{ctx.author.mention}, укажите роль!')
	else:
		cursor1.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
		connection1.commit()

		await ctx.message.add_reaction('<a:checkon:928259275090972772>')

@__oreshop.command(aliases=['buy', 'купить'])

async def __buy(ctx, role: nextcord.Role = None):
	if role is None:
		await ctx.send(f'{ctx.author.mention}, укажите роль!')
	else:
		if role in ctx.author.roles:
			await ctx.send('У вас уже есть эта роль!')
		elif cursor1.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor1.execute("SELECT coins FROM users WHERE user_id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0]:
			await ctx.send(f'{ctx.author.mention}, недостаточно средств!')
		else:
			await ctx.author.add_roles(role)
			cursor1.execute("UPDATE users SET coins = coins - {} WHERE user_id = {} AND guild_id = {}".format(cursor1.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id, ctx.guild.id))
			connection1.commit()

			await ctx.message.add_reaction('<a:checkon:928259275090972772>')

#Коги
for e in [f for f in os.listdir('cogs') if f.endswith('.py')]:
	try:
		client.load_extension(f'cogs.{e.replace(".py", "")}')
		print (f'Ког {e} загружен!')
	except Exception as error:
		print(f'{e} Ошибка!.\n{error}')

print('Коги успешно загружены!')

# Запуск Бота
token = open('token.txt', 'r').readline()
client.run(token)