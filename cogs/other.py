import nextcord
from nextcord.ext import commands
from random import choice
import random
import io
import contextlib
from aioconsole import aexec

class Other(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command(aliases = ['generator','password','passwordgenerator', 'passwordgen', 'пароль'])
	
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def _pass(self, ctx,amt : int = None):
		if amt == None:
			await ctx.send(f"{ctx.author.mention}, укажите число символов!\nИспользование: `?password <число>`")
		elif amt <= 0:
			return await ctx.send(f"{ctx.author.mention}, отрицательное число нельзя!")
		elif amt > 200:
			return await ctx.send(f"{ctx.author.mention}, мне кажется, столь больших паролей не бывает >:/")
		try:
			password = ""
			all_char = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
			'n','o','p','q','r','s','t','u','v','w','x','y','z','!','@',
			'#','$','%','^','&','*','(',')','-','_','+','=','{',",",'}',']',
			'[',';',':','<','>','?','/','1','2','3','4','5','6','7','8','9','0'
			,'`','~','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P'
			,'Q','R','S','T','U','V','W','X','Y','Z']
			for x in range(amt):
				newpass = random.choice(all_char)
				password += newpass
			fnpss = ''.join(password)
			await ctx.send(f'{ctx.author.mention}, ваш пароль успешно сгенерирован и был отправлен вам в личные сообщения!')
			await ctx.author.send(f'Пароль сгенерирован: {fnpss}')
		except Exception as e:
			print(e) 


	@commands.command(aliases = ['код'])
	
	async def code(self, ctx, *, msg):
		await ctx.message.delete()
		embed = nextcord.Embed(title=f'Код {ctx.author.name}:', description="```py\n" + msg.replace("`", "") +("```"), color=ctx.author.color)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.is_owner()
	async def leave(self, ctx, *, guildinput):
		try:
			guildid = int(guildinput)
		except:
			await ctx.send("<a:checkoff:928259276273758208> Не удалось покинуть сервер!")
		try:
			guild = self.client.get_guild(guildid)
		except:
			await ctx.send("<a:checkoff:928259276273758208> Не удалось покинуть сервер!")
		try:
			await guild.leave()
			await ctx.send(f"{ctx.author.mention}, я покинула `{guild.name}`")
		except:
			await ctx.send("<a:checkoff:928259276273758208> Не удалось покинуть сервер!")

	@leave.error
	async def error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('<a:checkoff:928259276273758208> Эту команду может использовать только разработчик')

	@commands.command(name="banner", aliases = ['баннер'])
	async def server_banner(self, ctx, member: nextcord.Member = None):
		if member == None:
			if not ctx.guild.banner:
				return await ctx.send("У этого сервера нет баннера...")
			emb = nextcord.Embed(color=0x2F3136)
			emb.set_image(url=ctx.guild.banner.with_format('png'))
			await ctx.send(content=f"Баннер сервера **{ctx.guild.name}:**", embed=emb)
		else:
			try:
				user = await self.client.fetch_user(member.id)
				banner_url = user.banner.url
				emb = nextcord.Embed(color=0x2F3136)
				emb.set_image(url=banner_url)
				await ctx.send(content=f"Баннер пользователя **{member.name}:**", embed=emb)
			except Exception as error:
				await ctx.send('У этого пользователя нет баннера...')

	@commands.command(aliases = ['эмоджи-конверт'])
	async def econvert(self, ctx, emoji: nextcord.Emoji):
		embed = nextcord.Embed(title=emoji.name, description='Конвертирование произошло успешно!', color=0x2F3136)
		embed.set_image(url=emoji.url)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.is_owner()
	async def evlt(self, ctx, *, code):
		str_obj = io.StringIO() #Retrieves a stream of data
		try:
			with contextlib.redirect_stdout(str_obj):
				await aexec(code)
		except Exception as e:
			return await ctx.send(f"```{e.__class__.__name__}: {e}```")
		if not str_obj.getvalue():
			await ctx.send(f'Команда выполнена, сообщений нет!')
		else:
			await ctx.send(embed=nextcord.Embed(description=f'```py\nКоманда: {code}\nВывод:\n\n{str_obj.getvalue()}```', color=0x2F3136))

	@commands.command()
	@commands.is_owner()
	async def evl(self, ctx, *, code):
		str_obj = io.StringIO() #Retrieves a stream of data
		try:
			with contextlib.redirect_stdout(str_obj):
				await aexec(code)
		except Exception as e:
			return await ctx.send(f"```{e.__class__.__name__}: {e}```")
		if not str_obj.getvalue():
			await ctx.send(f'Команда выполнена, сообщений нет!')
		else:
			await ctx.send(embed=nextcord.Embed(description=f'```py\n{str_obj.getvalue()}```', color=0x2F3136))

def setup(client):
	client.add_cog(Other(client))