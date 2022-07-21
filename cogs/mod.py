import nextcord
import typing
import asyncio
import json
import requests
import random
import aiohttp
import datetime
from nextcord.utils import *
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
import humanfriendly
from utils import default

def convert(self, time):
		pos = ["с","м","ч","д"]

		time_dict = {"с" : 1, "м" : 60, "ч" : 3600 , "д" : 3600*24}

		unit = time[-1]

		if unit not in pos:
			return -1
		try:
			val = int(time[:-1])
		except:
			return -2

		return val * time_dict[unit]

class Moderation(commands.Cog, name ="Модерация"):
	def __init__(self, client):
		self.client = client

	# Удаление сообщений
	@commands.command( pass_context = True, aliases = ['очистить'])
	
	@commands.has_permissions( manage_messages = True )

	async def clear(self, ctx, amount = 100 ):
		if amount < 1:
			return await ctx.send("<a:checkoff:928259276273758208> Нельзя указывать число **меньше нуля!**")
		elif amount > 1000:
			return await ctx.send(f"<a:checkoff:928259276273758208> Вы не можете удалить больше **1000** сообщений! **({amount}/1000)**")
		else:
			await ctx.channel.purge( limit = amount + 1 )
			embed=nextcord.Embed(title='Очистка!', timestamp=ctx.message.created_at, color=0x2F3136)
			embed.add_field(name='<a:checkon:928259275090972772> Очистил:', value=f'{ctx.author.mention}', inline = False)
			embed.add_field(name='<a:checkon:928259275090972772> Очищено:', value=f'`{amount} сообщений`', inline = False)
			embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
			await ctx.send(embed=embed, delete_after=5.0)


	# Кик
	@commands.command( pass_context = True, aliases = ['кик'])
	
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: nextcord.Member, *, reason = 'Без причины'):
		

		await ctx.message.delete()

		await member.kick(reason = reason)
		author = ctx.message.author
		embedkick = nextcord.Embed(title=f"Кик!", timestamp=ctx.message.created_at, color=0x2F3136)
		embedkick.add_field(name='<a:checkon:928259275090972772> Кикнут:', value=f'{member.mention}', inline=False)
		embedkick.add_field(name='<a:checkon:928259275090972772> Кикнул:', value=f'{author.mention}', inline=False)
		embedkick.add_field(name='<a:checkon:928259275090972772> Причина:', value=f'`{reason}`', inline=False)

		embedkick.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embedkick.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)


		await ctx.send(embed = embedkick)

	 # Бан
	@commands.command( pass_context = True, aliases = ['бан'])
	
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member: nextcord.Member, *, reason = 'Без причины'):
		

		await ctx.message.delete()

		await member.ban(reason = reason)
		author = ctx.message.author
		embedban = nextcord.Embed(title=f"Бан!", timestamp=ctx.message.created_at, color=0x2F3136)
		embedban.add_field(name='<a:checkon:928259275090972772> Забанен:', value=f'{member.name}#{member.discriminator}', inline=False)
		embedban.add_field(name='<a:checkon:928259275090972772> Забанил:', value=f'{author.mention}', inline=False)
		embedban.add_field(name='<a:checkon:928259275090972772> Причина:', value=f'`{reason}`', inline=False)

		embedban.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embedban.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)


		await ctx.send(embed = embedban)

	# Ping
	@commands.command(pass_context=True, aliases = ['пинг'])
	
	async def ping(self, ctx):
		await ctx.channel.purge(limit=1)
		embed=nextcord.Embed(title='Пинг!', description=f'<a:checkon:928259275090972772> Мой пинг: {round(self.client.latency*1000)}мс', timestamp=ctx.message.created_at, color=0x2F3136)
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		await ctx.send(embed=embed)

	# Мут
	@commands.command(description="Mutes the specified user.", aliases = ['мьют'])
	
	@commands.has_permissions(manage_messages=True)
	async def mute(self, ctx, member: nextcord.Member, *, reason='Без причины'):
		
		guild = ctx.guild
		mutedRole = nextcord.utils.get(guild.roles, name="Muted2")
		await ctx.message.delete()

		if not mutedRole:
			mutedRole = await guild.create_role(name="Muted2")

			for channel in guild.channels:
				await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
		embed = nextcord.Embed(title="Мут!", timestamp=ctx.message.created_at, color=0x2F3136)
		embed.add_field(name="<a:checkon:928259275090972772> Замучен:", value=f'{member.mention}', inline=False)
		embed.add_field(name="<a:checkon:928259275090972772> Замутил:", value=f'{ctx.author.mention}', inline=False)
		embed.add_field(name="<a:checkon:928259275090972772> Причина:", value=f'`{reason}`', inline=False)
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		await ctx.send(embed=embed)
		await member.add_roles(mutedRole, reason=reason)

	@commands.group(aliases = ['таймаут'])
	async def timeout(self, ctx):
		pass

	@timeout.command(aliases = ['добавить'])
	@commands.has_permissions(manage_messages=True)
	async def add(self, ctx, member:nextcord.Member, time, *, reason='Без причины'):
		time = humanfriendly.parse_timespan(time)
		await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time))
		embed = nextcord.Embed(title="Таймаут!", timestamp=ctx.message.created_at, color=0x2F3136)
		embed.add_field(name="<a:checkon:928259275090972772> Выдан:", value=f'{member.mention}', inline=False)
		embed.add_field(name="<a:checkon:928259275090972772> Выдал:", value=f'{ctx.author.mention}', inline=False)
		embed.add_field(name="<a:checkon:928259275090972772> Причина:", value=f'`{reason}`', inline=False)
		if time >= 3600:
			if time < 86400:
				embed.add_field(name="<a:checkon:928259275090972772> Заканчивается", value=f'`Через {round(time/3600, 1)} часов`\n`UTC:` {default.date(nextcord.utils.utcnow()+datetime.timedelta(seconds=time))}', inline=False)
		if time < 3600:
			if time > 60:
				embed.add_field(name="<a:checkon:928259275090972772> Заканчивается", value=f'`Через {round(time/60, 1)} минут`\n`UTC:` {default.date(nextcord.utils.utcnow()+datetime.timedelta(seconds=time))}', inline=False)
			elif time == 60:
				embed.add_field(name="<a:checkon:928259275090972772> Заканчивается", value=f'`Через {round(time/60, 1)} минут`\n`UTC:` {default.date(nextcord.utils.utcnow()+datetime.timedelta(seconds=time))}', inline=False)
		if time < 60:
			embed.add_field(name="<a:checkon:928259275090972772> Заканчивается", value=f'`Через {round(time, 1)} секунд`\n`UTC:` {default.date(nextcord.utils.utcnow()+datetime.timedelta(seconds=time))}', inline=False)
		if time >= 86400:
			embed.add_field(name="<a:checkon:928259275090972772> Заканчивается", value=f'`Через {round(time/86400, 1)} дней`\n`UTC:` {default.date(nextcord.utils.utcnow()+datetime.timedelta(seconds=time))}', inline=False)
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		await ctx.send(embed=embed)

	@timeout.command(aliases = ['убрать'])
	@commands.has_permissions(manage_messages=True)
	async def remove(self, ctx, member:nextcord.Member):
		await member.edit(timeout=None)
		embed = nextcord.Embed(title="Таймаут!", timestamp=ctx.message.created_at, color=0x2F3136)
		embed.add_field(name="<a:checkon:928259275090972772> Снят:", value=f'{member.mention}', inline=False)
		embed.add_field(name="<a:checkon:928259275090972772> Снял:", value=f'{ctx.author.mention}', inline=False)
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		await ctx.send(embed=embed)

	# Размут
	@commands.command(description="Unmutes a specified user.", aliases = ['размьют'])
	
	@commands.has_permissions(manage_messages=True)
	async def unmute(self, ctx, member: nextcord.Member):
		await ctx.message.delete()
		mutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted2")
		await member.remove_roles(mutedRole)
		author = ctx.message.author
		embed = nextcord.Embed(title="Размут!", timestamp=ctx.message.created_at, color=0x2F3136)
		embed.add_field(name="<a:checkon:928259275090972772> Размучен:", value=f'{member.mention}', inline=False)
		embed.add_field(name="<a:checkon:928259275090972772> Размутил:", value=f'{author.mention}', inline=False)
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
		
		await ctx.send(embed=embed)


	# Разбан
	@commands.command(aliases = ['разбан'])
	@commands.has_permissions(ban_members=True)
	
	async def unban(self, ctx, *, member):
		await ctx.message.delete()
		banned_users = await ctx.guild.bans()
		
		member_name, member_discriminator = member.split('#')
		for ban_entry in banned_users:
			user = ban_entry.user
			
			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user)
				author = ctx.message.author
				embed = nextcord.Embed(title="Разбан!", timestamp=ctx.message.created_at, color=0x2F3136)
				embed.add_field(name="<a:checkon:928259275090972772> Разбанен:", value=f'{user}', inline=False)
				embed.add_field(name="<a:checkon:928259275090972772> Разбанил:", value=f'{author.mention}', inline=False)
				embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
				embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)

				await ctx.send(embed=embed)

	@commands.command(aliases = ['репорт'])
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def report(self, ctx, member:nextcord.Member, *, reason):
		await ctx.message.delete()
		if member == ctx.author:
			return await ctx.send(f'{ctx.author.mention}, вы не можете подать жалобу на самого себя.')
		else:
			mods = []
			message = ''
			for user in ctx.guild.members:
				user_perm = ctx.channel.permissions_for(user)
				if user_perm.kick_members or user_perm.ban_members or user_perm.manage_messages:
					if not user.bot:
						mods.append(f'{user.mention}')
						message = f"{', '.join(mods)}\n"
			embed = nextcord.Embed(title='Жалоба', description=f'**Пользователь** {ctx.author.mention} **пожаловался на пользователя** {member.mention}**.**\n*Все модераторы были упомянуты, чтобы скорее решить проблему.*\nЕсли вы создали "ложную тревогу", модераторы могут наказать вас.', timestamp=ctx.message.created_at, color=0x2F3136)
			embed.add_field(name='Причина:', value=reason)
			embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
			await ctx.send(message, embed=embed)

	@commands.command()
	async def fakeban(self, ctx, member: nextcord.Member, *, reason = 'Без причины'):
		if ctx.author.id == 748494305005535253 or ctx.author.id == 903993786160521247:
			await ctx.message.delete()
			author = ctx.message.author
			embedban = nextcord.Embed(title=f"Бан!", timestamp=ctx.message.created_at, color=0x2F3136)
			embedban.add_field(name='<a:checkon:928259275090972772> Забанен:', value=f'{member.name}#{member.discriminator}', inline=False)
			embedban.add_field(name='<a:checkon:928259275090972772> Забанил:', value=f'{author.mention}', inline=False)
			embedban.add_field(name='<a:checkon:928259275090972772> Причина:', value=f'`{reason}`', inline=False)

			embedban.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
			embedban.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
			await ctx.send(embed=embedban)
		else:
			return

	
def setup(client):
	client.add_cog(Moderation(client))