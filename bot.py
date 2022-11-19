# -*- coding: utf-8 -*-s
import telebot
from telebot import types
from player import Player
from emailsend import PlayerEmail
from emailsend import RegularEmail
from datetime import datetime

from usercache import UserCache

#Экземпляр бота
bot = telebot.TeleBot('INPUT_YOUR_TOKEN')

#Текст для кнопок  
item1text = "Дозаявить/отзаявить игрока"
item2text = "Обращение/протест/апелляция (от лица команды)"
#item3text = "Задать вопрос"
item4text = "Предложить идею/жалоба (можно анонимно)"
item5text = "Таблицы/календари/статистика/составы"
item6text = "Документы"
#item7text = "Заполнить протокол"
item8text = "Контакты"
#item9text = "Подписаться на рассылку"
item10text = "Изменить контактные данные"

users = []

def check_user(message):
    flag = False
    for user in users:
        if user.user_id == message.chat.id:
            flag = True
    if not flag:
        user = UserCache(message.chat.id, senderinfo="", players=[], attachments=[])
        users.append(user)
        

def get_user(message):
    for user in users:
        if message.chat.id == user.user_id:
            return user


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    check_user(message)
    startprocedure(message)

# Выводит клаву с кнопками   
def startprocedure(message):
    
    # Добавляем кнопки
    mainmarkup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton(item1text)
    item2=types.KeyboardButton(item2text)
    #item3=types.KeyboardButton(item3text)
    item4=types.KeyboardButton(item4text)
    item5=types.KeyboardButton(item5text)
    item6=types.KeyboardButton(item6text)
    #item7=types.KeyboardButton(item7text)
    item8=types.KeyboardButton(item8text)
    #item9=types.KeyboardButton(item9text)
    item10=types.KeyboardButton(item10text)

    mainmarkup.add(item1)
    mainmarkup.add(item2)
    #mainmarkup.add(item3)  
    mainmarkup.add(item4)
    mainmarkup.add(item5)
    mainmarkup.add(item6)
    #mainmarkup.add(item7)
    mainmarkup.add(item8)
    #mainmarkup.add(item9)
    mainmarkup.add(item10)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup = mainmarkup)
    
    #Очистка
    check_user(message)
    for user in users:
        if message.chat.id == user.user_id:
            user.senderinfo = ""
            user.vidobr = ""
            user.body = ""
            if len(user.attachments) > 0: 
                user.attachments.clear()
            user.league_name = ""
            user.team_name = ""
            user.z_type = ""
            user.fio = ""
            user.playerdate = ""
            user.position = ""
            if len(user.players) > 0: 
                user.players.clear()
            user.is_anon = False
            user.is_team = False
        
    bot.register_next_step_handler(message, message_reply)    
    
