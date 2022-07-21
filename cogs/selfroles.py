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

class RolesForReaction(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command(aliases=['роли-по-реакции'])
	@commands.has_permissions(administrator=True)
	async def reactionrole(self, ctx):
		await ctx.send(embed=nextcord.Embed(title='Роли за реакции', description=f'{ctx.author.mention}, постарайтесь ответить на все вопросы в течении **3-х** минут.'))

		questions = ["Каким будет сообщение?\nПример: 🟦 - синий, 🟥 - красный", "Введите эмоджи (через пробел)\nПример: 🟦 🟥", "Введите роли без упоминания через |\nПример: Синий цвет | Красный цвет", f"Упомяните канал\nПример: {ctx.channel.mention}"]
		answers = []

		def check(user):
			return user.author == ctx.author and user.channel == ctx.channel
		
		for question in questions:
			await ctx.send(question)

			try:
				msg = await self.client.wait_for('message', timeout=180.0, check=check)
			except asyncio.TimeoutError:
				await ctx.send(embed=nextcord.Embed(title='Роли за реакции', description=f'{ctx.author.mention}, вы не успели ответить на все вопросы, постарайтесь отвечать быстрее в следующий раз.'))
				return
			else:
				answers.append(msg.content)

		emojis = answers[1].split(" ")
		roles = answers[2].split(" | ")
		c_id = int(answers[3][2:-1])
		channel = self.client.get_channel(c_id)

		client_msg = await channel.send(embed=nextcord.Embed(title='Роли за реакции', description=answers[0]))

		with open("selfrole.json", "r") as f:
			self_roles = json.load(f)

		self_roles[str(client_msg.id)] = {}
		self_roles[str(client_msg.id)]["emojis"] = emojis
		self_roles[str(client_msg.id)]["roles"] = roles

		with open("selfrole.json", "w") as f:
			json.dump(self_roles, f)

		for emoji in emojis:
			await client_msg.add_reaction(emoji)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		msg_id = payload.message_id

		with open("selfrole.json", "r") as f:
			self_roles = json.load(f)

		if payload.member.bot:
			return
		
		if str(msg_id) in self_roles:
			emojis = []
			roles = []

			for emoji in self_roles[str(msg_id)]['emojis']:
				emojis.append(emoji)

			for role in self_roles[str(msg_id)]['roles']:
				roles.append(role)
			
			guild = self.client.get_guild(payload.guild_id)

			for i in range(len(emojis)):
				choosed_emoji = str(payload.emoji)
				if choosed_emoji == emojis[i]:
					selected_role = roles[i]

					role = nextcord.utils.get(guild.roles, name=selected_role)

					await payload.member.add_roles(role)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		msg_id = payload.message_id

		with open("selfrole.json", "r") as f:
			self_roles = json.load(f)
		
		if str(msg_id) in self_roles:
			emojis = []
			roles = []

			for emoji in self_roles[str(msg_id)]['emojis']:
				emojis.append(
					emoji)

			for role in self_roles[str(msg_id)]['roles']:
				roles.append(role)
			
			guild = self.client.get_guild(payload.guild_id)

			for i in range(len(emojis)):
				choosed_emoji = str(payload.emoji)
				if choosed_emoji == emojis[i]:
					selected_role = roles[i]

					role = nextcord.utils.get(guild.roles, name=selected_role)

					member = await(guild.fetch_member(payload.user_id))
					if member is not None:
						await member.remove_roles(role)

def setup(client):
	client.add_cog(RolesForReaction(client))