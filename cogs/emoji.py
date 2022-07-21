import nextcord
from nextcord.ext import commands
import httpx as requests
from bs4 import BeautifulSoup as bs
import random



class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['emoji', 'эмоджи'])
    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def emoji__(self, ctx, *, message):
        URL = f"https://slackmojis.com/emojis/search?utf8=%E2%9C%93&authenticity_token=8OgBpTphVqlDDugOXU6J6IBtDdXBCdtVhg3VDCEHCTdTt7TSn5vQNha%2BoJkhDbmGkow8Tvk8d%2FiBmanqQeP%2Bdg%3D%3D&query={message}"
        response = requests.get(URL)

        if response.status_code == 200:
            soup = bs(response.text)
            images = []

            for img in soup.find_all('img'):
                images.append(img['src'])

            if len(images) != 0 and not nsfw_check(images):
                messagee = nextcord.Embed(title=f'Эмоджи: {message}', color=0x2F3136)
                messagee.set_image(url=random.choice(images))
                await ctx.send(embed=messagee)
            else:
                await ctx.send("Ничего не найдено!")
        else:
            await ctx.send("Ничего не найдено!")


    @commands.command(aliases = ['эмоджи-искать'])
    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def esearch(self, ctx, *, search):
        URL = f"https://slackmojis.com/emojis/search?utf8=%E2%9C%93&authenticity_token=8OgBpTphVqlDDugOXU6J6IBtDdXBCdtVhg3VDCEHCTdTt7TSn5vQNha%2BoJkhDbmGkow8Tvk8d%2FiBmanqQeP%2Bdg%3D%3D&query={search}"
        response = requests.get(URL)

        if response.status_code == 200:
            soup = bs(response.text)

            images = []
            titles = []

            for img in soup.find_all('img'):
                images.append(img['src'])
                title = img['alt'].replace(' random', '')
                titles.append(title)
                more_than_5 = True

            if len(images) == 0:
                await ctx.send("Ничего не найдено!")
            elif not nsfw_check(images):
                for i in range(3):
                    message = nextcord.Embed(title=titles[i].title(), color=0x2F3136)
                    message.set_image(url=images[i])
                    message.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
                    await ctx.send(embed=message)

                    if i == len(images) - 1:
                        more_than_5 = False
                        break

                if more_than_5:
                    await ctx.send(f"Пожалуйста, напишите `?elist {search}`, чтобы получить полный список эмоджи!")
            else:
                message = nextcord.Embed(title="Зацензурено!", color=0x2F3136)
                message.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
                await ctx.send(embed=message)


    @commands.command(aliases = ['эмоджи-список'])
    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def elist(self, ctx, *, search):
        URL = f"https://slackmojis.com/emojis/search?utf8=%E2%9C%93&authenticity_token=8OgBpTphVqlDDugOXU6J6IBtDdXBCdtVhg3VDCEHCTdTt7TSn5vQNha%2BoJkhDbmGkow8Tvk8d%2FiBmanqQeP%2Bdg%3D%3D&query={search}"
        response = requests.get(URL)

        if response.status_code == 200:
            soup = bs(response.text)
            images = []
            titles = []

            common = "random"

            for img in soup.find_all('img'):
                images.append(img['src'])
                title = img['alt'].replace(" random", '')
                titles.append(title)

            if not nsfw_check(images):
                message = nextcord.Embed(title="Результат:", color=0x2F3136)
                message.add_field(name=search.title(), value=", ".join(list(set(titles))))
                message.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)
                
            else:
                message = nextcord.Embed(title="Зацензурено!")
                message.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar)

            await ctx.send(embed=message)

    @commands.command(aliases=['efy', 'эмоджифай'])
    async def emojify(self, ctx, *, text):
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {'0':'zero',
                '1':'one',
                '2':'two',
                '3':'three',
                '4':'four',
                '5':'five',
                '6':'six',
                '7':'seven',
                '8':'eight',
                '9':'nine'}
                emojis.append(f":{num2emo.get(s)}:")
            elif s.isalpha():
                ru2emo = {
                'а':':regional_indicator_a:',
                'б':'<:6zFbn1o:932255578259070977>',
                'в':':regional_indicator_b:',
                'г':'<:AZ3K7oa:932255578452004934>',
                'д':'<:NOzIw7D:932255578489778186>',
                'е':':regional_indicator_e:',
                'ё':':regional_indicator_e:',
                'ж':'<:568Fpyq:932255578275872838>',
                'з':'<:z_:932255578644955207>',
                'и':'<:2MzCiXr:932255578233917450>',
                'й':'<:qM9pJmS:932255578472996874>',
                'к':':regional_indicator_k:',
                'л':'<:YrbtaFC:932255578565279744>',
                'м':':regional_indicator_m:',
                'н':':regional_indicator_h:',
                'о':':regional_indicator_o:',
                'п':'<:cd3Sm5j:932255578355556382>',
                'р':':regional_indicator_p:',
                'с':':regional_indicator_c:',
                'т':':regional_indicator_t:',
                'у':':regional_indicator_y:',
                'ф':'<:L8W6M8t:932255578275852289>',
                'х':':regional_indicator_x:',
                'ц':'<:tpXAWvG:932255578670104596>',
                'ч':'<:odw6QSU:932255578632359976>',
                'ш':'<:dFVzp9g:932255578137432125>',
                'щ':'<:LwbCDE2:932255578460389396>',
                'ъ':'<:IlCHUXu:932255578426863666>',
                'ы':'<:H8i7po5:932255578431049808>',
                'ь':'<:kpHU6Hl:932255579181826058>',
                'э':'<:OTyUw4y:932255578691092480>',
                'ю':'<:lB0RHl8:932255578414272522>',
                'я':'<:4fV3xYI:932255578099683419>',
                'a':':regional_indicator_a:',
                'b':':regional_indicator_b:',
                'c':':regional_indicator_c:',
                'd':':regional_indicator_d:',
                'e':':regional_indicator_e:',
                'f':':regional_indicator_f:',
                'g':':regional_indicator_g:',
                'h':':regional_indicator_h:',
                'i':':regional_indicator_i:',
                'j':':regional_indicator_j:',
                'k':':regional_indicator_k:',
                'l':':regional_indicator_l:',
                'm':':regional_indicator_m:',
                'n':':regional_indicator_n:',
                'o':':regional_indicator_o:',
                'p':':regional_indicator_p:',
                'q':':regional_indicator_q:',
                'r':':regional_indicator_r:',
                's':':regional_indicator_s:',
                't':':regional_indicator_t:',
                'u':':regional_indicator_u:',
                'v':':regional_indicator_v:',
                'w':':regional_indicator_w:',
                'x':':regional_indicator_x:',
                'y':':regional_indicator_y:',
                'z':':regional_indicator_z:'
                }
                emojis.append(f"{ru2emo.get(s)}")
            else:
                emojis.append(s)
        await ctx.send(' '.join(emojis))


def setup(client):
    client.add_cog(Fun(client))

def nsfw_check(images):
    nsfw_links = {'https://emojis.slackmojis.com/emojis/images/1528400660/4042/boob.png?1528400660',
                  'https://emojis.slackmojis.com/emojis/images/1533408970/4386/dildo.png?1533408970',
    }

    images = set(images)
    common = nsfw_links.intersection(images)
    if len(common) != 0: return True
    else: return False