#Обработка клавиатуры старта
@bot.message_handler(content_types='text')
def message_reply(message): 
    check_user(message)
    user = get_user(message)
    #Дозаявить/отзаявить игрока
    if message.text == item1text:
        if len(user.senderinfo) < 1:
            bot.reply_to(message, "Введите свою эл. почту:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, item1_message_hndlr)    
        else:
            item1_message_hndlr(message)
    #Обращение/протест/апелляция
    elif message.text == item2text:
        if len(user.senderinfo) < 1:
            bot.reply_to(message, "Введите свою эл. почту:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, item2_message_hndlr)    
        else:
            item2_message_hndlr(message)
    #Задать вопрос
    #elif message.text == item3text:
    #    if len(user.senderinfo) < 1:
    #        bot.reply_to(message, "Введите свою эл. почту (для обратной связи):", reply_markup=types.ReplyKeyboardRemove())
    #        bot.register_next_step_handler(message, item3_message_hndlr)
    #    else:
    #       item3_message_hndlr(message)
    #Предложить идею/жалоба (можно анонимно)
    elif message.text == item4text:
        bot.reply_to(message, "Введите свою эл. почту или напишите \"Анонимно\":", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, item4_message_hndlr)
    #Таблицы/календари/статистика/составы
    elif message.text == item5text:
        item5_message_hndlr(message)
    #Документы
    elif message.text == item6text:
        item6_message_hndlr(message)
    #Заполнить протокол
    #elif message.text == item7text:
    #    item7_message_hndlr(message)
    #Контакты
    elif message.text == item8text:
        item8_message_hndlr(message)
    #Подписаться на рассылку
    #elif message.text == item9text:
    #    item9_message_hndlr(message)  
    #Переделать контактные данные
    elif message.text == item10text:
        bot.reply_to(message, "Введите эл. почту:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, item10_message_hndlr)
        
        
#####################################################################################   
#Если выбрана опция "Дозаявить/отзаявить игрока"
#####################################################################################   

#Обработка опции "Дозаявить/отзаявить игрока"
@bot.message_handler(content_types='text')
def item1_message_hndlr(message): 
    #Проверка наличия данных о пользователе
    check_user(message)
    user = get_user(message)
    if len(user.senderinfo) < 1:
        user.senderinfo = message.text
    # Добавляем кнопки быстрого ввода текста
    bot.reply_to(message, "Количество игроков в заявке не должно превышать 25 человек. Пожалуйста, проверьте заявку своей команды перед внесением изменений:\nhttps://bmfl.ru/%d0%be%d0%bf%d0%bb/:", reply_markup=types.ReplyKeyboardRemove()) 
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('БМФЛЛ')
    item2=types.KeyboardButton('ЖМФЛЛ')
    item3=types.KeyboardButton('МЛФЛ')
    item4=types.KeyboardButton('ЭМФЛЛ')
    item5=types.KeyboardButton('МФЛЛНР')
    item6=types.KeyboardButton('Вернуться на главное меню')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    markup.add(item6)
    bot.reply_to(message, "Введите название лиги:", reply_markup=markup)    
    bot.register_next_step_handler(message, league_name_message_hndlr) #Следующий шаг, обработка выбора лиги
            
#Обработка выбора лиги
@bot.message_handler(content_types='text')
def league_name_message_hndlr(message): 
    #Проверка корректности ввода лиги
    check_user(message)
    user = get_user(message)
    leagues = ['БМФЛЛ', 'ЖМФЛЛ', 'МЛФЛ', 'ЭМФЛЛ', 'МФЛЛНР']
    league_input = str(message.text).strip().upper()
    #Если корректно, пользователь вводит название команды
    if league_input in leagues:
        user.league_name = league_input
        bot.reply_to(message, "Введите название команды:", reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, team_name_message_hndlr) #Обработка ввода названия команды
    #Если выбрано "Вернуться на главное меню"
    elif message.text == 'Вернуться на главное меню':
        startprocedure(message)
    #Если некорректно, вводит лигу еще раз, клавиатура заново появляется на экране
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('БМФЛЛ')
        item2=types.KeyboardButton('ЖМФЛЛ')
        item3=types.KeyboardButton('МЛФЛ')
        item4=types.KeyboardButton('ЭМФЛЛ')
        item5=types.KeyboardButton('МФЛЛНР')
        item6=types.KeyboardButton('Вернуться на главное меню')  
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)    
        markup.add(item6)
        bot.reply_to(message, "Введите корректное название лиги из представленного списка:", reply_markup=markup)  
        bot.register_next_step_handler(message, league_name_message_hndlr) #Обработка выбора лиги

#Обработка ввода названия команды
@bot.message_handler(content_types='text')
def team_name_message_hndlr(message): 
    check_user(message)
    user = get_user(message)
    user.team_name = message.text
    # Добавляем кнопки
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('Заявка')
    item2=types.KeyboardButton('Отзаявка')
    item3=types.KeyboardButton('Вернуться на главное меню')  
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.reply_to(message, "Заявка/отзаявка:", reply_markup = markup)
    bot.register_next_step_handler(message, zayavka_message_handler) #Обработка типа заявки

#Обработка типа заявки
@bot.message_handler(content_types='text')
def zayavka_message_handler(message): 
    check_user(message)
    user = get_user(message)
    if message.text == 'Заявка':
        user.z_type = 'Заявка'
        bot.reply_to(message, "Введите полностью фамилию имя и отчество игрока:", reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, fio_message_hndlr) #Обработка ФИО
    elif message.text == 'Отзаявка':
        user.z_type = 'Отзаявка'
        bot.reply_to(message, "Введите полностью фамилию имя и отчество игрока:", reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, fio_message_hndlr) #Обработка ФИО
    elif message.text == 'Вернуться на главное меню (письмо отправится на состояние последнего добавленного игрока)':
        player_email = PlayerEmail(f'{user.league_name} {user.team_name}', user.senderinfo, user.players)
        player_email.sendEmail()
        bot.send_message(message.chat.id, "Письмо отправлено.", reply_markup=types.ReplyKeyboardRemove())
        startprocedure(message)
    elif message.text == 'Вернуться на главное меню (письмо не отправится)':
        startprocedure(message)
    elif message.text == 'Вернуться на главное меню':
        startprocedure(message)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('Заявка')
        item2=types.KeyboardButton('Отзаявка')    
        item3=types.KeyboardButton('Вернуться на главное меню')  
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.reply_to(message, "Введите корректный тип заявки:", reply_markup = markup)
        bot.register_next_step_handler(message, zayavka_message_handler) #Обработка типа заявки
    
#Обработка ФИО
@bot.message_handler(content_types='text')
def fio_message_hndlr(message):
    check_user(message)
    user = get_user(message)
    user.fio = message.text
    #Заявка
    if user.z_type == 'Заявка':
        bot.reply_to(message, "Введите дату рождения игрока:")
        bot.register_next_step_handler(message, date_message_hndlr)
    #Отзаявка
    else:
        user.players.append(Player(user.z_type, user.fio, None, None, None))
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('Да')
        item2=types.KeyboardButton('Отправить заявку')
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, "Дозаявить/отзаявить еще одного игрока?", reply_markup=markup)
        bot.register_next_step_handler(message, handle_continue_yes_no)

#Амплуа
@bot.message_handler(content_types='text')
def date_message_hndlr(message):
    global playerdate
    playerdate = message.text
    # Добавляем кнопки
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('ВРТ')
    item2=types.KeyboardButton('ЗАЩ')
    item3=types.KeyboardButton('ПЗЩ')
    item4=types.KeyboardButton('НАП')
    item5=types.KeyboardButton('Вернуться на главное меню')  
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.reply_to(message, "Введите амплуа игрока:", reply_markup = markup)
    bot.register_next_step_handler(message, position_message_hndlr)

#Отправление фото
@bot.message_handler(content_types='text')
def position_message_hndlr(message):
    check_user(message)
    user = get_user(message)
    positions = ['ВРТ', 'ЗАЩ', 'ПЗЩ', 'НАП']
    position_input = str(message.text).strip().upper()
    if position_input in positions:
        user.position = message.text
        bot.reply_to(message, "Отправьте фото игрока:", reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_player_image)
    elif message.text == 'Вернуться на главное меню':
        startprocedure(message)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('ВРТ')
        item2=types.KeyboardButton('ЗАЩ')
        item3=types.KeyboardButton('ПЗЩ')
        item4=types.KeyboardButton('НАП')    
        item5=types.KeyboardButton('Вернуться на главное меню')  
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        bot.reply_to(message, "Выберите амплуа из предоставленного списка", reply_markup = markup)
        bot.register_next_step_handler(message, position_message_hndlr)

#Сохранение фото
@bot.message_handler(content_types=['photo'])
def handle_player_image(message):
    check_user(message)
    user = get_user(message)
    if user.fio is not None:
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = '/var/www/www-root/data/www/oplbot.ru/images/' + f"{user.fio.replace(' ', '_')}" + ".jpg" #Название фото
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            bot.reply_to(message, "Фото добавлено")
            
            #Записываем игрока в массив
            user.players.append(Player(user.z_type, user.fio, playerdate, user.position, src))
            
            # Добавляем кнопки
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton('Да')
            item2=types.KeyboardButton('Отправить заявку')
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Дозаявить/отзаявить еще одного игрока?", reply_markup=markup)
            bot.register_next_step_handler(message, handle_continue_yes_no)
        except Exception as err:
            print(f"Ошибка при загрузке файла: {err}")
            bot.reply_to(message, f"Ошибка при загрузке файла: {err}", reply_markup=types.ReplyKeyboardRemove())    
            bot.reply_to(message, "Отправьте фото игрока:", reply_markup = types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, handle_player_image)

#Продолжить - Да/Нет?
@bot.message_handler(content_types='text')
def handle_continue_yes_no(message):
    check_user(message)
    user = get_user(message)
    if(message.text == 'Да'):
        # Добавляем кнопки
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('Заявка')
        item2=types.KeyboardButton('Отзаявка')
        item3=types.KeyboardButton('Вернуться на главное меню (письмо отправится на состояние последнего добавленного игрока)')
        item4=types.KeyboardButton('Вернуться на главное меню (письмо не отправится)')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.reply_to(message, "Заявка/отзаявка:", reply_markup = markup)
        bot.register_next_step_handler(message, zayavka_message_handler)
    elif(message.text == 'Отправить заявку'):
        player_email = PlayerEmail(f"{user.league_name} {user.team_name}", user.senderinfo, user.players)
        player_email.sendEmail()
        bot.send_message(message.chat.id, "Письмо отправлено.", reply_markup=types.ReplyKeyboardRemove())
        startprocedure(message)


#####################################################################################   
#Шаблон для обычного письма (тело + вложения)
#####################################################################################     
   
#Обработка ввода тела письма 
@bot.message_handler(content_types='text')
def body_message_hndlr(message):
    check_user(message)
    user = get_user(message)
    user.body = message.text
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Да")
    item2=types.KeyboardButton("Нет")
    item3=types.KeyboardButton("Вернуться на главное меню (письмо не отправится)")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.reply_to(message, "Добавить вложение?", reply_markup=markup)    
    bot.register_next_step_handler(message, confirm_next_attach_hndlr)

#Обработка вопроса "Добавить еще вложения?"
@bot.message_handler(content_types='text')
def confirm_next_attach_hndlr(message):   
    check_user(message)
    user = get_user(message)
    if message.text == "Да":
        bot.reply_to(message, "Отправьте один файл", reply_markup=types.ReplyKeyboardRemove())    
        bot.register_next_step_handler(message, attachment_hndlr)
    elif message.text == "Нет":
        if user.is_anon:
            letter = RegularEmail(f"{user.vidobr}: Анонимно", user.body, user.attachments)
            letter.sendEmail()
        elif user.is_team:
            letter = RegularEmail(f"{user.vidobr}: {user.team_name}", f"{user.senderinfo}\n{user.body}", user.attachments)
            letter.sendEmail()
        else:
            letter = RegularEmail(f"{user.vidobr}", f"{user.senderinfo}\n{user.body}", user.attachments)
            letter.sendEmail()
        bot.reply_to(message, "Письмо отправлено.", reply_markup=types.ReplyKeyboardRemove())   
        startprocedure(message)
    elif message.text == "Вернуться на главное меню (письмо не отправится)":
        startprocedure(message)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Да")
        item2=types.KeyboardButton("Нет")
        markup.add(item1)
        markup.add(item2)
        bot.reply_to(message, "Выберите корректный вариант", reply_markup=markup)    
        bot.register_next_step_handler(message, confirm_next_attach_hndlr)

#Обработка фото
@bot.message_handler(content_types='photo')
def attachment_hndlr(message):
    check_user(message)
    user = get_user(message)
    try:
        if message.document is not None:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = '/var/www/www-root/data/www/oplbot.ru/docs/' + message.document.file_name #Название фото
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)  
            user.attachments.append(src)
        elif message.photo is not None:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = '/var/www/www-root/data/www/oplbot.ru/images/' + f"{datetime.now().strftime('%d%m%Y%H%M%S')}.jpg" #Название фото
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            user.attachments.append(src)
                
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Да")
        item2=types.KeyboardButton("Нет")
        item3=types.KeyboardButton("Вернуться на главное меню (письмо не отправится)")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)

        bot.reply_to(message, "Добавить еще вложение?", reply_markup=markup)    
        bot.register_next_step_handler(message, confirm_next_attach_hndlr)
    except Exception as err:
        print(f"Ошибка при загрузке файла: {err}")
        bot.reply_to(message, f"Ошибка при загрузке файла: {err}", reply_markup=types.ReplyKeyboardRemove())    
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Да")
        item2=types.KeyboardButton("Нет")
        item3=types.KeyboardButton("Вернуться на главное меню (письмо не отправится)")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.reply_to(message, "Добавить еще вложение?", reply_markup=markup)    
        bot.register_next_step_handler(message, confirm_next_attach_hndlr)
    

