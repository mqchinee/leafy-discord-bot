import nextcord
import asyncio
from nextcord.ext import commands
import sqlite3
import validators


class voice(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		guildID = member.guild.id
		c.execute("SELECT voiceChannelID FROM guild WHERE guildID = ?", (guildID,))
		voice=c.fetchone()
		if voice is None:
			pass
		else:
			voiceID = voice[0]
			try:
				if after.channel.id == voiceID:
					c.execute("SELECT * FROM voiceChannel WHERE userID = ?", (member.id,))
					cooldown=c.fetchone()
					if cooldown is None:
						c.execute("SELECT voiceCategoryID FROM guild WHERE guildID = ?", (guildID,))
						voice=c.fetchone()
						c.execute("SELECT channelName, channelLimit FROM userSettings WHERE userID = ?", (member.id,))
						setting=c.fetchone()
						c.execute("SELECT channelLimit FROM guildSettings WHERE guildID = ?", (guildID,))
						guildSetting=c.fetchone()
						if setting is None:
							name = f"Канал {member.name}"
							if guildSetting is None:
								limit = 0
							else:
								limit = guildSetting[0]
						else:
							if guildSetting is None:
								name = setting[0]
								limit = setting[1]
							elif guildSetting is not None and setting[1] == 0:
								name = setting[0]
								limit = guildSetting[0]
							else:
								name = setting[0]
								limit = setting[1]
						categoryID = voice[0]
						id = member.id
						category = self.client.get_channel(categoryID)
						channel2 = await member.guild.create_voice_channel(name,category=category)
						channelID = channel2.id
						await member.move_to(channel2)
						await channel2.set_permissions(self.client.user, connect=True,read_messages=True)
						await channel2.edit(name= name, user_limit = limit)
						c.execute("INSERT INTO voiceChannel VALUES (?, ?)", (id,channelID))
						conn.commit()
						def check(a,b,c):
							return len(channel2.members) == 0
						await self.client.wait_for('voice_state_update', check=check)
						await channel2.delete()
						await asyncio.sleep(3)
						c.execute('DELETE FROM voiceChannel WHERE userID=?', (id,))
					else:
						await member.send("<:voice:928259275401347105> Вы слишком быстро создаёте каналы! Попробуйте снова через 20 секунд!")
						await asyncio.sleep(20)
						return
			except:
				pass
		conn.commit()
		conn.close()

	@commands.group(aliases=['гк'])
	async def vc(self, ctx):
		pass

	@vc.command(aliases=['создать'])
	async def create(self, ctx):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		guildID = ctx.guild.id
		id = ctx.author.id
		if ctx.author.id == ctx.guild.owner.id:
			def check(m):
				return m.author.id == ctx.author.id
			await ctx.channel.send(embed=nextcord.Embed(description="<:voice:928259275401347105> Вопрос №1"))
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> Назовите имя категории, в котором будет временный голосовой канал"))
			try:
				category = await self.client.wait_for('message', check=check, timeout = 60.0)
			except asyncio.TimeoutError:
				await ctx.channel.send(embed=nextcord.Embed(description='<:voice:928259275401347105> Вы слишком долго отвечали!'))
			else:
				new_cat = await ctx.guild.create_category_channel(category.content)
				await ctx.channel.send(embed=nextcord.Embed(description='<:voice:928259275401347105> Назовите имя голосового канала (пример: [+] Создать канал)'))
				try:
					channel = await self.client.wait_for('message', check=check, timeout = 60.0)
				except asyncio.TimeoutError:
					await ctx.channel.send(embed=nextcord.Embed(description='<:voice:928259275401347105> Вы слишком долго отвечали!'))
				else:
					try:
						channel = await ctx.guild.create_voice_channel(channel.content, category=new_cat)
						c.execute("SELECT * FROM guild WHERE guildID = ? AND ownerID=?", (guildID, id))
						voice=c.fetchone()
						if voice is None:
							c.execute ("INSERT INTO guild VALUES (?, ?, ?, ?)",(guildID,id,channel.id,new_cat.id))
						else:
							c.execute ("UPDATE guild SET guildID = ?, ownerID = ?, voiceChannelID = ?, voiceCategoryID = ? WHERE guildID = ?",(guildID,id,channel.id,new_cat.id, guildID))
						await ctx.channel.send(embed=nextcord.Embed(description="<:voice:928259275401347105> Успешно!"))
					except:
						await ctx.channel.send(embed=nextcord.Embed(description="<:voice:928259275401347105> Ошибка! Вы ввели данные неверно!\nИспользуйте `?vc create` снова!"))
		else:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, только владелец может использовать эту команду!"))
		conn.commit()
		conn.close()

	@commands.command(aliases=['установить-лимит'])
	async def setlimit(self, ctx, num):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		if ctx.author.id == ctx.guild.owner.id:
			c.execute("SELECT * FROM guildSettings WHERE guildID = ?", (ctx.guild.id,))
			voice=c.fetchone()
			if voice is None:
				c.execute("INSERT INTO guildSettings VALUES (?, ?, ?)", (ctx.guild.id,f"Канал {ctx.author.name}",num))
			else:
				c.execute("UPDATE guildSettings SET channelLimit = ? WHERE guildID = ?", (num, ctx.guild.id))
			await ctx.send(embed=nextcord.Embed(description="<:voice:928259275401347105> Вы успешно изменили лимит!"))
		else:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, только владелец может использовать эту команду!"))
		conn.commit()
		conn.close()

	@create.error
	async def info_error(self, ctx, error):
		print(error)

	@vc.command(aliases=['заблокировать'])
	async def lock(self, ctx):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		id = ctx.author.id
		c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
		voice=c.fetchone()
		if voice is None:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, вы не владеете каналом."))
		else:
			channelID = voice[0]
			role = ctx.guild.default_role
			channel = self.client.get_channel(channelID)
			await channel.set_permissions(role, connect=False)
			await ctx.channel.send(embed=nextcord.Embed(description=f'<:voice:928259275401347105> {ctx.author.mention}, канал закрыт 🔒'))
		conn.commit()
		conn.close()

	@vc.command(aliases=['разблокировать'])
	async def unlock(self, ctx):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		id = ctx.author.id
		c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
		voice=c.fetchone()
		if voice is None:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, вы не владеете каналом."))
		else:
			channelID = voice[0]
			role = ctx.guild.default_role
			channel = self.client.get_channel(channelID)
			await channel.set_permissions(role, connect=True)
			await ctx.channel.send(embed=nextcord.Embed(description=f'<:voice:928259275401347105> {ctx.author.mention}, канал открыт 🔓'))
		conn.commit()
		conn.close()

	@vc.command(aliases=["allow", "позволить"])
	async def permit(self, ctx, member : nextcord.Member):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		id = ctx.author.id
		c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
		voice=c.fetchone()
		if voice is None:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, вы не владеете каналом."))
		else:
			channelID = voice[0]
			channel = self.client.get_channel(channelID)
			await channel.set_permissions(member, connect=True)
			await ctx.channel.send(embed=nextcord.Embed(description=f'<:voice:928259275401347105> {ctx.author.mention}, вы позволили {member.name} входить в ваш канал. ✅'))
		conn.commit()
		conn.close()

	@vc.command(aliases=["deny", "запретить"])
	async def reject(self, ctx, member : nextcord.Member):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		id = ctx.author.id
		guildID = ctx.guild.id
		c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
		voice=c.fetchone()
		if voice is None:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, вы не владеете каналом."))
		else:
			channelID = voice[0]
			channel = self.client.get_channel(channelID)
			for members in channel.members:
				if members.id == member.id:
					c.execute("SELECT voiceChannelID FROM guild WHERE guildID = ?", (guildID,))
					voice=c.fetchone()
					channel2 = self.client.get_channel(voice[0])
					await member.move_to(channel2)
			await channel.set_permissions(member, connect=False,read_messages=True)
			await ctx.channel.send(embed=nextcord.Embed(description=f'<:voice:928259275401347105> {ctx.author.mention}, вы запретили {member.name} входить в ваш канал. ❌'))
		conn.commit()
		conn.close()



	@vc.command(aliases=['лимит'])
	async def limit(self, ctx, limit):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		id = ctx.author.id
		c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
		voice=c.fetchone()
		if voice is None:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, вы не владеете каналом."))
		else:
			channelID = voice[0]
			channel = self.client.get_channel(channelID)
			await channel.edit(user_limit = limit)
			await ctx.channel.send(embed=nextcord.Embed(description=f'<:voice:928259275401347105> {ctx.author.mention}, вы установили лимит канала до '+ '{}!'.format(limit)))
			c.execute("SELECT channelName FROM userSettings WHERE userID = ?", (id,))
			voice=c.fetchone()
			if voice is None:
				c.execute("INSERT INTO userSettings VALUES (?, ?, ?)", (id,f'{ctx.author.name}',limit))
			else:
				c.execute("UPDATE userSettings SET channelLimit = ? WHERE userID = ?", (limit, id))
		conn.commit()
		conn.close()


	@vc.command(aliases=['имя'])
	async def name(self, ctx,*, name):
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		id = ctx.author.id
		c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
		voice=c.fetchone()
		if voice is None:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, вы не владеете каналом."))
		else:
			channelID = voice[0]
			channel = self.client.get_channel(channelID)
			await channel.edit(name = name)
			await ctx.channel.send(embed=nextcord.Embed(description=f'<:voice:928259275401347105> {ctx.author.mention}, вы изменили название своего канала на '+ '{}!'.format(name)))
			c.execute("SELECT channelName FROM userSettings WHERE userID = ?", (id,))
			voice=c.fetchone()
			if voice is None:
				c.execute("INSERT INTO userSettings VALUES (?, ?, ?)", (id,name,0))
			else:
				c.execute("UPDATE userSettings SET channelName = ? WHERE userID = ?", (name, id))
		conn.commit()
		conn.close()

	@vc.command(aliases=['забрать'])
	async def claim(self, ctx):
		x = False
		conn = sqlite3.connect('voice.db')
		c = conn.cursor()
		channel = ctx.author.voice.channel
		if channel == None:
			await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, вы не в голосовом канале."))
		else:
			id = ctx.author.id
			c.execute("SELECT userID FROM voiceChannel WHERE voiceID = ?", (channel.id,))
			voice=c.fetchone()
			if voice is None:
				await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, вы не можете стать владельцем этого канала!!"))
			else:
				for data in channel.members:
					if data.id == voice[0]:
						owner = ctx.guild.get_member(voice [0])
						await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, этот канал принадлежит {owner.mention}!"))
						x = True
				if x == False:
					await ctx.channel.send(embed=nextcord.Embed(description=f"<:voice:928259275401347105> {ctx.author.mention}, теперь вы владелец этого канала!"))
					c.execute("UPDATE voiceChannel SET userID = ? WHERE voiceID = ?", (id, channel.id))
			conn.commit()
			conn.close()


def setup(client):
	client.add_cog(voice(client))
