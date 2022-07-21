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

class TagSys(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.group(invoke_without_command=True, aliases=['тэг'])
	async def tag(self, ctx, name):
		db = sqlite3.connect('tag.db')
		cursor = db.cursor()
		cursor.execute("SELECT name, content, emb_name FROM tags WHERE name = ? AND guild_id = ?", (name, ctx.guild.id,))
		data = cursor.fetchone()
		if data:
			emb = nextcord.Embed(title=f'{str(data[2])}', description=f'{str(data[1])}')
			emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
			await ctx.send(embed=emb)
		if not data:
			await ctx.send('Такого тэга нет!')

	@tag.command(aliases=['добавить'])
	@commands.has_permissions(administrator=True)
	async def add(self, ctx, name, emb_name, *, content):
		db = sqlite3.connect('tag.db')
		cursor = db.cursor()
		cursor.execute("SELECT name FROM tags WHERE name = ? AND guild_id = ?", (name, ctx.guild.id,))
		data = cursor.fetchone()
		if data:
			await ctx.send('Такой тэг уже существует!')
		else:
			cursor.execute("INSERT INTO tags VALUES(?,?,?,?)", (name, emb_name, content, ctx.guild.id,))
			await ctx.send(f'Тэг {name} был добавлен успешно!')
		db.commit()
		cursor.close()
		db.close()

	@tag.command(aliases=['убрать'])
	@commands.has_permissions(administrator=True)
	async def remove(self, ctx, name):
		db = sqlite3.connect('tag.db')
		cursor = db.cursor()
		cursor.execute("SELECT name FROM tags WHERE name = ? AND guild_id = ?", (name, ctx.guild.id,))
		data = cursor.fetchone()
		if not data:
			await ctx.send('Такого тэга не существует!')
		else:
			cursor.execute("DELETE FROM tags WHERE name = ? AND guild_id = ?", (name, ctx.guild.id,))
			await ctx.send(f'Тэг {name} был удалён успешно!')
		db.commit()
		cursor.close()
		db.close()

	@tag.command(aliases=['список'])
	async def list(self, ctx):
		db = sqlite3.connect('tag.db')
		cursor = db.cursor()
		cursor.execute("SELECT name FROM tags WHERE guild_id = ?", (ctx.guild.id,))
		data = cursor.fetchone()
		try:
			e = nextcord.Embed(title=f'Тэги на этом сервере', timestamp=ctx.message.created_at)
			e.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			e.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
			for row in cursor.execute("SELECT name FROM tags WHERE guild_id = ?", (ctx.guild.id,)):
				e.add_field(name = f"Тэг", value=f"Команда: {str(row[0])}", inline=False)
			await ctx.send(embed=e)
		except:
			await ctx.send(embed=nextcord.Embed(title='Тэги на этом сервере', description='Тэгов нет или их слишком много!'))
	
def setup(client):
	client.add_cog(TagSys(client))