#####################################################################################   
#Если выбрана опция "Обращение/протест/апелляция" (от лица команды)
#####################################################################################   
#Обработка опции "Обращение/протест/апелляция"
@bot.message_handler(content_types='text')
def item2_message_hndlr(message): 
    check_user(message)
    user = get_user(message)
    if len(user.senderinfo)  < 1:
        user.senderinfo = message.text
    bot.reply_to(message, "Введите название команды:", reply_markup=types.ReplyKeyboardRemove())   
    bot.register_next_step_handler(message, team_message_hndlr) #Обработка ввода названия команды
    
#Обработка ввода названия команды
@bot.message_handler(content_types='text')
def team_message_hndlr(message):
    check_user(message)
    user = get_user(message)
    user.team_name = message.text
    user.is_team = True
    # Добавляем кнопки
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('Обращение')
    item2=types.KeyboardButton('Протест')
    item3=types.KeyboardButton('Апелляция')
    item4=types.KeyboardButton("Вернуться на главное меню")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    bot.reply_to(message, "Выберите вид обращения:", reply_markup=markup)    
    bot.register_next_step_handler(message, vidobr_message_hndlr) #Обработка вида обращения
    
#Обработка вида обращения
@bot.message_handler(content_types='text')
def vidobr_message_hndlr(message):
    check_user(message)
    user = get_user(message)
    user.vidobr = ""
    if message.text == 'Обращение':
        bot.reply_to(message, "Введите текстовое содержание обращения:", reply_markup = types.ReplyKeyboardRemove())
        user.vidobr = 'Обращение'
        bot.register_next_step_handler(message, body_message_hndlr) #Обработка ввода тела письма 
    elif message.text == 'Протест':
        bot.reply_to(message, "Введите текстовое содержание протеста:", reply_markup = types.ReplyKeyboardRemove()) 
        user.vidobr = 'Протест'
        bot.register_next_step_handler(message, body_message_hndlr) #Обработка ввода тела письма 
    elif message.text == 'Апелляция':
        bot.reply_to(message, "Введите текстовое содержание апелляции:", reply_markup = types.ReplyKeyboardRemove())
        user.vidobr = 'Апелляция'
        bot.register_next_step_handler(message, body_message_hndlr) #Обработка ввода тела письма 
    elif message.text == 'Вернуться на главное меню':
        startprocedure(message)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('Обращение')
        item2=types.KeyboardButton('Протест')
        item3=types.KeyboardButton('Апелляция')
        item4=types.KeyboardButton("Вернуться на главное меню")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.reply_to(message, "Выберите вид обращения из представленных:", reply_markup=markup)    
        bot.register_next_step_handler(message, vidobr_message_hndlr) #Обработка вида обращения

    

