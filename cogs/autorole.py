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

class Autoroles(commands.Cog, name ="Autoroles Guild"):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_member_join(self, member):
		db = sqlite3.connect("autoroles.db")
		cursor = db.cursor()
		try:
			for row in cursor.execute("SELECT role_name FROM roles WHERE guild_id = ?", (member.guild.id,)):
				role = nextcord.utils.get(member.guild.roles, name=f"{str(row[0])}")
				await member.add_roles(role)
		except:
			pass

	@commands.group(invoke_without_command=True, aliases = ['авто-роль'])
	@commands.has_permissions(administrator=True)
	async def autorole(self, ctx):
		db = sqlite3.connect("autoroles.db")
		cursor = db.cursor()
		cursor.execute("SELECT role_name FROM roles WHERE guild_id = ?", (ctx.guild.id,))
		data = cursor.fetchone()
		role = ctx.guild.get_role(data)
		if data:
			emb = nextcord.Embed(title="Авто-роли", description=f"Сейчас установлены роли:", color=0x2F3136)
			for row in cursor.execute("SELECT role_name FROM roles WHERE guild_id = ?", (ctx.guild.id,)):
				emb.add_field(name='Роль:', value=f'**{str(row[0])}**', inline=False)
			await ctx.send(embed=emb)
		else:
			emb = nextcord.Embed(title="Авто-роли", description=f"Сейчас установлены роли:\n**Не установлены**", color=0x2F3136)
			await ctx.send(embed=emb)

	@autorole.command(aliases = ['добавить'])
	@commands.has_permissions(administrator=True)
	async def add(self, ctx, role: nextcord.Role):
		db = sqlite3.connect("autoroles.db")
		cursor = db.cursor()
		cursor.execute("INSERT INTO roles(role_id, guild_id, role_name) VALUES(?, ?, ?)", (role.id, ctx.guild.id, role.name))
		emb = nextcord.Embed(title="Авто-роли", description=f"Вы добавили авто-роль:\n**{role.name}**", color=0x2F3136)
		await ctx.send(embed=emb)
		db.commit()
		cursor.commit()
		cursor.close()
		db.close()

	@autorole.command(aliases = ['убрать'])
	@commands.has_permissions(administrator=True)
	async def reset(self, ctx):
		db = sqlite3.connect("autoroles.db")
		cursor = db.cursor()
		cursor.execute("SELECT role_id FROM roles WHERE guild_id = ?", (ctx.guild.id,))
		data = cursor.fetchone()
		if data:
			cursor.execute("DELETE FROM roles WHERE guild_id = ?", (ctx.guild.id,))
			emb = nextcord.Embed(title="Авто-роли", description=f"Вы очистили авто-роли.", color=0x2F3136)
			await ctx.send(embed=emb)
		else:
			emb = nextcord.Embed(title="Авто-роль", description=f"Авто-роли уже очищены.", color=0x2F3136)
			await ctx.send(embed=emb)
		db.commit()
		cursor.commit()
		cursor.close()
		db.close()

	@commands.Cog.listener()
	async def on_message(self, message):
		ben = '.бен'
		if ben in message.content.lower():
				answers = ['Yes.','No.','Ho-ho-ho.','Eugh.']
				e = nextcord.Embed(title='Мой говорящий Бен!', description='Использование: .бен <вопрос>', color=0x2F3136)
				e.add_field(name='Ваш вопрос:', value=f"**{str(message.content)}**")
				e.add_field(name='Ответ Бена:', value=f"**{random.choice(answers)}**")
				e.set_image(url="https://cdn.discordapp.com/attachments/934423919874670643/947904952569823274/talking-ben-do-mal.gif")
				e.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
				e.set_footer(text=message.author.name, icon_url=message.author.display_avatar)
				await message.channel.send(embed=e)

def setup(client):
	client.add_cog(Autoroles(client))