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

class Roleplay(commands.Cog, name ="Ролеплей"):
	def __init__(self,client):
		self.client = client

	# Анимации!
	@commands.command(aliases=['обнять'])
	
	async def hug(self, ctx, member : nextcord.Member, *, text = None):
		hug = ["https://c.tenor.com/cFhjNVecNGcAAAAC/anime-hug.gif", "https://c.tenor.com/PuuhAT9tMBYAAAAC/anime-cuddles.gif", "https://c.tenor.com/ixaDEFhZJSsAAAAC/anime-choke.gif", "https://c.tenor.com/qF7mO4nnL0sAAAAC/abra%C3%A7o-hug.gif", "https://c.tenor.com/uIBg3BLATf0AAAAC/hug-darker.gif", "https://c.tenor.com/ncblDAj_2FwAAAAC/abrazo-hug.gif", "https://c.tenor.com/QCQV57yhBMsAAAAd/comforting-hug.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'👐 {author.mention} **обнял(а)** {member.mention}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'👐 {author.mention} **обнял(а)** {member.mention}\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['поцеловать'])
	
	async def kiss(self, ctx, member : nextcord.Member, *, text = None):
		hug = ["https://c.tenor.com/I8kWjuAtX-QAAAAC/anime-ano.gif", "https://c.tenor.com/TWbZjCy8iN4AAAAC/girl-anime.gif", "https://c.tenor.com/JQ9jjb_JTqEAAAAC/anime-kiss.gif", "https://c.tenor.com/16MBIsjDDYcAAAAC/love-cheek.gif", "https://c.tenor.com/Ge4DoX5aDD0AAAAC/love-kiss.gif", "https://c.tenor.com/VTvkMN6P648AAAAC/anime-kiss.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'❤️ {author.mention} **поцеловал(а)** {member.mention}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'❤️ {author.mention} **поцеловал(а)** {member.mention}\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['гуль'])
	
	async def ghoul(self, ctx, *, text = None):
		hug = ["https://c.tenor.com/rGWSL4dY9B8AAAAC/ken-kaneki.gif", "https://c.tenor.com/Jwh5aCZwmbwAAAAC/tokyo-ghoul.gif", "https://c.tenor.com/2KchjcuZ7-gAAAAC/%D7%91%D7%A0%D7%99%D7%94.gif", "https://c.tenor.com/MyCm9Gd2tDEAAAAC/tokyo-ghoul-anime.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'🖤 {author.mention} **отбросил(а) эмоции**', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'🖤 {author.mention} **отбросил(а) эмоции**\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['смутиться'])
	
	async def lewd(self, ctx, *, text = None):
		hug = ["https://c.tenor.com/2iEVFFCbPj4AAAAC/momokuri-anime-blush.gif", "https://c.tenor.com/Tk2xYonmrsEAAAAC/anime-blushing.gif", "https://c.tenor.com/bEes0xCurvMAAAAC/anime-blush-dizzy.gif", "https://c.tenor.com/HAWlr1X00Y8AAAAC/anime-love.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'😊 {author.mention} **смущен(а)**', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'😊 {author.mention} **смущен(а)**\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['ударить'])
	
	async def slap(self, ctx, member : nextcord.Member, *, text = None):
		hug = ["https://c.tenor.com/1lJTSPaUfKkAAAAd/chika-fujiwara-fwap.gif", "https://c.tenor.com/iDdGxlZZfGoAAAAC/powerful-head-slap.gif", "https://c.tenor.com/wOCOTBGZJyEAAAAC/chikku-neesan-girl-hit-wall.gif", "https://c.tenor.com/E4Px9kJOQ5wAAAAC/anime-kid.gif", "https://c.tenor.com/1-1M4PZpYcMAAAAd/tsuki-tsuki-ga.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'🖐️ {author.mention} **ударил(а)** {member.mention}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'🖐️ {author.mention} **ударил(а)** {member.mention}\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['погладить'])
	
	async def pat(self, ctx, member : nextcord.Member, *, text = None):
		hug = ["https://c.tenor.com/3PjRNS8paykAAAAC/pat-pat-head.gif", "https://c.tenor.com/N41zKEDABuUAAAAC/anime-head-pat-anime-pat.gif", "https://c.tenor.com/8DaE6qzF0DwAAAAC/neet-anime.gif", "https://c.tenor.com/Bps4SVOb8JkAAAAC/head-petting.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'😀 {author.mention} **погладил(а)** {member.mention}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'😀 {author.mention} **погладил(а)** {member.mention}\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['лизнуть'])
	
	async def lick(self, ctx, member : nextcord.Member, *, text = None):
		hug = ["https://c.tenor.com/uw6-q_y4xKsAAAAd/%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5-darling-in-the-franxx.gif", "https://c.tenor.com/Yo1IUz2KJy0AAAAC/loli-lick.gif", "https://c.tenor.com/0LMxPQdFBKAAAAAC/nekopara-kiss.gif", "https://c.tenor.com/4U2-K7XUIJUAAAAC/pain-ellenoar.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'😛 {author.mention} **облизал(а)** {member.mention}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'😛 {author.mention} **облизал(а)** {member.mention}\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['кастом'])
	
	async def custom(self, ctx, *, text):
		author = ctx.message.author
		emb = nextcord.Embed(description=f'{ctx.author.mention} {text}')
		await ctx.send(embed=emb)

	@commands.command(aliases=['злиться'])
	
	async def angry(self, ctx, member : nextcord.Member, *, text = None):
		hug = ["https://c.tenor.com/X3x3Y2mp2W8AAAAC/anime-angry.gif", "https://c.tenor.com/wtSs_VCHYmEAAAAC/noela-angry.gif", "https://c.tenor.com/-aieB6Qw8YQAAAAd/anime-angry.gif", "https://c.tenor.com/B2G5s1cY7GUAAAAC/anime-angry.gif", "https://c.tenor.com/jgFVzr3YeJwAAAAC/date-a-live-rage.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'😠 {author.mention} **разозлился(лась) на** {member.mention}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'😠 {author.mention} **разозлился(лась) на** {member.mention}\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['покормить'])
	
	async def feed(self, ctx, member : nextcord.Member, *, text = None):
		hug = ["https://c.tenor.com/kcpMVM8nvMwAAAAC/tsumiki-miniwa-acchi-kocchi.gif", "https://c.tenor.com/JHqOKnXVNDQAAAAC/azunom-feed.gif", "https://c.tenor.com/_qetTKAryEsAAAAC/miyabi-ito-ryu-yamada.gif", "https://c.tenor.com/xS09IqCS1e0AAAAd/anime-anime-boy.gif", "https://c.tenor.com/6wbujfe8-fcAAAAd/anime-feed-me.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'🍕 {author.mention} **кормит** {member.mention}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'🍕 {author.mention} **кормит** {member.mention}\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['хвост'])
	
	async def wag(self, ctx, *, text = None):
		hug = ["https://c.tenor.com/aqrVj-YBUucAAAAC/shino-wag.gif", "https://c.tenor.com/ICV1nFqqx40AAAAC/murenase-lanka.gif", "https://c.tenor.com/kL8cLeAZxXUAAAAC/tail-anime.gif", "https://c.tenor.com/4g4BQMRtCN4AAAAC/dog-animation.gif", "https://c.tenor.com/Vz5yn1fwv-gAAAAd/pat-anime.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'✨ {author.mention} **виляет хвостом**', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'✨ {author.mention} **виляет хвостом**\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['кричать'])
	
	async def scream(self, ctx, *, text = None):
		hug = ["https://c.tenor.com/MXlXZbQ7054AAAAC/anime-girl.gif", "https://c.tenor.com/USUVjH4Ah8MAAAAC/anime-freaking-out.gif", "https://c.tenor.com/PqJsoGX4qOwAAAAC/angry-cat-noises-shout.gif", "https://c.tenor.com/Pz9fOE6TujoAAAAC/miko-anime.gif", "https://c.tenor.com/mL_keJcBwCIAAAAC/fangirl-excited.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'😱 {author.mention} **кричит**', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'😱 {author.mention} **кричит**\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['напиться'])
	
	async def drunk(self, ctx, *, text = None):
		hug = ["https://c.tenor.com/KSIcVh0UpbIAAAAC/anime-drink.gif", "https://c.tenor.com/lk8yVO8VOEsAAAAC/drinking-kobayashi.gif", "https://c.tenor.com/kDwsneWH0FgAAAAC/hikikomori-anime.gif", "https://c.tenor.com/5LzGYYilK04AAAAC/hikikomori-kobayashi.gif", "https://c.tenor.com/HVo5X4CDYgAAAAAC/gintama-drunk.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'🤤 {author.mention} **пьян(а)**', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'🤤 {author.mention} **пьян(а)**\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

	@commands.command(aliases=['танцевать'])
	
	async def dance(self, ctx, *, text = None):
		hug = ["https://c.tenor.com/mKTS5nbF1zcAAAAd/cute-anime-dancing.gif", "https://c.tenor.com/TVFrC38WTRQAAAAC/celebrate-shinkoukei.gif", "https://c.tenor.com/d2NYSXokaK4AAAAC/pikachu-cheer-dance.gif", "https://c.tenor.com/jWRFHjiNdkgAAAAd/anime-dance.gif", "https://c.tenor.com/MGhl4dBxjpMAAAAC/dance-anime.gif"]
		author = ctx.message.author
		if text == None:
			emb1 = nextcord.Embed(title='', description=f'💃 {author.mention} **танцует**', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb1.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb1)
		else:
			emb = nextcord.Embed(title='', description=f'💃 {author.mention} **танцует**\n *Комментарий*: {text}', timestamp=ctx.message.created_at, colour=ctx.author.color)
			emb.set_image(url=f'{random.choice(hug)}')
			await ctx.send(embed=emb)

def setup(client):
	client.add_cog(Roleplay(client))