#####################################################################################   
#Если выбрана опция "Задать вопрос"
#####################################################################################       
@bot.message_handler(content_types='text')
def item3_message_hndlr(message): 
    check_user(message)
    user = get_user(message)
    user.vidobr = "Вопрос"
    if len(user.senderinfo)  < 1:
        user.senderinfo = message.text
    bot.reply_to(message, "Введите содержимое письма:", reply_markup = types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, body_message_hndlr)

#####################################################################################   
#Если выбрана опция "Предложить идею/жалоба" (анонимно)
#####################################################################################   
@bot.message_handler(content_types='text')
def item4_message_hndlr(message): 
    check_user(message)
    user = get_user(message)
    if "@" not in message.text:
        user.is_anon = True
    user.senderinfo = message.text
    # Добавляем кнопки
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('Идея')
    item2=types.KeyboardButton('Жалоба')
    item3=types.KeyboardButton('Вернуться на главное меню')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.reply_to(message, "Выберите вид обращения:", reply_markup=markup)    
    bot.register_next_step_handler(message, idzhal_message_nhdlr)
    
@bot.message_handler(content_types='text')
def idzhal_message_nhdlr(message):
    check_user(message)
    user = get_user(message)
    if message.text == 'Идея':
        user.vidobr = "Идея"
        bot.reply_to(message, "Введите содержание обращения:", reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, body_message_hndlr)
    elif message.text == 'Жалоба':
        user.vidobr = "Жалоба"
        bot.reply_to(message, "Введите содержание обращения:", reply_markup = types.ReplyKeyboardRemove())  
        bot.register_next_step_handler(message, body_message_hndlr)
    elif message.text == 'Вернуться на главное меню':
        startprocedure(message)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('Идея')
        item2=types.KeyboardButton('Жалоба')
        markup.add(item1)
        markup.add(item2)
        bot.reply_to(message, "Выберите вид обращения из представленных:", reply_markup=markup)    
        bot.register_next_step_handler(message, idzhal_message_nhdlr)

