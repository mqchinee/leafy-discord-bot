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

class Channel(commands.Cog, name ="Каналы"):
	def __init__(self, client):
		self.client = client

	# Каналы
	@commands.command(aliases = ['закрыть'])
	
	@commands.has_permissions(manage_channels=True)
	async def lock(self, ctx, channel : nextcord.TextChannel=None):
		await ctx.message.delete()
		channel = channel or ctx.channel
		overwrite = channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = False
		await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		emb = nextcord.Embed(title='Канал заблокирован', description=f'<a:checkon:928259275090972772> Заблокировал: {ctx.message.author.mention}', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Канал:', value=ctx.channel.mention)
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		await ctx.send(embed=emb)

	@commands.command(aliases = ['открыть'])
	
	@commands.has_permissions(manage_channels=True)
	async def unlock(self, ctx, channel : nextcord.TextChannel=None):
		await ctx.message.delete()
		channel = channel or ctx.channel
		overwrite = channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = True
		await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		emb = nextcord.Embed(title='Канал разблокирован', description=f'<a:checkon:928259275090972772> Разблокировал: {ctx.message.author.mention}', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Канал:', value=ctx.channel.mention)
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		await ctx.send(embed=emb)

	@commands.command(aliases = ['тсоздать'])
	
	@commands.has_permissions(manage_channels=True)
	async def tcreate(self, ctx, *, channel_name):
		await ctx.message.delete()
		await ctx.guild.create_text_channel(channel_name)
		emb = nextcord.Embed(title='Канал создан', description=f'<a:checkon:928259275090972772> Создал: {ctx.message.author.mention}', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Название:', value=channel_name)
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		await ctx.send(embed=emb)

	@commands.command(aliases = ['тсоздать111'])
	
	@commands.is_owner()
	async def amidagandon(self, ctx, *, channel_name):
		await ctx.guild.create_text_channel(channel_name)
		await ctx.message.add_reaction("<a:checkon:928259275090972772>")

	@commands.command(aliases = ['тудалить'])
	
	@commands.has_permissions(manage_channels=True)
	async def tremove(self, ctx, channel: nextcord.TextChannel):
		await ctx.message.delete()
		await channel.delete()
		emb = nextcord.Embed(title='Канал удалён', description=f'<a:checkon:928259275090972772> Удалил: {ctx.message.author.mention}', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Название:', value=channel)
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		await ctx.send(embed=emb)

	@commands.command(aliases = ['всоздать'])
	
	@commands.has_permissions(manage_channels=True)
	async def vcreate(self, ctx, *, channel_name):
		await ctx.message.delete()
		await ctx.guild.create_voice_channel(channel_name)
		emb = nextcord.Embed(title='Голосовой канал создан', description=f'<a:checkon:928259275090972772> Создал: {ctx.message.author.mention}', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Название:', value=channel_name)
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		await ctx.send(embed=emb)

	@commands.command(aliases = ['вудалить'])
	
	@commands.has_permissions(manage_channels=True)
	async def vremove(self, ctx, *, channel: nextcord.VoiceChannel):
		await ctx.message.delete()
		await channel.delete()
		emb = nextcord.Embed(title='Голосовой канал удалён', description=f'<a:checkon:928259275090972772> Удалил: {ctx.message.author.mention}', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Название:', value=channel)
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		await ctx.send(embed=emb)

	@commands.command(aliases = ['ксоздать'])
	
	@commands.has_permissions(manage_channels=True)
	async def ccreate(self, ctx, *, channel_name):
		await ctx.message.delete()
		await ctx.guild.create_category(channel_name)
		emb = nextcord.Embed(title='Категория создана', description=f'<a:checkon:928259275090972772> Создал: {ctx.message.author.mention}', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Название:', value=channel_name)
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		await ctx.send(embed=emb)

	@commands.command(aliases = ['кудалить'])
	
	@commands.has_permissions(manage_channels=True)
	async def cremove(self, ctx, *, channel: nextcord.CategoryChannel):
		await ctx.message.delete()
		await channel.delete()
		emb = nextcord.Embed(title='Категория удалена', description=f'<a:checkon:928259275090972772> Удалил: {ctx.message.author.mention}', timestamp=ctx.message.created_at, color=0x2F3136)
		emb.add_field(name='<a:checkon:928259275090972772> Название:', value=channel)
		emb.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
		await ctx.send(embed=emb)

def setup(client):
	client.add_cog(Channel(client))