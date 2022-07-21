import nextcord
from nextcord.ext import commands
import wikipedia
class Wikipedia(commands.Cog, name ="Википедия"):
	def __init__(self,client):
		self.client = client

	@commands.command(pass_context = True, aliases=['вики'])
	
	@commands.cooldown(1, 5, commands.BucketType.guild)
	async def wiki(self,ctx, *search):
		message = await ctx.send(embed = nextcord.Embed(title ="Поиск и обработка...",colour = ctx.author.color))
		wikipedia.set_lang("ru")
		query = " ".join(search)
		searchs = wikipedia.search(query,results = 1)
		page = wikipedia.page(searchs)
		pagehtmldata = wikipedia.WikipediaPage(pageid = page.pageid)
		summary = page.summary
		cutted = f"{summary[:1000]} ..."
		embed = nextcord.Embed(title = page.original_title, description = cutted, colour = ctx.author.color,url = page.url)
		embed.set_thumbnail(url = pagehtmldata.images[0])
		embed.set_footer(text = f"Найдено по запросу: {query}")
		view = nextcord.ui.View()
		item = nextcord.ui.Button(style = nextcord.ButtonStyle.primary, label = "Читать дальше",emoji = "📖", url = page.url)
		view.add_item(item)
		await message.edit(embed =embed, view = view)

def setup(client):
	client.add_cog(Wikipedia(client))