#####################################################################################   
#Если выбрана опция "Таблицы/календари/статистика/составы"
#####################################################################################   
#Ссылки

@bot.message_handler(content_types='text')
def item5_message_hndlr(message): 
    # Добавляем кнопки
    markup = types.InlineKeyboardMarkup()
    btn_bmfl= types.InlineKeyboardButton(text='БМФЛЛ', url='https://bmfl.ru/bmfll/')
    btn_zhmfl= types.InlineKeyboardButton(text='ЖМФЛЛ', url='https://bmfl.ru/jmfll/')
    btn_mflnr= types.InlineKeyboardButton(text='МФЛЛНР', url='https://bmfl.ru/ногинский-р-н/')
    btn_emfl= types.InlineKeyboardButton(text='МЛФЛ', url='https://bmfl.ru/мытищи-турниры/')
    btn_mlfl= types.InlineKeyboardButton(text='ЭМФЛЛ', url='https://bmfl.ru/emfll/')
    
    
    markup.add(btn_bmfl)
    markup.add(btn_zhmfl)
    markup.add(btn_mflnr)
    markup.add(btn_emfl)
    markup.add(btn_mlfl)
    bot.reply_to(message, "Ссылки на сайт:", reply_markup = markup)  
    

#####################################################################################   
#Если выбрана опция "Документы"
#####################################################################################   

