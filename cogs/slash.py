# Настройка
import nextcord
import typing
import asyncio
import json
import requests
import random
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
import datetime
from modules.components import *
from utils import default

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class SlashCommands(commands.Cog, name ="Слэш-команды"):
	def __init__(self,client):
		self.client = client

	testingServerID = [919153490025148417, 917783767869980753]

	@nextcord.slash_command(description='Вывести аватарку пользователя')
	async def avatar(self, interaction:Interaction , member: nextcord.Member=None):
		if member == None:
			member = interaction.user

		icon_url = member.display_avatar
		avatarEmbed = nextcord.Embed(title = f"<a:checkon:928259275090972772> Аватарка {member.name}", color=0x2F3136)
		avatarEmbed.set_image(url = f"{icon_url}")
		avatarEmbed.timestamp = datetime.datetime.now()
		avatarEmbed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		avatarEmbed.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
		await interaction.response.send_message(embed = avatarEmbed)

	@nextcord.slash_command(description='Магический шар!')
	async def eightball(self, interaction:Interaction, *, question):
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
		emb = nextcord.Embed(title='Магический шар!', timestamp=datetime.datetime.now(), color=0x2F3136)
		emb.add_field(name='Вопрос:', value=f'{question}', inline=False)
		emb.add_field(name='Ответ:', value=f'{random.choice(responses)}')
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		emb.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
		await interaction.response.send_message(embed=emb)

	@nextcord.slash_command(description="Показывает скорость отклика бота",guild_ids=testingServerID)
	async def ping(self, interaction: Interaction):
		embed=nextcord.Embed(title='Пинг!', description=f'<a:checkon:928259275090972772> Мой пинг: {round(self.client.latency*1000)}мс', color=0x2F3136, timestamp=datetime.datetime.now())
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embed.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
		await interaction.response.send_message(embed=embed)

	@nextcord.slash_command(description="Сменить префикс бота на сервере")
	async def setprefix(self, interaction:Interaction, prefix=None):
		if (not interaction.user.guild_permissions.manage_channels):
				await interaction.response.send_message('<a:checkoff:928259276273758208> Недостаточно прав!')
				return

		if prefix is None:
			return await interaction.response.send_message('Нельзя указывать пустоту, если вы хотите префикс с пробелом, напишите текст в кавычках.. пример: ?setprefix "leafy "')

		cursor.execute("SELECT prefix FROM prefixes WHERE id = ?", (interaction.user.guild.id,))
		data = cursor.fetchone()
		if data:
			cursor.execute("UPDATE prefixes SET prefix = ? WHERE id = ?", (prefix, interaction.user.guild.id,))
			await interaction.response.send_message(f'<a:checkon:928259275090972772> Префикс бота изменён на `{prefix}`')
		else:
			cursor.execute("INSERT INTO prefixes (prefix, id) VALUES (?, ?)", ('?', interaction.user.guild.id,))
			cursor.execute("SELECT prefix FROM prefixes WHERE id = ?", (interaction.user.guild.id,))
			data = cursor.fetchone()
			if data:
				cursor.execute("UPDATE prefixes SET prefix = ? WHERE id = ?", (prefix, interaction.user.guild.id,))
				await interaction.response.send_message(f'<a:checkon:928259275090972772> Префикс бота изменён на `{prefix}`')
			else:
				return

		connection.commit()

	@nextcord.slash_command(description="Привет!")
	async def hello(self, interaction:Interaction):
		author = interaction.user
		await interaction.response.send_message(f'Привет, {author.mention}')

	@nextcord.slash_command(description="Информация о текущем сервере")
	async def server(self, interaction: Interaction):
		verify = ""
		if interaction.user.guild.verification_level == nextcord.VerificationLevel.low:
			verify = "Низкий"
		elif interaction.user.guild.verification_level == nextcord.VerificationLevel.medium:
			verify = "Средний"
		elif interaction.user.guild.verification_level == nextcord.VerificationLevel.high:
			verify = "Высокий"
		elif interaction.user.guild.verification_level == nextcord.VerificationLevel.highest:
			verify = "Очень высокий"
		elif interaction.user.guild.verification_level == nextcord.VerificationLevel.none:
			verify = "Отсутствует"

		offlinecounter = 0
		dndcounter = 0
		idlecounter = 0
		onlinecounter = 0
		invisiblecounter = 0

		textcounter = 0
		voicecounter = 0
		categorycounter = 0

		for member in interaction.user.guild.members:
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

		for channel in interaction.user.guild.channels:
			if channel.type == ChannelType.text:
				textcounter += 1
			elif channel.type == ChannelType.voice:
				voicecounter += 1
			elif channel.type == ChannelType.category:
				categorycounter += 1

		owner = interaction.user.guild.owner
		role_count = len(interaction.user.guild.roles)
		if interaction.user.guild.icon:
			embed = nextcord.Embed(timestamp=datetime.datetime.now(), color=0x2F3136)
			embed.add_field(name='Название:', value=f'`{interaction.user.guild.name}`', inline = False)
			embed.add_field(name='Владелец:', value=f'{owner.mention}', inline = False)
			embed.add_field(name='Участников:', value=f'`{interaction.user.guild.member_count}`', inline = False)
			embed.add_field(name='Уровень верификации:', value=str(verify), inline = False)
			embed.add_field(name='Высшая роль:', value=f'`{interaction.user.guild.roles[-2]}`', inline = False)
			embed.add_field(name='Ролей:', value=f'`{str(role_count)}`', inline = False)
			embed.add_field(name='Создан:', value=default.date(interaction.user.guild.created_at, ago=True), inline = False)
			embed.add_field(name='Сортировка по статусам:', value=f'<:1415online:926414278322442270> В сети: `{onlinecounter + idlecounter + dndcounter}`\n<:5251onlinestatus:926412397047070730> Онлайн: `{onlinecounter}`\n<:4572discordidle:926414279861743646> Неактивен: `{idlecounter}`\n<:5163dndstatus:926412396816388166> Не беспокоить: `{dndcounter}`\n<:2179offlinestatus:926412396589899787> Не в сети: `{offlinecounter}`', inline=False)
			embed.add_field(name='Каналов:', value=f'📜 Всего каналов: `{textcounter + voicecounter}`\n💬 Текстовых: `{textcounter}`\n🔊 Голосовых: `{voicecounter}`\n🌀 Категорий: `{categorycounter}`')
			embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			embed.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
			embed.set_thumbnail(url=interaction.user.guild.icon.url)
		else:
			embed = nextcord.Embed(timestamp=datetime.datetime.now(), color=0x2F3136)
			embed.add_field(name='Название:', value=f'`{interaction.user.guild.name}`', inline = False)
			embed.add_field(name='Владелец:', value=f'{owner.mention}', inline = False)
			embed.add_field(name='Участников:', value=f'`{interaction.user.guild.member_count}`', inline = False)
			embed.add_field(name='Уровень верификации:', value=str(verify), inline = False)
			embed.add_field(name='Высшая роль:', value=f'`{interaction.user.guild.roles[-2]}`', inline = False)
			embed.add_field(name='Ролей:', value=f'`{str(role_count)}`', inline = False)
			embed.add_field(name='Создан:', value=default.date(interaction.user.guild.created_at, ago=True), inline = False)
			embed.add_field(name='Сортировка по статусам:', value=f'<:1415online:926414278322442270> В сети: `{onlinecounter + idlecounter + dndcounter}`\n<:5251onlinestatus:926412397047070730> Онлайн: `{onlinecounter}`\n<:4572discordidle:926414279861743646> Неактивен: `{idlecounter}`\n<:5163dndstatus:926412396816388166> Не беспокоить: `{dndcounter}`\n<:2179offlinestatus:926412396589899787> Не в сети: `{offlinecounter}`', inline=False)
			embed.add_field(name='Каналов:', value=f'📜 Всего каналов: `{textcounter + voicecounter}`\n💬 Текстовых: `{textcounter}`\n🔊 Голосовых: `{voicecounter}`\n🌀 Категорий: `{categorycounter}`')
			embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			embed.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
		await interaction.response.send_message(embed=embed)

	@nextcord.slash_command(description='Информация о пользователе')
	async def user(self, interaction: Interaction ,user:nextcord.Member):
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
			embed = nextcord.Embed(color=0x2F3136, timestamp=datetime.datetime.now())
			embed.set_author(name=f"<a:checkon:928259275090972772> Информация о: - {user}"),
			embed.set_thumbnail(url=user.display_avatar),
			embed.set_footer(text=f'{interaction.user}',
				icon_url=interaction.user.display_avatar)
			embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			embed.add_field(name='ID:',value=user.id,inline=False)
			embed.add_field(name='Имя:',value=user.display_name,inline=False)
			embed.add_field(name='Аккаунт создан:',value=default.date(user.created_at, ago=True),inline=False)
			embed.add_field(name='Вошел на сервер:',value=default.date(user.joined_at, ago=True),inline=False)
			embed.add_field(name='Бот',value=isbot,inline=False)
			await interaction.response.send_message(embed=embed)
		else:
			embed = nextcord.Embed(description='Количество отображаемых ролей снижено до 15!', color=0x2F3136, timestamp=datetime.datetime.now())
			embed.set_author(name=f"<a:checkon:928259275090972772> Информация о: - {user}"),
			embed.set_thumbnail(url=user.display_avatar),
			embed.set_footer(text=f'{interaction.user}',
				icon_url=interaction.user.display_avatar)
			embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			embed.add_field(name='ID:',value=user.id,inline=False)
			embed.add_field(name='Имя:',value=user.display_name,inline=False)
			embed.add_field(name='Аккаунт создан:',value=default.date(user.created_at, ago=True),inline=False)
			embed.add_field(name='Вошел на сервер:',value=default.date(user.joined_at, ago=True),inline=False)
			embed.add_field(name='Бот',value=isbot,inline=False)
			embed.add_field(name=f'Роли: ({len(rlist)})',value=''.join([b]),inline=False)
			embed.add_field(name='Высшая роль:',value=user.top_role.mention,inline=False)
			await interaction.response.send_message(embed=embed)

	@nextcord.slash_command(description="Тест кнопок...",guild_ids=testingServerID)
	async def buttontest(self, interaction: Interaction):
		view = TestCommand(user=interaction.user.id)
		await interaction.response.send_message('Вы подтверждаете какое-либо действие?', view=view)

	@nextcord.slash_command(description="Создать вложение")
	async def embed(self, interaction:Interaction, title, description):
		embed = nextcord.Embed(title=title, description=description, color=0x2F3136, timestamp=datetime.datetime.now())
		embed.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
		await interaction.response.send_message(embed=embed)

	@nextcord.slash_command(description="Never Gonna Give You Up!")
	async def rickroll(self, interaction:Interaction):
	    embed=nextcord.Embed(title="Ты зарикроллен!", url="", description="**Рик Эстли станцует для тебя!**", color=0x2F3136)
	    embed.set_image(url="https://c.tenor.com/u9XnPveDa9AAAAAM/rick-rickroll.gif")
	    await interaction.response.send_message(embed=embed)

	@nextcord.slash_command(description="Рандомный мем с Reddit!")
	async def meme(self, interaction:Interaction):
		embed = nextcord.Embed(title="", description="", color=0x2F3136)
		async with aiohttp.ClientSession() as cs:
			async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
				res = await r.json()
				embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
				await interaction.response.send_message(embed=embed)

	@nextcord.slash_command(description="Рандомная лисичка с Reddit!")
	async def fox(self, interaction:Interaction):
		embed = nextcord.Embed(title="", description="", color=0x2F3136)
		async with aiohttp.ClientSession() as cs:
			async with cs.get('https://www.reddit.com/r/foxes/new.json?sort=foxes') as r:
				res = await r.json()
				embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
				await interaction.response.send_message(embed=embed)

	@nextcord.slash_command(description="Поиск видео с YouTube")
	async def yt(self, interaction:Interaction, *, search):
	    query_string = urllib.parse.urlencode({
	        "search_query": search
	    })
	    html_content = urllib.request.urlopen(
	        "http://www.youtube.com/results?" + query_string
	    )
	    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
	    await interaction.response.send_message("http://www.youtube.com/watch?v=" + search_results[0])

	@nextcord.slash_command(description="Пригласить меня на сервер!")
	async def invite(self, interaction:Interaction):
		emb = nextcord.Embed(title='<a:checkon:928259275090972772> Пригласить меня на сервер!', description=f'[Нажми сюда, чтобы пригласить меня!](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=applications.commands%20bot)', color=nextcord.Colour.from_rgb(255,255,255), timestamp=datetime.datetime.now())
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		emb.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
		emb.set_thumbnail(url=self.client.user.display_avatar)
		await interaction.response.send_message(embed=emb, ephemeral=True)

	@nextcord.slash_command(description="Установить медленный режим в канале")
	async def slow(self, interaction:Interaction, time: int):
		if (not interaction.user.guild_permissions.manage_channels):
			await interaction.response.send_message('<a:checkoff:928259276273758208> Недостаточно прав!', ephemeral=True)
			return
		try:
			if time == 0:
				await interaction.response.send_message('<a:checkon:928259275090972772> Медленный режим выключен!')
				await interaction.channel.edit(slowmode_delay=0)
			elif time > 21600:
				await interaction.response.send_message('<a:checkoff:928259276273758208> Вы не можете устанавливать время больше 6-ти часов!')
				return
			else:
				await interaction.channel.edit(slowmode_delay=time)
				await interaction.response.send_message(f'<a:checkon:928259275090972772> Вы установили медленный режим на {time} секунд!')
		except Exception:
			print('Упс!')

	@nextcord.slash_command(description="Украсть эмоджи с другого сервера")
	async def esteal(self,interaction:Interaction, url:str, *, name):
		guild = interaction.user.guild
		if interaction.user.guild_permissions.administrator:
			async with aiohttp.ClientSession() as ses:
				async with ses.get(url) as r:
					try:
						imgOrGif = BytesIO(await r.read())
						bValue = imgOrGif.getvalue()
						if r.status in range(200, 299):
							emoji = await guild.create_custom_emoji(image=bValue, name=name)
							await interaction.response.send_message('<a:checkon:928259275090972772> Эмоджи добавлено!')
							await ses.close()
						else:
							await interaction.response.send_message(f'({r.status}) Ошибка что-ли ._.')
					except nextcord.HTTPExeption:
						await interaction.response.send_message('Короче ты нуб, ничего не работает')
		else:
			return await interaction.response.send_message('<a:checkoff:928259276273758208> Недостаточно прав!', ephemeral=True)


	@nextcord.slash_command(description="Создать опрос")
	async def poll(self,interaction:Interaction,*,message):
		if interaction.user.guild_permissions.manage_nicknames:
			emb=nextcord.Embed(title="Опрос!", description=f"{message}", color=0x2F3136, timestamp=datetime.datetime.now())
			emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			emb.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
			msg=await interaction.channel.send(embed=emb)
			await msg.add_reaction('👍')
			await msg.add_reaction('👎')
			await interaction.response.send_message("Опрос создан!", ephemeral=True)
		else:
			return await interaction.response.send_message('<a:checkoff:928259276273758208> Недостаточно прав!', ephemeral=True)


	@nextcord.slash_command(description="Проверить совместимость двух пользователей")
	async def clove(self, interaction:Interaction, member1: nextcord.Member, member2: nextcord.Member):
		embed = nextcord.Embed(title='❤️ Совместимость!', description=f'💝 {member1.mention} и {member2.mention} совместимы на {random.randint(0,100)}%', colour=nextcord.Colour.red(), timestamp = datetime.datetime.now())
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embed.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
		await interaction.response.send_message(embed=embed)

	@nextcord.slash_command(description="Подбросить монетку (орёл/решка)")
	async def coin(self,interaction:Interaction, bet):
		resp = ['выпал орёл!', 'выпала решка!'] 
		if bet == 'орёл':
			await interaction.response.send_message(embed=nextcord.Embed(title='Подбрасываю монетку...', description=f'{interaction.user.mention}, {random.choice(resp)}\nВы поставили на: `орёл`'))
		elif bet == 'решка':
			await interaction.response.send_message(embed=nextcord.Embed(title="Подбрасываю монетку...", description=f"{interaction.user.mention}, {random.choice(resp)}\nВы поставили на: `решка`"))
		else:
			return await interaction.response.send_message("<a:checkoff:928259276273758208> Напишите орёл либо решка!", ephemeral=True)

	@nextcord.slash_command(description="Бросить кости")
	async def roll(self, interaction:Interaction):
		await interaction.response.send_message(f':game_die: {interaction.user.mention} бросил кости!\n:game_die: Выпало: **{random.randint(1,6)}**')

	@nextcord.slash_command(description="Информация о настройках сервера")
	async def info(self, interaction: Interaction):
		dbhelp = sqlite3.connect('server.db')
		cursorhelp = dbhelp.cursor()
		cursorhelp.execute("SELECT prefix FROM prefixes WHERE id = ?", (interaction.user.guild.id,))
		resulthelp = cursorhelp.fetchone()
		db1 = sqlite3.connect("levellog.db")
		cursor1 = db1.cursor()
		cursor1.execute("SELECT channel_log FROM log WHERE guild_log = ?", (interaction.user.guild.id,))
		result1 = cursor1.fetchone()

		db3 = sqlite3.connect('welcome.db')
		cursor3 = db3.cursor()
		cursor3.execute(f"SELECT channel_id_h FROM welcome WHERE guild_id = {interaction.user.guild.id}")
		result3 =  cursor3.fetchone()
		db4 = sqlite3.connect('welcome.db')
		cursor4 = db4.cursor()
		cursor4.execute(f"SELECT channel_id_b FROM welcome WHERE guild_id = {interaction.user.guild.id}")
		result4 =  cursor4.fetchone()
		leveldb = sqlite3.connect("levellog.db")
		lvlcursor = leveldb.cursor()
		lvlcursor.execute("SELECT disabled_id FROM disable WHERE disabled_id = ?", (interaction.user.guild.id,))
		lvlresult = lvlcursor.fetchone()
		db5 = sqlite3.connect('generator.db')
		cursor5 = db5.cursor()
		cursor5.execute("SELECT id FROM enabled WHERE id = ?", (interaction.user.guild.id,))
		data5 = cursor5.fetchone()

		p = str(resulthelp[0])
		embed = nextcord.Embed(title="Бот на этом сервере", description=f'**{p}help** | Меню помощи\n**{p}invite** | Пригласить меня\n**Сайт** | [Жми сюда](https://www.leafy.cf)\n[Сервер поддержки](https://discord.gg/CT8VekA57Z)', color=0x2F3136)
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embed.set_footer(text=interaction.user.guild.name, icon_url=interaction.user.display_avatar)
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
		await interaction.response.send_message(embed=embed)

		

def setup(client):
	client.add_cog(SlashCommands(client))