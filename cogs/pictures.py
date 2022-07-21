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

class Pictures(commands.Cog, name ="Манипуляции с картинками"):
	def __init__(self,client):
		self.client = client

	# Мапипуляции с картинками!
	@commands.command(aliases = ['розыск'])
	
	async def wanted(self, ctx, member : nextcord.Member = None):
		if member == None:
			member = ctx.author

		wanted = Image.open("IMG/imagemanipulation2.jpg")

		asset = member.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		profilepic = Image.open(data)

		profilepic = profilepic.resize((423, 403))

		wanted.paste(profilepic, (98, 211))

		wanted.save("IMG/wantedpic.png")

		await ctx.send(file=nextcord.File('IMG/wantedpic.png'))

	@commands.command(aliases = ['могила'])
	
	async def rip(self, ctx, member : nextcord.Member = None, *, text = None):
		if member == None:
			member = ctx.author

		if text == None:
			rip = Image.open("IMG/manipulationcommand1.jpg")
			asset = member.display_avatar.with_size(128)
			data = BytesIO(await asset.read())
			profilepic = Image.open(data)
			profilepic = profilepic.resize((145, 139))
			rip.paste(profilepic, (108, 73))
			rip.save("IMG/rippic.png")
			await ctx.send(file=nextcord.File("IMG/rippic.png"))
		else:
			rip = Image.open("IMG/manipulationcommand1.jpg")
			asset = member.display_avatar.with_size(128)
			data = BytesIO(await asset.read())
			profilepic = Image.open(data)
			profilepic = profilepic.resize((145, 139))
			idraw = ImageDraw.Draw(rip)
			headline = ImageFont.truetype('fonts/sans.otf', size = 12)
			idraw.text((97, 233), text, font = headline, fill="#000")
			rip.paste(profilepic, (108, 73))
			rip.save("IMG/rippictext.png")
			await ctx.send(file=nextcord.File("IMG/rippictext.png"))

	@commands.command(aliases = ['пожар'])
	
	async def fire(self, ctx, member : nextcord.Member = None):
		if member == None:
			member = ctx.author

		rip = Image.open("IMG/fire.jpg")

		asset = member.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		profilepic = Image.open(data)

		profilepic = profilepic.resize((228, 238))

		rip.paste(profilepic, (398, 98))

		rip.save("IMG/firepic.png")

		await ctx.send(file=nextcord.File("IMG/firepic.png"))

	@commands.command(aliases = ['утка'])
	
	async def duck(self, ctx, member : nextcord.Member = None):
		if member == None:
			member = ctx.author

		rip = Image.open("IMG/duck.jpg")

		asset = member.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		profilepic = Image.open(data)

		profilepic = profilepic.resize((389, 392))

		rip.paste(profilepic, (152, 101))

		rip.save("IMG/duckpic.png")

		await ctx.send(file=nextcord.File("IMG/duckpic.png"))

	@commands.command(aliases = ['кот'])
	
	async def cat(self, ctx, member : nextcord.Member = None):
		if member == None:
			member = ctx.author

		rip = Image.open("IMG/cat.jpg")

		asset = member.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		profilepic = Image.open(data)

		profilepic = profilepic.resize((498, 432))

		rip.paste(profilepic, (388, 262))

		rip.save("IMG/catpic.png")

		await ctx.send(file=nextcord.File("IMG/catpic.png"))

	@commands.command(aliases = ['пёс'])
	
	async def dog(self, ctx, member : nextcord.Member = None):
		if member == None:
			member = ctx.author

		rip = Image.open("IMG/dog.jpg")

		asset = member.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		profilepic = Image.open(data)

		profilepic = profilepic.resize((282, 278))

		rip.paste(profilepic, (247, 185))

		rip.save("IMG/dogpic.png")

		await ctx.send(file=nextcord.File("IMG/dogpic.png"))

	@commands.command(aliases = ['что'])
	
	async def wtf(self, ctx, member : nextcord.Member = None):
		if member == None:
			member = ctx.author

		rip = Image.open("IMG/wtf.png")

		asset = member.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		profilepic = Image.open(data)

		profilepic = profilepic.resize((339, 335))

		rip.paste(profilepic, (449, 232))

		rip.save("IMG/wtfpic.png")

		await ctx.send(file=nextcord.File("IMG/wtfpic.png"))


	@commands.command(aliases = ['губка'])
	
	async def sponge(self, ctx, member : nextcord.Member = None):
		if member == None:
			member = ctx.author

		sponge = Image.open("IMG/sponge.jpg")

		asset = member.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		profilepic = Image.open(data)

		profilepic = profilepic.resize((146, 163))

		sponge.paste(profilepic, (58, 112))

		sponge.save("IMG/spongepic.png")

		await ctx.send(file=nextcord.File("IMG/spongepic.png"))

	@commands.command(pass_context=True, aliases = ['уно'])
	
	async def uno(self, ctx):
		await ctx.send(file=nextcord.File("IMG/uno.gif"))

def setup(client):
	client.add_cog(Pictures(client))