def item6_message_hndlr(message): 
    # Добавляем кнопки
    markup = types.InlineKeyboardMarkup()
    btn_regl= types.InlineKeyboardButton(text='Регламент ОПЛ', url='https://bmfl.ru/wp-content/uploads/2022/05/Reglament_OPL.pdf')
    btn_ust= types.InlineKeyboardButton(text='Устав КДК', url='https://bmfl.ru/wp-content/uploads/2021/06/%D0%A3%D0%A1%D0%A2%D0%90%D0%92-%D0%9A%D0%94%D0%9A.pdf')
    

    markup.add(btn_regl)
    markup.add(btn_ust)
    bot.reply_to(message, "Ссылки на документы:", reply_markup = markup)  
    


#####################################################################################   
#Если выбрана опция "Заполнить протокол"
#####################################################################################   
####
#На будущее
####

def item7_message_hndlr(message): 
    markup = types.InlineKeyboardMarkup()
    btn_tables= types.InlineKeyboardButton(text='Таблицы', url='https://bmfl.ru')
    markup.add(btn_tables)

#####################################################################################   
#Если выбрана опция "Контакты"
#####################################################################################   


def item8_message_hndlr(message): 
    # Добавляем кнопки
    markup = types.InlineKeyboardMarkup()

    bot.reply_to(message, """
Руководитель Объединенной Подмосквной Лиги
Артемьев Артем Сергеевич
Тел: +7(964)642-68-05

Заместитель руководителя ОПЛ
Лапчик Станислав Дмитриевич
Тел: +7(919)996-44-45 

Руководитель БМФЛЛ (Балашиха)
Попов Василий Петрович
Тел.: +7(926)589-54-00 

Руководитель ЖМФЛЛ (Железнодорожный)
Захаров Кирилл Валерьевич
Тел.: +7(926)725-20-88 

Руководитель МФЛЛНР и ЭМФЛЛ (Ногинск и Электросталь)
Дружинин Станислав Владимирович
Тел.: +7(925)152-40-77""")  
    startprocedure(message)


#####################################################################################   
#Если выбрана опция "Подписаться на рассылку"
#####################################################################################   
####
#На будущее
####

def item9_message_hndlr(message): 
    markup = types.InlineKeyboardMarkup()
    btn_tables= types.InlineKeyboardButton(text='Телеграмм ОПЛ', url='https://bmfl.ru')
    markup.add(btn_tables)
    

#####################################################################################   
#Если выбрана опция "Поменять контактные данные"
#####################################################################################   
@bot.message_handler(content_types='text')
def item10_message_hndlr(message): 
    check_user(message)
    user = get_user(message)
    user.senderinfo = message.text
    bot.reply_to(message, "Данные изменены.")
    startprocedure(message)

# Запускаем бота
while(True):
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as err:
        print(f"Ошибка, таймаут: {err}")
