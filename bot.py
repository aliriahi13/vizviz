from telebot import TeleBot
from telebot.types import (Message, InlineKeyboardMarkup,
                           InlineKeyboardButton,WebAppData,WebAppInfo, CallbackQuery)
from telebot.util import update_types
from config import *

token: str = Token

bot = TeleBot(token=token, parse_mode="HTML")

def check_join(user, channels):

    for i in channels:
        is_member = bot.get_chat_member(chat_id=i, user_id=user)

        if is_member.status in ["kicked", "left"]:
            return False
        
    return True

@bot.message_handler(commands=["start"])
def start(message: Message):
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("vizviz_wolv",url="https://t.me/vizviz_wolv")
    button2 = InlineKeyboardButton("channel_jadid_wolv",url="https://t.me/channel_jadid_wolv")
    button3 = InlineKeyboardButton("mostwanted_wolv",url="https://t.me/mostwanted_wolv")
    button4 = InlineKeyboardButton("عضو شدم",callback_data="confrim")
    markup.add(button1,button2,button3,button4)
    bot.send_message(chat_id=message.chat.id,
                     text="برای استفاده از ربات باید در کانال های زیر عضو بشید",
                     reply_markup=markup)

                    
@bot.callback_query_handler(func= lambda call: call.data == "confrim")
def proceed(call: CallbackQuery):

    is_member = check_join(user=call.from_user.id, channels=channels)

    if is_member is False:
        bot.send_message(chat_id=call.message.chat.id,text="عضویت شما تایید نشد,دوباره امتحان کنید") 
    else:
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton(
            text="استفاده از ربات",
            web_app=WebAppInfo(""))
        markup.add(button)
        bot.send_message(chat_id=call.message.chat.id,text="عضویت شما تایید شد", reply_markup=markup)


if __name__ == "__main__":
    bot.polling(allowed_updates=update_types)
    
