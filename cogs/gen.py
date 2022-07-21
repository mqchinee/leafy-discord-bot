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
from nextcord import Member
from nextcord.ext.commands import has_permissions, MissingPermissions, cooldown, BucketType
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import psutil

class Generator(commands.Cog, name ="Generate"):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self,message):
		db = sqlite3.connect('generator.db')
		cursor = db.cursor()
		cursor.execute("SELECT id FROM enabled WHERE id = ?", (message.guild.id,))
		data = cursor.fetchone()
		link = 'http'
		link2 = 'discord.gg'
		if data:
			if not message.content.startswith(f"?"):
				if not link in message.content:
					if not link2 in message.content:
						if not message.author.bot:
							tst = [1, 2]
							first = random.choice(tst)
							second = random.choice(tst)
							if first == second:
								db = sqlite3.connect('generator.db')
								cursor = db.cursor()
								cursor.execute("INSERT INTO msg(messages) VALUES(?)", (message.content,))
								db.commit()
								cursor.close()
								db.close()
		if not data:
			return


		db = sqlite3.connect('generator.db')
		cursor = db.cursor()
		cursor.execute("SELECT id FROM enabled WHERE id = ?", (message.guild.id,))
		data = cursor.fetchone()
		if data:
			if message.reference is not None:
				db = sqlite3.connect('generator.db')
				cursor = db.cursor()
				cursor.execute("SELECT messages FROM msg ORDER BY RANDOM() LIMIT 1")
				result1 =  cursor.fetchone()
				await message.channel.send(f"{str(result1[0])}")
		if not data:
			return

	@commands.group(aliases = ['ген'])
	async def gen(self, ctx):
		pass

	@gen.command(aliases = ['включить'])
	
	@commands.has_permissions(administrator=True)
	async def enable(self, ctx):
		db = sqlite3.connect('generator.db')
		cursor = db.cursor()
		cursor.execute("INSERT INTO enabled(id) VALUES(?)", (ctx.guild.id,))
		await ctx.send('Генерация сообщений включена.\n`Что это?`\nТеперь при каждом ответе, бот будет отправлять рандомную фразу, что поможет поднять актив на вашем сервере.')
		db.commit()
		cursor.close()
		db.close()

	@gen.command(aliases = ['выключить'])
	
	@commands.has_permissions(administrator=True)
	async def disable(self, ctx):
		db = sqlite3.connect('generator.db')
		cursor = db.cursor()
		cursor.execute("DELETE FROM enabled WHERE id = ?", (ctx.guild.id,))
		await ctx.send('Генерация сообщений выключена.')
		db.commit()
		cursor.close()
		db.close()

def setup(client):
	client.add_cog(Generator(client))