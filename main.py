

from DbModels import *
import telebot
import time
from telebot import types
import random

from crypto_pay_api_sdk import cryptopay

bot = telebot.TeleBot('6748210987:AAH29ZaAO_52Ka_VXb6p8c7uktnpV6P5SBQ')
Crypto = cryptopay.Crypto("68470:AAxinOmVNHgCdl5UvO0yLKJe7UYZUtgoZUf", testnet = False)


@bot.message_handler(commands=['admin_balance_08_09_04_01'])
def change(msg):
    m = bot.send_message(msg.chat.id, 'Кому (id) [space] какой (amount)')
    bot.register_next_step_handler(m, apply_balance)

def apply_balance(msg):
    user_id = msg.text.split(' ')[0]
    amount = msg.text.split(' ')[1]

    Users.change_balance(user_id, amount)

    bot.send_message(msg.chat.id, 'Done')

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.chat.id
    if not Users.user_exists(user_id):
        Users.create_user(user_id)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('ССЫЛКА НА ЧАТ', url='https://t.me/+vVwS0zi--R9jMDli'))

    menu=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Пополнение баланса 🎮")
    item2=types.KeyboardButton("Профиль 👤")
    item3=types.KeyboardButton("Игры 🎰")
    item4=types.KeyboardButton("ЧАТ")

    menu.add(item1, item2, item3, item4)

    m = bot.send_message(msg.chat.id, '🎲 Добро пожаловать в KingPlay Ca$1n0! 🎰', reply_markup=menu)
    bot.send_message(msg.chat.id, '''
<b>✨ Присоединяйтесь в наш ЧАТ ✨</b>
                                 
💎 Наш Функционал:
• 🎮 Уникальные Игры:
    • Dice, Дартс, Боулинг, Футбол, Баскет Обычный 🎲
    • Jackpot ☄️
    • CoinFlip
    • Слоты 🎰
• 🧪 Команды:
    • Профиль 👤
    • Перевод Денег Другим Пользователям 💸
    • Пополнение баланса 🎮
    • Вывод 💈
    • Удалить аккаунт 🚫
                                 
💬 В нашем чате ламповая атмосфера и общение на разные темы!
                                 
<b><i>👨‍💻 Чат модерируется и никто не останется безнаказанно!</i></b>''', parse_mode="html", reply_markup=markup)
    bot.register_next_step_handler(m, msg_processing)

@bot.message_handler(content_types=['text'])
def msg_processing(msg):
    if msg.text == "Профиль 👤":

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✨ Пополнить баланс', callback_data='deposit'), types.InlineKeyboardButton('💈 Заказать выплату', callback_data='withdraw'))
        obj_list = Users.get_about(msg.chat.id)
        bot.send_message(msg.chat.id, f'''
👤 Профиль
➖➖➖➖➖➖➖➖➖➖➖➖
🔢 ID: {msg.chat.id}
💰 Баланс: {obj_list[1]} руб.

🕹 Никнейм: @{msg.from_user.username}
🎮 Юзернейм: @{msg.from_user.username}

📊 Статистика:
➖➖➖➖➖➖➖➖➖➖➖➖
⌛️ Всего депозитов: {obj_list[2]} руб.
''', reply_markup=markup)


    if msg.text == 'Пополнение баланса 🎮':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('CryptoBot', callback_data=f'deposit-crypto'), types.InlineKeyboardButton('СБП через поддержку', url=f'https://t.me/kingplay_admin'))
        m = bot.send_message(msg.chat.id, text=f'''
<b>Выберите способ пополнения: </b>

''', parse_mode="html", reply_markup=markup)
        '''bot.edit_message_reply_markup(
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        reply_markup=markup
    )'''

    if msg.text == "Игры 🎰":

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('🔴⚫ Рулетка', callback_data='double'), 
            types.InlineKeyboardButton('🃏 BlackJack', callback_data='blackjack'), 
            types.InlineKeyboardButton('🎲 Dice', callback_data='dice'), 
            types.InlineKeyboardButton('🏀 Basket', callback_data='basket'), 
            #types.InlineKeyboardButton('🎯 Darts', callback_data='darts'),
            types.InlineKeyboardButton('🦅🟡 CoinFlip', callback_data='coinflip')
            )
        #obj_list = Users.get_about(msg.chat.id)
        bot.send_message(msg.chat.id, f'''
<b>Выберите игру!</b>''',parse_mode='html' ,reply_markup=markup)


    if msg.text == "ЧАТ":

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('ССЫЛКА НА ЧАТ', url='https://t.me/+vVwS0zi--R9jMDli'))
        #obj_list = Users.get_about(msg.chat.id)
        bot.send_message(msg.chat.id, f'''
💬 В нашем чате ламповая атмосфера и общение на разные темы!
                                 
<b><i>👨‍💻 Чат модерируется и никто не останется безнаказанно!</i></b>''',parse_mode='html' ,reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'double':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('🔴', callback_data=f'{call.data}game-red'), types.InlineKeyboardButton('⚫', callback_data=f'{call.data}game-black'))
        m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите цвет (МИН. 10 РУБ)</b>

