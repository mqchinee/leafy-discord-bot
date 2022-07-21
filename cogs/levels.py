import nextcord
import json
import sqlite3

from nextcord import File
from nextcord.ext import commands
from typing import Optional
from easy_pil import Editor, load_image_async, Font
from nextcord.ext.commands import has_permissions, MissingPermissions, cooldown, BucketType

class Levelsys(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_message(self, message):
    leveldb = sqlite3.connect("levellog.db")
    lvlcursor = leveldb.cursor()
    lvlcursor.execute("SELECT disabled_id FROM disable WHERE disabled_id = ?", (message.guild.id,))
    lvlresult = lvlcursor.fetchone()

    if not lvlresult:
        if not message.content.startswith("?"):

      
          if not message.author.bot:
            with open("levels.json", "r") as f:
              data = json.load(f)
            
            #checking if the user's data is already there in the file or not
            if str(message.author.id) in data:
              xp = data[str(message.author.id)]['xp']
              lvl = data[str(message.author.id)]['level']

              #increase the xp by the number which has 100 as its multiple
              increased_xp = xp+5
              new_level = int(increased_xp/100)

              data[str(message.author.id)]['xp']=increased_xp

              with open("levels.json", "w") as f:
                json.dump(data, f)

              if new_level > lvl:
                logdb = sqlite3.connect("levellog.db")
                logcursor = logdb.cursor()
                logcursor.execute("SELECT channel_log FROM log WHERE guild_log = ?", (message.guild.id,))
                logresult = logcursor.fetchone()
                if not logresult:
                    if message.guild.icon:
                      embed = nextcord.Embed(title='Повышение уровня', description=f"{message.author.mention}, вы повысили свой уровень!", color=nextcord.Colour.yellow())
                      embed.add_field(name='Новый уровень:', value=new_level)
                      embed.add_field(name='Сервер:', value=message.author.guild.name)
                      embed.set_thumbnail(url=message.author.guild.icon)
                    else:
                      embed = nextcord.Embed(title='Повышение уровня', description=f"{message.author.mention}, вы повысили свой уровень!", color=nextcord.Colour.yellow())
                      embed.add_field(name='Новый уровень:', value=new_level)
                      embed.add_field(name='Сервер:', value=message.author.guild.name)
                    await message.author.send(embed=embed)
                else:
                    embed = nextcord.Embed(title='Повышение уровня', description=f"{message.author.mention}, вы повысили свой уровень!", color=nextcord.Colour.yellow())
                    embed.add_field(name='Новый уровень:', value=new_level)
                    channel = self.client.get_channel(int(logresult[0]))
                    await channel.send(embed=embed)

                data[str(message.author.id)]['level']=new_level
                data[str(message.author.id)]['xp']=0

                with open("levels.json", "w") as f:
                  json.dump(data, f)
            else:
              data[str(message.author.id)] = {}
              data[str(message.author.id)]['xp'] = 0
              data[str(message.author.id)]['level'] = 1

              with open("levels.json", "w") as f:
                json.dump(data, f)

    else:
        return

  @commands.command(aliases=["ранг"])
  async def rank(self, ctx: commands.Context, user: Optional[nextcord.Member]):
    leveldb = sqlite3.connect("levellog.db")
    lvlcursor = leveldb.cursor()
    lvlcursor.execute("SELECT disabled_id FROM disable WHERE disabled_id = ?", (ctx.guild.id,))
    lvlresult = lvlcursor.fetchone()

    if not lvlresult:
        userr = user or ctx.author

        with open("levels.json", "r") as f:
          data = json.load(f)

        xp = data[str(userr.id)]["xp"]
        lvl = data[str(userr.id)]["level"]

        next_level_xp = (lvl+1) * 100
        xp_need = next_level_xp
        xp_have = data[str(userr.id)]["xp"]

        percentage = int(((xp_have * 100)/ xp_need))

        if percentage < 1:
          percentage = 0
        
        ## Rank card
        background = Editor(f"IMG/zIMAGE3.png")
        profile = await load_image_async(str(userr.display_avatar))

        profile = Editor(profile).resize((150, 150)).circle_image()
        
        poppins = Font("fonts/sans.otf", size=40)
        poppins_small = Font.poppins(size=30)

        #you can skip this part, I'm adding this because the text is difficult to read in my selected image
        ima = Editor("IMG/zBLACK.png")
        background.blend(image=ima, alpha=.5, on_top=False)

        background.paste(profile.image, (30, 30))

        background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percentage,
            fill="#4f4d4d",
            radius=20,
        )
        background.text((200, 55), str(userr.name), font=poppins, color="#ffffff")

        background.rectangle((200, 100), width=350, height=2, fill="#ffffff")
        background.text(
            (200, 120),
            f"LVL : {lvl}   "
            + f" XP : {xp} / {(lvl+1) * 100}",
            font=poppins_small,
            color="#ffffff",
        )

        card = File(fp=background.image_bytes, filename="IMG/zCARD.png")
        await ctx.reply(file=card)

    else:
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nсистема уровней отключена на этом сервере.\n`Включить: level enable`')
        return await ctx.send(embed=embi)

    
  @commands.group(aliases = ['уровни'])
  async def level(self, ctx):
    pass

  @level.command(aliases = ['выключить'])
  @commands.has_permissions(administrator=True)
  async def disable(self, ctx):
    db = sqlite3.connect("levellog.db")
      
    cursor = db.cursor()
    cursor.execute("SELECT disabled_id FROM disable WHERE disabled_id = ?", (ctx.guild.id,))
    result = cursor.fetchone()
    if result:
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nсистема уровней уже отключена на этом сервере.\n`Включить: level enable`', color=0x2F3136)
        await ctx.send(embed=embi)
    else:
        cursor.execute("INSERT INTO disable(disabled_id) VALUES(?)", (ctx.guild.id,))
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nсистема уровней была успешно отключена на этом сервере.\n`Включить: level enable`', color=0x2F3136)
        await ctx.send(embed=embi)
    db.commit()
    cursor.commit()
    cursor.close()
    db.close()

  @level.command(aliases = ['включить'])
  @commands.has_permissions(administrator=True)
  async def enable(self, ctx):
    db = sqlite3.connect("levellog.db")
    cursor = db.cursor()
    cursor.execute("SELECT disabled_id FROM disable WHERE disabled_id = ?", (ctx.guild.id,))
    result = cursor.fetchone()
    if not result:
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nсистема уровней уже была успешно включена на этом сервере.\n`Выключить: level disable`', color=0x2F3136)
        await ctx.send(embed=embi)
    else:
        cursor.execute("DELETE FROM disable WHERE disabled_id = ?", (ctx.guild.id,))
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nсистема уровней была успешно включена на этом сервере.\n`Выключить: level disable`', color=0x2F3136)
        await ctx.send(embed=embi)
    db.commit()
    cursor.commit()
    cursor.close()
    db.close()

  @level.command(aliases = ['канал'])
  @commands.has_permissions(administrator=True)
  async def channel(self, ctx, channel:nextcord.TextChannel):
    db = sqlite3.connect("levellog.db")
    cursor = db.cursor()
    cursor.execute("SELECT channel_log FROM log WHERE guild_log = ?", (ctx.guild.id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO log(channel_log, guild_log) VALUES(?,?)", (channel.id, ctx.guild.id,))
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nканал для уведомлений был установлен как:\n{channel.mention}', color=0x2F3136)
        await ctx.send(embed=embi)
    else:
        cursor.execute("UPDATE log SET channel_log = ? WHERE guild_log = ?", (channel.id, ctx.guild.id,))
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nканал для уведомлений был установлен как:\n{channel.mention}', color=0x2F3136)
        await ctx.send(embed=embi)
        
    db.commit()
    cursor.commit()
    cursor.close()
    db.close()

  @level.command(aliases = ['лс'])
  @commands.has_permissions(administrator=True)
  async def dm(self, ctx):
    db = sqlite3.connect("levellog.db")
    cursor = db.cursor()
    cursor.execute("SELECT channel_log FROM log WHERE guild_log = ?", (ctx.guild.id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("DELETE FROM log WHERE guild_log = ?", (ctx.guild.id,))
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nканал для уведомлений был установлен как:\n`Личные сообщения`', color=0x2F3136)
        await ctx.send(embed=embi)
    else:
        embi = nextcord.Embed(title="Ранг", description=f'{ctx.author.mention},\nканал для уведомлений уже был установлен как:\n`Личные сообщения`', color=0x2F3136)
        await ctx.send(embed=embi)
    db.commit()
    cursor.commit()
    cursor.close()
    db.close()

  @level.command(aliases=['лидеры'])
  async def leaderboard(self, ctx, range_num=12):
    with open ("levels.json", "r") as f:
        data = json.load(f)

    async with ctx.channel.typing():

        l = {}
        total_xp = []

        for userid in data:
            xp = int(data[str(userid)]['xp']+(int(data[str(userid)]['level'])*100))

            l[xp] = f"{userid};{data[str(userid)]['xp']};{data[str(userid)]['level']}"
            total_xp.append(xp)

        total_xp = sorted(total_xp, reverse=True)
        index=1

        mbed = nextcord.Embed(title='Список лидеров', color=nextcord.Colour.yellow())

        for amt in total_xp:
            id_ = int(str(l[amt]).split(";")[0])
            level = int(str(l[amt]).split(";")[1])
            xp = int(str(l[amt]).split(";")[2])

            member = await self.client.fetch_user(id_)

            if member is not None:
                name = member
                mbed.add_field(name=f"{index}. {name}", value=f"**Уровень:** {xp} | **Опыт:** {level}", inline=True)

                if index == range_num:
                    break
                else:
                    index += 1

        await ctx.send(embed=mbed)

def setup(client):
  client.add_cog(Levelsys(client))