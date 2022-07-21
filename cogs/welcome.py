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
from easy_pil import Canvas, Editor, Font, Text, font

class Welcome(commands.Cog, name ="Welcome"):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_member_join(self,member):
		db = sqlite3.connect('welcome.db')
		cursor = db.cursor()
		randomhello = ["https://i.pinimg.com/originals/aa/02/43/aa024380afc3587bad3cb6f8adbf1aab.gif","https://i.yapx.ru/Mr2aI.gif","https://78.media.tumblr.com/c7fe775814145d8a59f3629b72802357/tumblr_pc03twL37F1uvobnmo1_540.gif","https://i.imgur.com/1GJjhIy.gif"]
		cursor.execute(f"SELECT channel_id_h FROM welcome WHERE guild_id = {member.guild.id}")
		result =  cursor.fetchone()
		if result is None:
			return
		else:
			if member.guild.icon:
				cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {member.guild.id}")
				result1 =  cursor.fetchone()
				members = len(list(member.guild.members))
				mention = member.mention
				user = member.name
				guild=member.guild
				embed = nextcord.Embed(title="Привет!",description=f"<@{member.id}> присоединился к **{member.guild.name}**\n{str(result1[0])}".format(members=members, mention=mention, user=user, guild=guild))
				embed.set_thumbnail(url=f"{member.display_avatar}")
				embed.set_footer(text=f"Нас теперь: {members}", icon_url=f"{member.display_avatar}")
				embed.set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon.url}")
				embed.set_image(url=random.choice(randomhello))
				channel = self.client.get_channel(int(result[0]))
			else:
				cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {member.guild.id}")
				result1 =  cursor.fetchone()
				members = len(list(member.guild.members))
				mention = member.mention
				user = member.name
				guild=member.guild
				embed = nextcord.Embed(title="Привет!",description=f"<@{member.id}> присоединился к **{member.guild.name}**\n{str(result1[0])}".format(members=members, mention=mention, user=user, guild=guild))
				embed.set_thumbnail(url=f"{member.display_avatar}")
				embed.set_footer(text=f"Нас теперь: {members}", icon_url=f"{member.display_avatar}")
				embed.set_image(url=random.choice(randomhello))
				channel = self.client.get_channel(int(result[0]))
			await channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_remove(self,member):
		db = sqlite3.connect('welcome.db')
		cursor = db.cursor()
		randombye = ["https://data.whicdn.com/images/315441551/original.gif", "https://animesher.com/orig/1/168/1681/16811/animesher.com_sad-watch-leonardo-crying-1681110.gif", "https://i1.wp.com/insiliconjurer.com/wp-content/uploads/2019/06/mobfightgif.gif?resize=540%2C225&ssl=1"]
		cursor.execute(f"SELECT channel_id_b FROM welcome WHERE guild_id = {member.guild.id}")
		result =  cursor.fetchone()
		if member.guild.icon:
			members = len(list(member.guild.members))
			mention = member.mention
			user = member.name
			guild=member.guild
			embed = nextcord.Embed(title="Пока!",description=f"<@{member.id}> покинул **{member.guild.name}**".format(members=members, mention=mention, user=user, guild=guild))
			embed.set_thumbnail(url=f"{member.display_avatar}")
			embed.set_footer(text=f"Нас теперь: {members}", icon_url=f"{member.display_avatar}")
			embed.set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon.url}")
			embed.set_image(url=random.choice(randombye))
			channel = self.client.get_channel(int(result[0]))
		else:
			members = len(list(member.guild.members))
			mention = member.mention
			user = member.name
			guild=member.guild
			embed = nextcord.Embed(title="Пока!",description=f"<@{member.id}> покинул **{member.guild.name}**".format(members=members, mention=mention, user=user, guild=guild))
			embed.set_thumbnail(url=f"{member.display_avatar}")
			embed.set_footer(text=f"Нас теперь: {members}", icon_url=f"{member.display_avatar}")
			embed.set_image(url=random.choice(randombye))
			channel = self.client.get_channel(int(result[0]))
		await channel.send(embed=embed)

	@commands.group(invoke_without_command=True, aliases=['приветствия'])
	
	@commands.has_permissions(manage_channels=True)
	async def welcome(self,ctx):
		pass

	@welcome.command(aliases=['вход-канал'])
	
	@commands.has_permissions(manage_channels=True)
	async def hellochannel(self, ctx, channel:nextcord.TextChannel):
		db = sqlite3.connect('welcome.db')
		cursor = db.cursor()
		cursor.execute(f"SELECT channel_id_h FROM welcome WHERE guild_id = {ctx.guild.id}")
		result =  cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO welcome(guild_id, channel_id_h) VALUES(?,?)")
			val = (ctx.guild.id, channel.id)
			await ctx.send(f"<a:checkon:928259275090972772> Канал приветствия был установлен: {channel.mention}")
		elif result is not None:
			sql = ("UPDATE welcome SET channel_id_h = ? WHERE guild_id = ?")
			val = (channel.id, ctx.guild.id)
			await ctx.send(f"<a:checkon:928259275090972772> Канал приветствия был обновлён: {channel.mention}")
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

	@welcome.command(aliases=['выход-канал'])
	
	@commands.has_permissions(manage_channels=True)
	async def byechannel(self, ctx, channel:nextcord.TextChannel):
		db = sqlite3.connect('welcome.db')
		cursor = db.cursor()
		cursor.execute(f"SELECT channel_id_b FROM welcome WHERE guild_id = {ctx.guild.id}")
		result =  cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO welcome(guild_id, channel_id_b) VALUES(?,?)")
			val = (ctx.guild.id, channel.id)
			await ctx.send(f"<a:checkon:928259275090972772> Канал прощания был установлен: {channel.mention}")
		elif result is not None:
			sql = ("UPDATE welcome SET channel_id_b = ? WHERE guild_id = ?")
			val = (channel.id, ctx.guild.id)
			await ctx.send(f"<a:checkon:928259275090972772> Канал прощания был обновлён: {channel.mention}")
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

	@welcome.command(aliases=['сообщение'])
	
	@commands.has_permissions(manage_channels=True)
	async def message(self, ctx,*, text):
		db = sqlite3.connect('welcome.db')
		cursor = db.cursor()
		cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {ctx.guild.id}")
		result =  cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO welcome(guild_id, msg) VALUES(?,?)")
			val = (ctx.guild.id, text)
			await ctx.send(f"<a:checkon:928259275090972772> Сообщение было установлено: `{text}`")
		elif result is not None:
			sql = ("UPDATE welcome SET msg = ? WHERE guild_id = ?")
			val = (text, ctx.guild.id)
			await ctx.send(f"<a:checkon:928259275090972772> Сообщение было обновлено: `{text}`")
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

	@welcome.command(aliases=['сбросить'])
	
	@commands.has_permissions(manage_channels=True)
	async def reset(self, ctx):
		db = sqlite3.connect('welcome.db')
		cursor = db.cursor()
		cursor.execute("DELETE FROM welcome WHERE guild_id = ?", (ctx.guild.id,))
		msg = await ctx.send("<a:checkon:928259275090972772> Вы успешно отключили сообщения при входе и выходе!")
		await msg.add_reaction("<a:checkon:928259275090972772>")
		db.commit()
		cursor.close()
		db.close()

	@welcome.command(aliases=['просмотр'])
	
	@commands.has_permissions(manage_channels=True)
	async def look(self, ctx):
		db = sqlite3.connect('welcome.db')
		cursor = db.cursor()
		cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {ctx.guild.id}")
		result1 =  cursor.fetchone()
		if ctx.guild.icon:
			members = len(list(ctx.guild.members))
			mention = ctx.author.mention
			user = ctx.author.name
			guild=ctx.author.guild
			randombye = ["https://data.whicdn.com/images/315441551/original.gif", "https://animesher.com/orig/1/168/1681/16811/animesher.com_sad-watch-leonardo-crying-1681110.gif", "https://i1.wp.com/insiliconjurer.com/wp-content/uploads/2019/06/mobfightgif.gif?resize=540%2C225&ssl=1"]
			randomhello = ["https://i.pinimg.com/originals/aa/02/43/aa024380afc3587bad3cb6f8adbf1aab.gif","https://i.yapx.ru/Mr2aI.gif","https://78.media.tumblr.com/c7fe775814145d8a59f3629b72802357/tumblr_pc03twL37F1uvobnmo1_540.gif","https://i.imgur.com/1GJjhIy.gif"]
			embed = nextcord.Embed(title="Привет!",description=f"<@{ctx.author.id}> присоединился к **{ctx.author.guild.name}**\n{str(result1[0])}".format(members=members, mention=mention, user=user, guild=guild))
			embed.set_thumbnail(url=f"{ctx.author.display_avatar}")
			embed.set_footer(text=f"Нас теперь: {members}", icon_url=f"{ctx.author.display_avatar}")
			embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon.url}")
			embed.set_image(url=random.choice(randomhello))
		else:
			members = len(list(ctx.guild.members))
			mention = ctx.author.mention
			user = ctx.author.name
			guild=ctx.author.guild
			randombye = ["https://data.whicdn.com/images/315441551/original.gif", "https://animesher.com/orig/1/168/1681/16811/animesher.com_sad-watch-leonardo-crying-1681110.gif", "https://i1.wp.com/insiliconjurer.com/wp-content/uploads/2019/06/mobfightgif.gif?resize=540%2C225&ssl=1"]
			randomhello = ["https://i.pinimg.com/originals/aa/02/43/aa024380afc3587bad3cb6f8adbf1aab.gif","https://i.yapx.ru/Mr2aI.gif","https://78.media.tumblr.com/c7fe775814145d8a59f3629b72802357/tumblr_pc03twL37F1uvobnmo1_540.gif","https://i.imgur.com/1GJjhIy.gif"]
			embed = nextcord.Embed(title="Привет!",description=f"<@{ctx.author.id}> присоединился к **{ctx.author.guild.name}**\n{str(result1[0])}".format(members=members, mention=mention, user=user, guild=guild))
			embed.set_thumbnail(url=f"{ctx.author.display_avatar}")
			embed.set_footer(text=f"Нас теперь: {members}", icon_url=f"{ctx.author.display_avatar}")
			embed.set_image(url=random.choice(randomhello))
		await ctx.send("Сообщение при входе:", embed=embed)

		if ctx.guild.icon:
			embed1 = nextcord.Embed(title="Пока!",description=f"<@{ctx.author.id}> покинул **{ctx.guild.name}**".format(members=members, mention=mention, user=user, guild=guild))
			embed1.set_thumbnail(url=f"{ctx.author.display_avatar}")
			embed1.set_footer(text=f"Нас теперь: {members}", icon_url=f"{ctx.author.display_avatar}")
			embed1.set_author(name=f"{ctx.author.guild.name}", icon_url=f"{ctx.guild.icon.url}")
			embed1.set_image(url=random.choice(randombye))
		else:
			embed1 = nextcord.Embed(title="Пока!",description=f"<@{ctx.author.id}> покинул **{ctx.guild.name}**".format(members=members, mention=mention, user=user, guild=guild))
			embed1.set_thumbnail(url=f"{ctx.author.display_avatar}")
			embed1.set_footer(text=f"Нас теперь: {members}", icon_url=f"{ctx.author.display_avatar}")
			embed1.set_image(url=random.choice(randombye))
		await ctx.send("Сообщение при выходе:", embed=embed1)

def setup(client):
	client.add_cog(Welcome(client))