<i>ПОТЕНЦИАЛЬНЫЙ ВЫИГРЫШ X2 ОТ СТАВКИ</i>
''', parse_mode="html")
        bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

    if call.data == 'blackjack':
       # markup = types.InlineKeyboardMarkup()
       # markup.add(types.InlineKeyboardButton('🔴', callback_data=f'{call.data}game-red'), types.InlineKeyboardButton('⚫', callback_data=f'{call.data}game-black'))
        m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
В ИГРЕ ИСЧЕРПАН ЛИМИТ ВЫИГРЫШЕЙ 
''', parse_mode="html")

    if call.data == 'dice':
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('1', callback_data=f'{call.data}game-1'),
            types.InlineKeyboardButton('2', callback_data=f'{call.data}game-2'),
            types.InlineKeyboardButton('3', callback_data=f'{call.data}game-3'),
            types.InlineKeyboardButton('4', callback_data=f'{call.data}game-4'),
            types.InlineKeyboardButton('5', callback_data=f'{call.data}game-5'),
            types.InlineKeyboardButton('6', callback_data=f'{call.data}game-6'),

        )
        m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите грань (МИН. 10 РУБ)</b>

<i>ПОТЕНЦИАЛЬНЫЙ ВЫИГРЫШ X2.5 ОТ СТАВКИ</i>
''', parse_mode="html")
        bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )
    if call.data == 'basket':

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('Попадет в кольцо', callback_data=f'{call.data}game-1'),
            types.InlineKeyboardButton('Не попадет в кольцо', callback_data=f'{call.data}game-2')

        )
        m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите событие (МИН. 10 РУБ)</b>

<i>ПОТЕНЦИАЛЬНЫЙ ВЫИГРЫШ X2 ОТ СТАВКИ</i>
''', parse_mode="html")
        bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

    if call.data == 'coinflip':
       markup = types.InlineKeyboardMarkup()
       markup.add(
            types.InlineKeyboardButton('🟡 - Решка', callback_data=f'{call.data}game-1'),
            types.InlineKeyboardButton('🦅 - Орёл', callback_data=f'{call.data}game-2')

        )
       m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите событие (МИН. 10 РУБ)</b>

