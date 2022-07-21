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

class SupportServerVerification(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message):
		verify = 'верификация'
		if message.channel.id == 935101453373157416:
			if verify in message.content.lower():
				await message.delete()
				await message.author.send(embed=nextcord.Embed(title='Верификация!', description='Чтобы пройти верификацию, напишите команду `?verify` в этот чат!', color=nextcord.Color.green()))
			else:
				await message.delete()

		if isinstance(message.channel, nextcord.channel.DMChannel):
			message1 = '?verify'
			if message1 in message.content.lower():
				try:
					pepeServer = self.client.get_guild(935101249479663637)
					targetUser = nextcord.utils.get(pepeServer.members, id=message.author.id)
					role = nextcord.utils.get(pepeServer.roles, id=935111857973383198)
					await targetUser.add_roles(role)
					await message.channel.send('✅ Вы успешно прошли верификацию!')
				except:
					await message.channel.send('❎ Вы уже прошли верификацию или вы не находитесь на сервере поддержки!')

def setup(client):
	client.add_cog(SupportServerVerification(client))