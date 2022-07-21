# Настройка
import nextcord
import typing
import asyncio
import json
import bs4, requests
import random
import aiohttp
import os
import sqlite3
import urllib.parse, urllib.request, re
from urllib.parse import urlparse
from nextcord.utils import get
from itertools import cycle
from io import BytesIO
from nextcord.ext import commands, tasks
from bs4 import BeautifulSoup
from nextcord import Member
from nextcord.ext.commands import has_permissions, MissingPermissions, cooldown, BucketType
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import psutil

class Requests(commands.Cog, name ="From sites"):
	def __init__(self,client):
		self.client = client

	@commands.command(aliases=['шутка'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def joke(self,ctx):
		response = requests.get('http://rzhunemogu.ru/')
		soup = BeautifulSoup(response.text, 'html.parser')
		text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion1_Pane_0_content_LabelText').getText()
		emb=nextcord.Embed(title="Случайная шутка", description=text)
		emb.set_footer(text="Источник: http://rzhunemogu.ru/", icon_url=ctx.author.display_avatar)
		await ctx.send(embed=emb)

def setup(client):
	client.add_cog(Requests(client))