<i>ПОТЕНЦИАЛЬНЫЙ ВЫИГРЫШ X2 ОТ СТАВКИ</i>
''', parse_mode="html")
       bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

# coinflip game ----------------------------------
    if 'coinflipgame' in call.data:
        info = Users.get_all_stats(call.message.chat.id)

        if info[1] < 10:
            bot.answer_callback_query(call.id, f"‼️ ПОПОЛНИТЕ БАЛАНС, ЧТОБЫ ИГРАТЬ. ВАШ БАЛАНС: {info[1]} РУБ.", show_alert=True)

        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(
            types.InlineKeyboardButton('10 ₽', callback_data=f'10_{call.data}'),
            types.InlineKeyboardButton('25 ₽', callback_data=f'25_{call.data}'),
            types.InlineKeyboardButton('100 ₽', callback_data=f'100_{call.data}'),
            types.InlineKeyboardButton('200 ₽', callback_data=f'250_{call.data}'),
            types.InlineKeyboardButton('300 ₽', callback_data=f'300_{call.data}'),
            types.InlineKeyboardButton('500 ₽', callback_data=f'500_{call.data}'),
            types.InlineKeyboardButton('ВА-БАНК!', callback_data=f'allin_{call.data}')
        )
            m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите размер ставки (МИН. 10 РУБ)</b>

<i>ПОТЕНЦИАЛЬНЫЙ ВЫИГРЫШ X2 ОТ СТАВКИ</i>
''', parse_mode="html")
        bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
        )

    
    if '_coinflipgame' in call.data:

        all_stats = Users.get_all_stats(call.message.chat.id)
        if call.data.split("-")[1] == '1':
            flag = '🟡 - Решка'
        else:
            flag = '🦅 - Орёл'

        rubs = call.data.split('_')[0]
        if rubs == 'allin':
            rubs = all_stats[1]
            
        if int(rubs) <= int(all_stats[1]):

            bot.send_message(call.message.chat.id, f'вы поставили на {flag}\n<b>Бросаем монетку!</b>', parse_mode="html")
            for x in range(1, 5):
                m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    <b>Бросаем монетку!</b>
    <i>{5-x}...</i>
    ''', parse_mode="html")
                time.sleep(1)

            time.sleep(2)

            rubs = call.data.split('_')[0]
            if rubs == 'allin':
                rubs = all_stats[1]

            if random.random() < float(all_stats[4]):
                if '-1' in call.data:
                    m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    🟡
    ''', parse_mode="html")
                else:
                    m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    🦅
    ''', parse_mode="html")


                Users.add_balance(call.message.chat.id, rubs)
                bot.send_message(call.message.chat.id, f'🎉💖 Поздравляем вы выиграли! <b>Ваши {rubs} превратились в {int(rubs)*2} ₽</b>', parse_mode="html")
            

            else:
                if '-1' in call.data:
                    m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    🦅
    ''', parse_mode="html")
                else:
                    m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    🟡
    ''', parse_mode="html")

                Users.lose_balance(call.message.chat.id, rubs)
                bot.send_message(call.message.chat.id, f'⚠️ К сожалению, вы проиграли <b>Попробуете еще?</b>', parse_mode="html")
        else:
            bot.answer_callback_query(call.id, f"‼️ ПОПОЛНИТЕ БАЛАНС, ЧТОБЫ ИГРАТЬ. ВАШ БАЛАНС: {all_stats[1]} РУБ.", show_alert=True)
  

# DOUBLE GAME ---------------------------------------------------------
    if 'doublegame' in call.data:
        info = Users.get_all_stats(call.message.chat.id)

        if info[1] < 10:
            bot.answer_callback_query(call.id, f"‼️ ПОПОЛНИТЕ БАЛАНС, ЧТОБЫ ИГРАТЬ. ВАШ БАЛАНС: {info[1]} РУБ.", show_alert=True)

        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(
            types.InlineKeyboardButton('10 ₽', callback_data=f'10_{call.data}'),
            types.InlineKeyboardButton('25 ₽', callback_data=f'25_{call.data}'),
            types.InlineKeyboardButton('100 ₽', callback_data=f'100_{call.data}'),
            types.InlineKeyboardButton('200 ₽', callback_data=f'250_{call.data}'),
            types.InlineKeyboardButton('300 ₽', callback_data=f'300_{call.data}'),
            types.InlineKeyboardButton('500 ₽', callback_data=f'500_{call.data}'),
            types.InlineKeyboardButton('ВА-БАНК!', callback_data=f'allin_{call.data}')
        )
            m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите размер ставки (МИН. 10 РУБ)</b>

<i>ПОТЕНЦИАЛЬНЫЙ ВЫИГРЫШ X2 ОТ СТАВКИ</i>
''', parse_mode="html")
        bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
        )

    
    if '_doublegame' in call.data:
        all_stats = Users.get_all_stats(call.message.chat.id)
        rubs = call.data.split('_')[0]
        if rubs == 'allin':
            rubs = all_stats[1]
            
        if int(rubs) <= int(all_stats[1]):

            bot.send_message(call.message.chat.id, f'вы поставиили на {call.data.split("-")[1]}\n<b>Крутим рулетку!</b>', parse_mode="html")
            for x in range(1, 5):
                m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    <b>Крутим рулетку!</b>
    <i>{5-x}...</i>
    ''', parse_mode="html")
                time.sleep(1)

            time.sleep(2)
            all_stats = Users.get_all_stats(call.message.chat.id)

            rubs = call.data.split('_')[0]
            if rubs == 'allin':
                rubs = all_stats[1]

            if random.random() < float(all_stats[4]):
                if 'red' in call.data:
                    m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    🔴
    ''', parse_mode="html")
                else:
                    m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    ⚫
    ''', parse_mode="html")


                Users.add_balance(call.message.chat.id, rubs)
                bot.send_message(call.message.chat.id, f'🎉💖 Поздравляем вы выиграли! <b>Ваши {rubs} превратились в {int(rubs)*2} ₽</b>', parse_mode="html")
            

            else:
                if 'red' in call.data:
                    m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    ⚫
    ''', parse_mode="html")
                else:
                    m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    🔴
    ''', parse_mode="html")

                Users.lose_balance(call.message.chat.id, rubs)
                bot.send_message(call.message.chat.id, f'⚠️ К сожалению, вы проиграли <b>Попробуете еще?</b>', parse_mode="html")
        else:
            bot.answer_callback_query(call.id, f"‼️ ПОПОЛНИТЕ БАЛАНС, ЧТОБЫ ИГРАТЬ. ВАШ БАЛАНС: {all_stats[1]} РУБ.", show_alert=True)

    if 'dicegame' in call.data:
        info = Users.get_all_stats(call.message.chat.id)

        if info[1] < 10:
            bot.answer_callback_query(call.id, f"‼️ ПОПОЛНИТЕ БАЛАНС, ЧТОБЫ ИГРАТЬ. ВАШ БАЛАНС: {info[1]} РУБ.", show_alert=True)

        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(
            types.InlineKeyboardButton('10 ₽', callback_data=f'10_{call.data}'),
            types.InlineKeyboardButton('25 ₽', callback_data=f'25_{call.data}'),
            types.InlineKeyboardButton('100 ₽', callback_data=f'100_{call.data}'),
            types.InlineKeyboardButton('200 ₽', callback_data=f'250_{call.data}'),
            types.InlineKeyboardButton('300 ₽', callback_data=f'300_{call.data}'),
            types.InlineKeyboardButton('500 ₽', callback_data=f'500_{call.data}'),
            types.InlineKeyboardButton('ВА-БАНК!', callback_data=f'allin_{call.data}')
        )
            m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите размер ставки (МИН. 10 РУБ)</b>

<i>ПОТЕНЦИАЛЬНЫЙ ВЫИГРЫШ X2.5 ОТ СТАВКИ</i>
''', parse_mode="html")
        bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
        )

    if '_dicegame' in call.data:
        all_stats = Users.get_all_stats(call.message.chat.id)
        rubs = call.data.split('_')[0]
        if rubs == 'allin':
            rubs = all_stats[1]

        if int(rubs) <= int(all_stats[1]):
            bot.send_message(call.message.chat.id, f'вы поставиили на грань: {call.data.split("-")[1]}\n<b>Бросаем кубик!</b>', parse_mode="html")
            for x in range(1, 5):
                m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    <b>Бросаем кубик!</b>
    <i>{5-x}...</i>
    ''', parse_mode="html")
                time.sleep(1)

            time.sleep(5)
            all_stats = Users.get_all_stats(call.message.chat.id)

            rubs = call.data.split('_')[0]
            if rubs == 'allin':
                rubs = all_stats[1]


            msg = bot.send_dice(call.message.chat.id)
            print(msg)
            if int(msg.dice.value) == int(call.data.split("-")[1]):

                Users.add_balance(call.message.chat.id, rubs)
                bot.send_message(call.message.chat.id, f'🎉💖 Поздравляем вы выиграли! <b>Ваши {rubs} превратились в {int(rubs)*2.5} ₽</b>', parse_mode="html")
            

            else:

                Users.lose_balance(call.message.chat.id, rubs)
                bot.send_message(call.message.chat.id, f'⚠️ К сожалению, вы проиграли <b>Попробуете еще?</b>', parse_mode="html")
        else:
            bot.answer_callback_query(call.id, f"‼️ ПОПОЛНИТЕ БАЛАНС, ЧТОБЫ ИГРАТЬ. ВАШ БАЛАНС: {all_stats[1]} РУБ.", show_alert=True)

# BASKETBALL PLAY

    if 'basketgame' in call.data:
        info = Users.get_all_stats(call.message.chat.id)

        if info[1] < 10:
            bot.answer_callback_query(call.id, f"‼️ ПОПОЛНИТЕ БАЛАНС, ЧТОБЫ ИГРАТЬ. ВАШ БАЛАНС: {info[1]} РУБ.", show_alert=True)

        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(
            types.InlineKeyboardButton('10 ₽', callback_data=f'10_{call.data}'),
            types.InlineKeyboardButton('25 ₽', callback_data=f'25_{call.data}'),
            types.InlineKeyboardButton('100 ₽', callback_data=f'100_{call.data}'),
            types.InlineKeyboardButton('200 ₽', callback_data=f'250_{call.data}'),
            types.InlineKeyboardButton('300 ₽', callback_data=f'300_{call.data}'),
            types.InlineKeyboardButton('500 ₽', callback_data=f'500_{call.data}'),
            types.InlineKeyboardButton('ВА-БАНК!', callback_data=f'allin_{call.data}')
        )
            m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите размер ставки (МИН. 10 РУБ)</b>

<i>ПОТЕНЦИАЛЬНЫЙ ВЫИГРЫШ X2 ОТ СТАВКИ</i>
''', parse_mode="html")
        bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
        )

    if '_basketgame' in call.data:
        all_stats = Users.get_all_stats(call.message.chat.id)
        rubs = call.data.split('_')[0]
        if rubs == 'allin':
            rubs = all_stats[1]

        if int(rubs) <= int(all_stats[1]):

            if call.data.split("-")[1] == '1':
                flag = 'Попадет'
                win = 4
            else:
                flag = 'Не попадет'
            bot.send_message(call.message.chat.id, f'вы поставили на событие: {flag}\n<b>Бросаем в кольцо!</b>', parse_mode="html")
            for x in range(1, 5):
                m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
    <b>Бросаем в кольцо!</b>
    <i>{5-x}...</i>
    ''', parse_mode="html")
                time.sleep(1)

            time.sleep(5)
            all_stats = Users.get_all_stats(call.message.chat.id)

            #rubs = call.data.split('_')[0]


            msg = bot.send_dice(call.message.chat.id, '🏀')
            print(msg)
            if call.data.split("-")[1] == '1':
                if msg.dice.value == 4 or msg.dice.value == 5:
                    time.sleep(3)
                    Users.add_balance(call.message.chat.id, rubs)
                    bot.send_message(call.message.chat.id, f'🎉💖 Поздравляем вы выиграли! <b>Ваши {rubs} превратились в {int(rubs)*2} ₽</b>', parse_mode="html")
            

                else:
                    time.sleep(3)
                    Users.lose_balance(call.message.chat.id, rubs)
                    bot.send_message(call.message.chat.id, f'⚠️ К сожалению, вы проиграли <b>Попробуете еще?</b>', parse_mode="html")
            
            elif call.data.split("-")[1] == '2':
                if msg.dice.value != 4 or msg.dice.value != 5:
                    time.sleep(3)
                    Users.add_balance(call.message.chat.id, rubs)
                    bot.send_message(call.message.chat.id, f'🎉💖 Поздравляем вы выиграли! <b>Ваши {rubs} превратились в {int(rubs)*2} ₽</b>', parse_mode="html")
        else:
            bot.answer_callback_query(call.id, f"‼️ ПОПОЛНИТЕ БАЛАНС, ЧТОБЫ ИГРАТЬ. ВАШ БАЛАНС: {all_stats[1]} РУБ.", show_alert=True)

    if call.data == 'deposit':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('CryptoBot', callback_data=f'{call.data}-crypto'), types.InlineKeyboardButton('СБП через поддержку', url=f'https://t.me/kingplay_admin'))
        m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Выберите способ пополнения: </b>

''', parse_mode="html")
        bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

    if call.data == 'deposit-crypto':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('CryptoBot', callback_data=f'{call.data}-crypto'), types.InlineKeyboardButton('СБП через поддержку', url=f'https://t.me/kingplay_admin'))
        m = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
