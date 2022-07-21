import nextcord
import datetime
import random
import sqlite3

class TestCommand(nextcord.ui.View):
	def __init__(self, user:int):
		super().__init__(timeout=60)
		self.value = None
		self.user = user

	@nextcord.ui.button(label="Подтвердить", style=nextcord.ButtonStyle.green)
	async def testcmdd1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
		if interaction.user.id == self.user:
			await interaction.response.send_message("Вы успешно подтвердили своё действие!")
			self.value = True
			self.stop()
		else:
			await interaction.user.response.send_message("Вы не можете взаимодействовать с кнопкой, так как вы не вызали команду!", ephemeral=True)

	@nextcord.ui.button(label="Отклонить", style=nextcord.ButtonStyle.red)
	async def testcmdd2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
		if interaction.user.id == self.user:
			await interaction.response.send_message("Вы успешно отклонили своё действие!")
			self.value = False
			self.stop()
		else:
			await interaction.user.response.send_message("Вы не можете взаимодействовать с кнопкой, так как вы не вызали команду!", ephemeral=True)

class HelpCommand(nextcord.ui.Select):
	def __init__(self):

		selectOps = [
			nextcord.SelectOption(emoji="<:4246serverdiscovery:926412396967366666>", label='Сервер', description='Помощь по серверу и его настройкам.'),
			nextcord.SelectOption(emoji="<:6453banhammer:926414282072154123>", label='Модерация', description='Помощь по модерации.'),
			nextcord.SelectOption(emoji="<:9656stats:926412396992540702>", label='Утилиты', description='Помощь по утилитам.'),
			nextcord.SelectOption(emoji="<a:bob:928259277414604841>", label='Развлечения', description='Помощь по развлечениям.'),
			nextcord.SelectOption(emoji="<:8509peepohappygun:926415464303845386>", label='Картинки', description='Помощь по манипуляциям с картинками.'),
			nextcord.SelectOption(emoji="<a:pepedance:928259162503270440>", label='РП', description='Помощь по РП.'),
			nextcord.SelectOption(emoji="<:coinleafy:927841623667269663>", label='Экономика', description='Помощь по экономике.'),
			nextcord.SelectOption(emoji="<a:tadatada:928259276823224341>", label='Розыгрыши', description='Помощь по розыгрышам.'),
			nextcord.SelectOption(emoji="<a:wave1:929685841280897075>", label='Сообщения при входе-выходе', description='Помощь по приветственным каналам.'),
			nextcord.SelectOption(emoji="⬆️", label='Межсерверная система уровней', description='Помощь по системе уровней.'),
			nextcord.SelectOption(emoji="<:voice:928259275401347105>", label='Временный голосовой канал', description='Помощь по временном голосовом канале.'),
			nextcord.SelectOption(emoji="📖", label='Тэги', description='Помощь по тэгам.'),
			nextcord.SelectOption(emoji="<:2898picodediamante:939195860032577577>", label='Майнкрафт', description='Помощь по майнкрафт-экономике.')
		]
		super().__init__(placeholder='Выберите категорию', min_values=1, max_values=1, options=selectOps)

	async def callback(self, interaction: nextcord.Interaction):
		dbhelp = sqlite3.connect('server.db')
		cursorhelp = dbhelp.cursor()
		cursorhelp.execute("SELECT prefix FROM prefixes WHERE id = ?", (interaction.guild.id,))
		resulthelp = cursorhelp.fetchone()
		p = str(resulthelp[0])

		page1 = nextcord.Embed(title="<:4246serverdiscovery:926412396967366666> Сервер", description=f'**Страница #1**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page1.add_field(name=f'```{str(resulthelp[0])}help [помощь]```', value='```❓ Помощь по отдельной команде```', inline=True)
		page1.add_field(name=f'```{str(resulthelp[0])}lock [закрыть]```', value='```🔒 Заблокировать текущий канал```', inline=True)
		page1.add_field(name=f'```{str(resulthelp[0])}unlock [открыть]```', value='```🔓 Разблокировать текущий канал```', inline=False)
		page1.add_field(name=f'```{str(resulthelp[0])}tcreate [тсоздать]```', value='```✅ Создать текстовый канал```', inline=True)
		page1.add_field(name=f'```{str(resulthelp[0])}tremove [тудалить]```', value='```❎ Удалить текстовый канал```', inline=True)
		page1.add_field(name=f'```{str(resulthelp[0])}vcreate [всоздать]```', value='```✅ Создать голосовой канал```', inline=False)
		page1.add_field(name=f'```{str(resulthelp[0])}vremove [вудалить]```', value='```❎ Удалить голосовой канал```', inline=True)
		page1.add_field(name=f'```{str(resulthelp[0])}ccreate [ксоздать]```', value='```✅ Создать категорию```', inline=True)
		page1.add_field(name=f'```{str(resulthelp[0])}cremove [кудалить]```', value='```❎ Удалить категорию```', inline=False)
		page1.add_field(name=f'```{str(resulthelp[0])}setprefix [префикс]```', value='```⚙️ Изменить префикс бота на этом сервере```', inline=True)
		page1.add_field(name=f'```{str(resulthelp[0])}invite [пригласить]```', value='```▶️ Пригласить бота на сервер!```', inline=True)
		page1.add_field(name=f'```{str(resulthelp[0])}info [инфо]```', value='```🔨 Настройки текущего сервера```', inline=False)
		page1.add_field(name=f'```{str(resulthelp[0])}reactionrole [роли-по-реакции]```', value='```📘 Роли за реакции```', inline=False)

		page2 = nextcord.Embed(title="<:6453banhammer:926414282072154123> Модерация", description=f'**Страница #2**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page2.add_field(name=f'```{str(resulthelp[0])}clear [очистить]```', value='```🗑️ Очистка сообщений в чате```', inline=True)
		page2.add_field(name=f'```{str(resulthelp[0])}kick [кик]```', value='```🦵 Выгнать пользователя сервера```', inline=True)
		page2.add_field(name=f'```{str(resulthelp[0])}ban [бан]```', value='```🔨 Забанить пользователя сервера```', inline=False)
		page2.add_field(name=f'```{str(resulthelp[0])}unban [разбан]```', value='```⛏️ Разбанить пользователя сервера```', inline=True)
		page2.add_field(name=f'```{str(resulthelp[0])}mute [мьют]```', value='```🤐 Замутить пользователя```', inline=True)
		page2.add_field(name=f'```{str(resulthelp[0])}timeout add [таймаут добавить]```', value='```🤐 Выдать таймаут пользователю```', inline=False)
		page2.add_field(name=f'```{str(resulthelp[0])}timeout remove [таймаут убрать]```', value='```🤐 Снять таймаут пользователю```', inline=True)
		page2.add_field(name=f'```{str(resulthelp[0])}unmute [размьют]```', value='```😐 Размутить пользователя```', inline=True)
		page2.add_field(name=f'```{str(resulthelp[0])}slow [слоумод]```', value='```❄ Установить медленный режим```', inline=False)
		page2.add_field(name=f'```{str(resulthelp[0])}autorole add [авто-роль добавить]```', value='```📜 Добавить авто-роль```', inline=True)
		page2.add_field(name=f'```{str(resulthelp[0])}autorole reset [авто-роль убрать]```', value='```📜 Сбросить авто-роль```', inline=True)
		page2.add_field(name=f'```{str(resulthelp[0])}nick [ник]```', value='```📋 Сменить ник пользователя (для сброса: --reset)```', inline=False)
		page2.add_field(name=f'```{str(resulthelp[0])}automod link [авто-мод ссылка]```', value='```🤖 Бот удаляет все сообщения, которые содержат приглашения (кроме сообщений создателя)```', inline=False)

		page3 = nextcord.Embed(title="<:9656stats:926412396992540702> Утилиты", description=f'**Страница #3**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page3.add_field(name=f'```{str(resulthelp[0])}who [кто]```', value='```📲 Информация о пользователе!```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}help [помощь]```', value='```🗒 Вызывает это меню```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}server [сервер]```', value='```📋 Информация о сервере!```', inline=False)
		page3.add_field(name=f'```{str(resulthelp[0])}avatar [аватар]```', value='```🔗 Вывести аватар пользователя.```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}embed [вложение]```', value='```📜 Создать вложение. (<название> | <описание>)```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}ping [пинг]```', value='```🏓 Скорость отклика бота```', inline=False)
		page3.add_field(name=f'```{str(resulthelp[0])}yt [ютуб]```', value='```🔎 Поиск видео с YouTube```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}wiki [вики]```', value='```🔎 Поиск статьи на Wikipedia```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}invcount [приглашения]```', value='```🔨 Узнать сколько вы пригласили пользователей на этот сервер```', inline=False)
		page3.add_field(name=f'```{str(resulthelp[0])}mcstats [мкстата]```', value='```🧊 Поиск информации о игроке (Minecraft)```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}mchistory [мкистория]```', value='```🧊 Поиск истории ников игрока (Minecraft)```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}stats [статистика]```', value='```🤖 Статистика бота```', inline=False)
		page3.add_field(name=f'```{str(resulthelp[0])}devs [разработчики]```', value='```📋 Разработчики```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}banner [баннер]```', value='```🔗 Вывести баннер сервера```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}econvert [эмоджи-конверт]```', value='```💚 Конвертировать эмоджи в картинку```', inline=False)
		page3.add_field(name=f'```{str(resulthelp[0])}report [репорт]```', value='```😠 Пожаловаться на пользователя```', inline=True)
		page3.add_field(name=f'```{str(resulthelp[0])}suggest [предложить]```', value='```✋ Отправить сообщение разработчику```', inline=True)

		page4 = nextcord.Embed(title="<a:bob:928259277414604841> Развлечения", description=f'**Страница #4**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page4.add_field(name=f'```{str(resulthelp[0])}hello [привет]```', value='```👋 Привет, бот```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}8b [шар]```', value='```🎱 Магический шар```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}rickroll [риклолл]```', value='```💃 Never Gonna Give You Up```', inline=False)
		page4.add_field(name=f'```{str(resulthelp[0])}meme [мем]```', value='```😆 Время рандомных мемов с Reddit```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}fox [лиса]```', value='```🦊 Лисички!```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}uno [уно]```', value='```🗣 Говоришь на меня - переводишь на себя.```', inline=False)
		page4.add_field(name=f'```{str(resulthelp[0])}roll [кости]```', value='```🎲 Кинуть кости```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}coin [монетка]```', value='```🪙 Подбросить монетку```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}clove [совместимость]```', value='```💌 Проверить совместимость двух пользователей```', inline=False)
		page4.add_field(name=f'```{str(resulthelp[0])}code [код]```', value='```🤖 Отправить сообщение в стиле кода Python```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}password [пароль]```', value='```✋ Генератор паролей!```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}emoji [эмоджи]```', value='```🖼️ Найти эмоджи```', inline=False)
		page4.add_field(name=f'```{str(resulthelp[0])}elist [эмоджи-список]```', value='```😘 Загрузить список эмоджи```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}esearch [эмоджи-искать]```', value='```😐 Отправить три первые эмоджи```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}esteal [украсть-эмоджи]```', value='```💚 Украсть эмоджи с сервера```', inline=False)
		page4.add_field(name=f'```{str(resulthelp[0])}emojify [эмоджифай]```', value='```💚 Конвертировать текст в эмоджи```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}gen enable [ген включить]```', value='```✋ Включить авто-генерацию сообщений```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}gen disable [ген выключить]```', value='```😛 Выключить авто-генерацию сообщений```', inline=False)
		page4.add_field(name=f'```{str(resulthelp[0])}covid [ковид]```', value='```🖼️ Статистика Covid-19```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}joke [шутка]```', value='```🖼️ Рандомная шутка```', inline=True)
		page4.add_field(name=f'```{str(resulthelp[0])}paint [полотно]```', value='```🖌️ Создать полотно для рисования```', inline=False)
		page4.add_field(name=f'```Мой говорящий Бен!```', value='```.бен <вопрос>```', inline=False)

		page5 = nextcord.Embed(title="<:8509peepohappygun:926415464303845386> Картинки", description=f'**Страница #5**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page5.add_field(name=f'```{str(resulthelp[0])}wanted [розыск]```', value='```🖼️ Постер "Живым или мёртвым"```', inline=True)
		page5.add_field(name=f'```{str(resulthelp[0])}rip [могила]```', value='```🖼️ Могила```', inline=True)
		page5.add_field(name=f'```{str(resulthelp[0])}sponge [губка]```', value='```🖼️ Рядом с Губкой```', inline=False)
		page5.add_field(name=f'```{str(resulthelp[0])}wtf [что]```', value='```🖼️ WTF?```', inline=True)
		page5.add_field(name=f'```{str(resulthelp[0])}dog [пёс]```', value='```🖼️ Собака```', inline=True)
		page5.add_field(name=f'```{str(resulthelp[0])}cat [кот]```', value='```🖼️ Кошка```', inline=False)
		page5.add_field(name=f'```{str(resulthelp[0])}duck [утка]```', value='```🖼️ Утка```', inline=True)
		page5.add_field(name=f'```{str(resulthelp[0])}fire [пожар]```', value='```🖼️ Пожар```', inline=True)

		page6 = nextcord.Embed(title="<a:pepedance:928259162503270440> Roleplay", description=f'**Страница #6**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page6.add_field(name=f'```{str(resulthelp[0])}hug [обнять]```', value='```🤗 Обнять пользователя```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}kiss [поцеловать]```', value='```😘 Поцеловать пользователя```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}ghoul [гуль]```', value='```🖤 1000-7```', inline=False)
		page6.add_field(name=f'```{str(resulthelp[0])}lewd [смутиться]```', value='```🤭 Смутиться```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}slap [ударить]```', value='```🤜 Ударить пользователя```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}lick [лизнуть]```', value='```😛 Лизнуть пользователя```', inline=False)
		page6.add_field(name=f'```{str(resulthelp[0])}pat [погладить]```', value='```✋ Погладить пользователя```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}angry [злиться]```', value='```😠 Разозлиться на пользователя```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}custom [кастом]```', value='```🤖 Создать своё действие```', inline=False)
		page6.add_field(name=f'```{str(resulthelp[0])}feed [покормить]```', value='```🍕 Покормить пользователя```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}wag [хвост]```', value='```✨ Повилять хвостом```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}scream [кричать]```', value='```😱 Закричать```', inline=False)
		page6.add_field(name=f'```{str(resulthelp[0])}drunk [напиться]```', value='```🤤 Опьянеть```', inline=True)
		page6.add_field(name=f'```{str(resulthelp[0])}dance [танцевать]```', value='```💃 Танцевать```', inline=True)

		page7 = nextcord.Embed(title="<:coinleafy:927841623667269663> Экономика", description=f'**Страница #7**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page7.add_field(name=f'```{str(resulthelp[0])}bal [баланс]```', value='```🪙 Узнать баланс пользователя```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}bag [мешок]```', value='```🪙 Ежедневный мешок с деньгами```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}shop buy [магазин купить]```', value='```🪙 Купить роль с магазина```', inline=False)
		page7.add_field(name=f'```{str(resulthelp[0])}shop add [магазин добавить]```', value='```🪙 Добавить роль в магазин```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}shop remove [магазин убрать]```', value='```🪙 Убрать роль из магазина```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}shop [магазин]```', value='```🪙 Магазин```', inline=False)
		page7.add_field(name=f'```{str(resulthelp[0])}lb cash [лб наличные]```', value='```🪙 Таблица лидеров (наличные)```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}lb bank [лб банк]```', value='```🪙 Таблица лидеров (банк)```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}lb treasury [лб казна]```', value='```🪙 Таблица лидеров (казна)```', inline=False)
		page7.add_field(name=f'```{str(resulthelp[0])}send [отправить]```', value='```🪙 Перекинуть пользователю деньги```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}rob [ограбить]```', value='```🪙 Попытаться ограбить пользователя```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}deposit [депозит]```', value='```🪙 Положить деньги на банковский счёт```', inline=False)
		page7.add_field(name=f'```{str(resulthelp[0])}withdraw [снять]```', value='```🪙 Снять деньги с банковского счёта```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}slot [слоты]```', value='```🪙 Сыграть на слот-машине```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}guess [угадать]```', value='```🪙 Сыграть в игру чисел```', inline=False)
		page7.add_field(name=f'```{str(resulthelp[0])}robbery [ограбление]```', value='```🪙 Попытаться ограбить банк```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}work [работа]```', value='```🪙 Работа```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}treasury [казна]```', value='```🪙 Казна сервера```', inline=False)
		page7.add_field(name=f'```{str(resulthelp[0])}treasury take [казна взять]```', value='```🪙 Взять деньги с казны```', inline=True)
		page7.add_field(name=f'```{str(resulthelp[0])}treasury deposit [казна положить]```', value='```🪙 Положить деньги в казну```', inline=True)

		page8 = nextcord.Embed(title="<a:tadatada:928259276823224341> Розыгрыши", description=f'**Страница #8**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page8.add_field(name=f'```{str(resulthelp[0])}giveaway start [розыгрыш создать]```', value='```🎉 Начать розыгрыш```', inline=False)
		page8.add_field(name=f'```{str(resulthelp[0])}giveaway reroll [розыгрыш перевыбрать]```', value='```🎉 Выбрать нового победителя```', inline=True)

		page9 = nextcord.Embed(title="<a:wave1:929685841280897075> Сообщения при входе", description=f'**Страница #9**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page9.add_field(name=f'```{str(resulthelp[0])}welcome hellochannel [приветствия вход-канал]```', value='```👋 Установить канал при входе```', inline=True)
		page9.add_field(name=f'```{str(resulthelp[0])}welcome byechannel [приветствия выход-канал]```', value='```👋 Установить канал при выходе```', inline=True)
		page9.add_field(name=f'```{str(resulthelp[0])}welcome message [приветствия сообщение]```', value='```👋 Установить сообщение```', inline=False)
		page9.add_field(name=f'```{str(resulthelp[0])}welcome look [приветствия просмотр]```', value='```👋 Посмотреть как будут выглядеть сообщения```', inline=True)
		page9.add_field(name=f'```{str(resulthelp[0])}welcome reset [приветствия сбросить]```', value='```👋 Отключить сообщения```', inline=True)

		page10 = nextcord.Embed(title="⬆️ Межсерверная система уровней", description=f'**Страница #10**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)\n*Предоставленные ниже функции находятся в бета-тесте!*', color=0x2F3136)
		page10.add_field(name=f'```{str(resulthelp[0])}rank [ранг]```', value='```📜 Статистика пользователя```', inline=True)
		page10.add_field(name=f'```{str(resulthelp[0])}level enable [уровни включить]```', value='```📜 Включить систему уровней```', inline=True)
		page10.add_field(name=f'```{str(resulthelp[0])}level disable [уровни выключить]```', value='```📜 Отключить систему уровней```', inline=False)
		page10.add_field(name=f'```{str(resulthelp[0])}level channel [уровни канал]```', value='```📜 Установить канал для уведомлений```', inline=True)
		page10.add_field(name=f'```{str(resulthelp[0])}level dm [уровни лс]```', value='```📜 Установить ЛС как канал для уведомлений```', inline=True)
		page10.add_field(name=f'```{str(resulthelp[0])}level leaderboard [уровни лидеры]```', value='```📜 Вывести список лидеров```', inline=False)

		page11 = nextcord.Embed(title=f"<:voice:928259275401347105> Временный голосовой канал", description=f'**Страница #11**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page11.add_field(name=f'```{str(resulthelp[0])}vc create [гк создать]```', value='```🔊 Создать временный голосовой канал```', inline=True)
		page11.add_field(name=f'```{str(resulthelp[0])}vc setlimit [гк установить-лимит]```', value='```🔊 Установить лимит для всех каналов```', inline=True)
		page11.add_field(name=f'```{str(resulthelp[0])}vc lock [гк заблокировать]```', value='```🔊 Закрыть свой канал```', inline=False)
		page11.add_field(name=f'```{str(resulthelp[0])}vc unlock [гк разблокировать]```', value='```🔊 Открыть свой канал```', inline=True)
		page11.add_field(name=f'```{str(resulthelp[0])}vc limit [гк лимит]```', value='```🔊 Установить лимит для своего канала```', inline=True)
		page11.add_field(name=f'```{str(resulthelp[0])}vc name [гк имя]```', value='```🔊 Сменить имя своего канала```', inline=False)
		page11.add_field(name=f'```{str(resulthelp[0])}vc permit [гк позволить]```', value='```🔊 Позволить пользователю подключаться к вашему каналу```', inline=True)
		page11.add_field(name=f'```{str(resulthelp[0])}vc claim [гк забрать]```', value='```🔊 Стать владельцем пустого канала```', inline=True)
		page11.add_field(name=f'```{str(resulthelp[0])}vc reject [гк запретить]```', value='```🔊 Запретить пользователю подключаться к вашему каналу```', inline=False)

		page12 = nextcord.Embed(title="📖 Тэги", description=f'**Страница #12**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)\n*Предоставленные ниже функции находятся в бета-тесте!*', color=0x2F3136)
		page12.add_field(name=f'```{str(resulthelp[0])}tag [тэг]```', value='```📖 Вызвать тэг```', inline=True)
		page12.add_field(name=f'```{str(resulthelp[0])}tag add [тэг добавить]```', value='```📖 Добавить тэг```', inline=True)
		page12.add_field(name=f'```{str(resulthelp[0])}tag remove [тэг убрать]```', value='```📖 Убрать тэг```', inline=False)
		page12.add_field(name=f'```{str(resulthelp[0])}tag list [тэг список]```', value='```📖 Вывести список тэгов```', inline=True)

		page13 = nextcord.Embed(title="<:2898picodediamante:939195860032577577> Майнкрафт", description=f'**Страница #13**\n<:9969none:926414280394407947> Отдельная помощь по команде: `{str(resulthelp[0])}help <команда>`\n[Сайт](https://leafy.cf/)', color=0x2F3136)
		page13.add_field(name=f'```{str(resulthelp[0])}mine [копать]```', value='```⛏️ Пойти в шахту```', inline=True)
		page13.add_field(name=f'```{str(resulthelp[0])}furn [переплавить]```', value='```⛏️ Переплавить руду```', inline=True)
		page13.add_field(name=f'```{str(resulthelp[0])}convert [конверт]```', value='```⛏️ Конвертировать слитки в деньги```', inline=False)
		page13.add_field(name=f'```{str(resulthelp[0])}craft [крафт]```', value='```⛏️ Крафт```', inline=True)
		page13.add_field(name=f'```{str(resulthelp[0])}inventory [инвентарь]```', value='```⛏️ Инвентарь```', inline=True)
		page13.add_field(name=f'```{str(resulthelp[0])}coinsend [м-отправить]```', value='```⛏️ Отправить монеты другому пользователю```', inline=False)
		page13.add_field(name=f'```{str(resulthelp[0])}leaders [лидеры]```', value='```⛏️ Список лидеров на вашем сервере```', inline=True)
		page13.add_field(name=f'```{str(resulthelp[0])}oreshop [м-магазин]```', value='```⛏️ Вывести магазин ролей```', inline=True)
		page13.add_field(name=f'```{str(resulthelp[0])}oreshop add [м-магазин добавить]```', value='```⛏️ Добавить роль в магазин```', inline=False)
		page13.add_field(name=f'```{str(resulthelp[0])}oreshop remove [м-магазин убрать]```', value='```⛏️ Убрать роль с магазина```', inline=True)
		page13.add_field(name=f'```{str(resulthelp[0])}oreshop buy [м-магазин купить]```', value='```⛏️ Купить роль с магазина```', inline=True)

		if self.values[0] == 'Сервер':
			return await interaction.response.edit_message(embed=page1)
		elif self.values[0] == 'Модерация':
			return await interaction.response.edit_message(embed=page2)
		elif self.values[0] == 'Утилиты':
			return await interaction.response.edit_message(embed=page3)
		elif self.values[0] == 'Развлечения':
			return await interaction.response.edit_message(embed=page4)
		elif self.values[0] == 'Картинки':
			return await interaction.response.edit_message(embed=page5)
		elif self.values[0] == 'РП':
			return await interaction.response.edit_message(embed=page6)
		elif self.values[0] == 'Экономика':
			return await interaction.response.edit_message(embed=page7)
		elif self.values[0] == 'Розыгрыши':
			return await interaction.response.edit_message(embed=page8)
		elif self.values[0] == 'Сообщения при входе-выходе':
			return await interaction.response.edit_message(embed=page9)
		elif self.values[0] == 'Межсерверная система уровней':
			return await interaction.response.edit_message(embed=page10)
		elif self.values[0] == 'Временный голосовой канал':
			return await interaction.response.edit_message(embed=page11)
		elif self.values[0] == 'Тэги':
			return await interaction.response.edit_message(embed=page12)
		elif self.values[0] == 'Майнкрафт':
			return await interaction.response.edit_message(embed=page13)

class HelpCommandView(nextcord.ui.View):
	def __init__(self):
		super().__init__()
		self.add_item(HelpCommand())



class DevelopersCommand(nextcord.ui.Select):
	def __init__(self):

		selectOps = [
			nextcord.SelectOption(emoji="<:vsparkles:935247052642852884>", label='Разработчики', description='Мы разрабатываем Leafy!'),
			nextcord.SelectOption(emoji="🎟️", label='Администраторы', description='Администраторы сервера поддержки!')
		]
		super().__init__(placeholder='Выберите категорию', min_values=1, max_values=1, options=selectOps)

	async def callback(self, interaction: nextcord.Interaction):
		embed1=nextcord.Embed(title='Разработчики',  description='Мы разрабатываем Leafy!\n[Сервер поддержки](https://discord.gg/CT8VekA57Z)', color=0x2F3136)
		embed1.add_field(name='#1 | mqchinee#1422', value='Статус: `Создатель`\nКомментарий: `Надеюсь, вам нравится Лифи!`')
		embed1.set_thumbnail(url='https://cdn.discordapp.com/avatars/748494305005535253/9f9d0a5927b00f4916c0e6f6b1456779.png?size=1024')

		embed2=nextcord.Embed(title='Администраторы',  description='Мы модерируем сервер поддержки!\n[Сервер поддержки](https://discord.gg/CT8VekA57Z)', color=0x2F3136)
		embed2.add_field(name='#1 | iron ougi#5391', value='Статус: `Администратор`\nКомментарий: `Я гений, вопросы?`')

		if self.values[0] == 'Разработчики':
			return await interaction.response.edit_message(embed=embed1)
		elif self.values[0] == 'Администраторы':
			return await interaction.response.edit_message(embed=embed2)

class DevelopersCommandView(nextcord.ui.View):
	def __init__(self):
		super().__init__()
		self.add_item(DevelopersCommand())