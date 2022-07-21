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

class AutoModeration(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author is not message.guild.owner:
			antilinkdb = sqlite3.connect('automod.db')
			antilinkcursor = antilinkdb.cursor()
			antilinkcursor.execute("SELECT guild FROM enabled WHERE guild = ?", (message.guild.id,))
			linkdata = antilinkcursor.fetchone()
			if linkdata:
				link = 'discord.gg'
				if not message.author.bot:
					if link in message.content.lower():
						await message.delete()
						await message.channel.send(embed=nextcord.Embed(description=f'{message.author.mention}, реклама - это плохо!', color=0x2F3136))

	@commands.group(pass_context=True, invoke_without_command=True, aliases = ['авто-мод'])
	@commands.has_permissions(administrator=True)
	async def automod(self, ctx):
		pass

	@automod.command(aliases = ['ссылка'])
	@commands.has_permissions(administrator=True)
	async def link(self, ctx):
		antilinkdb = sqlite3.connect('automod.db')
		antilinkcursor = antilinkdb.cursor()
		antilinkcursor.execute("SELECT guild FROM enabled WHERE guild = ?", (ctx.guild.id,))
		linkdata = antilinkcursor.fetchone()
		if not linkdata:
			antilinkcursor.execute("INSERT INTO enabled VALUES(?)", (ctx.guild.id,))
			await ctx.send(embed=nextcord.Embed(description='Теперь ссылки на другие дискорд-сервера будут блокироваться.', color=0x2F3136))
		if linkdata:
			antilinkcursor.execute("DELETE FROM enabled WHERE guild = ?", (ctx.guild.id,))
			await ctx.send(embed=nextcord.Embed(description='Теперь ссылки на другие дискорд-сервера не будут блокироваться.', color=0x2F3136))
		antilinkdb.commit()
		antilinkcursor.close()
		antilinkdb.close()

def setup(client):
	client.add_cog(AutoModeration(client))