<b>Напишите сумму пополнения ЦИФРАМИ:</b>
например: 850

‼️ Минимальная сумма пополнения 400 руб.
''', parse_mode="html")
        bot.register_next_step_handler(m, deposit_sum)
        '''print(Crypto.createInvoice("USDT", "0.4", params={"description": "Test Invoice",
                                                                         "expires_in": 300
                                                                         }))'''

    if 'check-' in call.data:
        invoice_id = call.data.split('-')[1]
        rubs = call.data.split('_')[0]

        invoice = Crypto.getInvoices(params = {"invoice_ids": invoice_id})

        if invoice['result']['items'][0]['status'] == 'paid':
            rates = Crypto.getExchangeRates()
            
            Users.add_balance(call.message.chat.id, rubs)
            Users.add_deposit(call.message.chat.id, rubs)
            CasinoBalance.add_balance(rubs)

            bot.send_message(call.message.chat.id, '✅ Ваш баланс успешно пополнен, удачи!')
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('✨ Пополнить баланс', callback_data='deposit'), types.InlineKeyboardButton('💈 Заказать выплату', callback_data='withdraw'))
            obj_list = Users.get_about(call.message.chat.id)
            bot.send_message(call.message.chat.id, f'''
👤 Профиль
➖➖➖➖➖➖➖➖➖➖➖➖
🔢 ID: {call.message.chat.id}
💰 Баланс: {obj_list[1]} руб.

🕹 Никнейм: @{call.message.from_user.username}
🎮 Юзернейм: @{call.message.from_user.username}

📊 Статистика:
➖➖➖➖➖➖➖➖➖➖➖➖
⌛️ Всего депозитов: {obj_list[2]} руб.
''', reply_markup=markup)


    if call.data == 'withdraw':
        all_stats = Users.get_all_stats(call.message.chat.id)
        if int(all_stats[1]) > 999:
            bot.send_message(call.message.chat.id, '<i>Комиссия при выводе 5% + 20rub. </i>', parse_mode='html')
            m = bot.send_message(call.message.chat.id, 'Пришлите реквизиты для вывода ПО ШАБЛОНУ!\n\nНОМЕР: <b>СБП (номер телефона и наименование банка)</b> (Либо адрес крипто-кошелька)\nСУММА ВЫВОДА: (просто число)', parse_mode='html')
            bot.register_next_step_handler(m, confirm)
            #bot.register_next_step_handler(m, send_money)
        else:
            bot.answer_callback_query(call.id, f"‼️ Минимальная сумма вывода 1000 rub. ВАШ БАЛАНС: {all_stats[1]} rub.", show_alert=True)

    if 'confirm' in call.data:
        summ = call.data.split('-')[1]
        summ = int(summ) - int(summ) * 0.05 - 20
        CasinoBalance.lose_balance(summ)
        Users.lose_balance(call.message.chat.id, float(call.data.split('-')[1]))
        bot.send_message(6053136867, call.message.text)
        bot.send_message(call.message.chat.id, '🕓 Спасибо за заявку! Время вывода составит от 5 мин до 2х суток')




def send_money(msg):
    if int(msg.text)  > 1000:
        bot.send_message(msg.chat.id, 'Пришлите реквизиты для вывода ПО ШАБЛОНУ!\n\nНОМЕР: <b>СБП (номер телефона и наименование банка)</b> (Либо адрес крипто-кошелька)\nСУММА ВЫВОДА: (просто число)', parse_mode='html')
        bot.register_next_step_handler(m, confirm)

    else:
        bot.send_message(msg.chat.id, 'Сумма вывода не может быть меньше 1000 rub')

def confirm(msg):
    summ = msg.text.split("\n")[1]
    if int(summ) >= 1000:
        markup = types.InlineKeyboardMarkup()
        summ = int(msg.text.split("\n")[1]) - int(msg.text.split("\n")[1]) * 0.05 - 20

        amount = int(msg.text.split("\n")[1])
        markup.add(types.InlineKeyboardButton('✅ ПОДТВЕРЖДАЮ ВЫВОД', callback_data=f'confirm-{amount}'))

        info = msg.text.split("\n")[0]
        bot.send_message(msg.chat.id, f'<b> ПОДТВЕРДИТЕ ВЫВОД НАЖАВ КНОПКУ: <u>ПОДТВЕРЖДАЮ ВЫВОД</u> </b>\nРеквизиты вывода: {info}\nСумма с учетом комиссии: {summ}', parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(msg.chat.id, 'Сумма вывода не может быть меньше 1000 rub')


def deposit_sum(msg):
    if int(msg.text)  > 399:
        rates = Crypto.getExchangeRates()
        usdt_rub = rates['result'][0]['rate']
        usdt = round(int(msg.text) / int(float(usdt_rub)), 2)
        #Deposits.create_order(msg.chat.id, int(msg.text))

        invoice = Crypto.createInvoice("USDT", f"{usdt}", params={"description": f"Пополнение баланса пользователя: {msg.chat.id}",
                                                                             "expires_in": 900
                                                                             })

        markup = types.InlineKeyboardMarkup()
        i_id = invoice['result']['invoice_id']
        p_url = invoice['result']['pay_url']
        markup.add(types.InlineKeyboardButton('✅ ПРОВЕРИТЬ ✅', callback_data=f'{msg.text}_check-{i_id}'))
        m = bot.send_message(msg.chat.id, text=f'''
<b>ССЫЛКА ДЛЯ ОПЛАТЫ</b>
{p_url}

‼️ ОПЛАТА ЧЕРЕЗ USDT КОТОРЫЙ МОЖНО КУПИТЬ В БОТЕ
СУММА В USDT {usdt} = {msg.text} РУБ

<b>ССЫЛКА АКТИВНА 15 МИНУТ</b>
    ''', parse_mode="html", reply_markup=markup)
    else:
        bot.send_message(msg.chat.id, 'Произошла ошибка. МИНИМАЛЬНАЯ сумма пополнения ОТ 400 РУБЛЕЙ')



bot.infinity_polling(none_stop=True)