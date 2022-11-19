import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logic
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


def mode_selector():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Single player", callback_data="mode-SP"),
               InlineKeyboardButton("Multiplayer", callback_data="mode-MP"))
    return markup


def move_selector():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("1", callback_data='move 1'),
               InlineKeyboardButton("2", callback_data='move 2'),
               InlineKeyboardButton("3", callback_data='move 3'),
               InlineKeyboardButton("4", callback_data='move 4'),
               InlineKeyboardButton("5", callback_data='move 5'),
               InlineKeyboardButton("6", callback_data='move 6'),
               InlineKeyboardButton("7", callback_data='move 7'),
               InlineKeyboardButton("8", callback_data='move 8'),
               InlineKeyboardButton("9", callback_data='move 9'))
    return markup


@bot.message_handler(commands=['start'])
def begin(message):
    bot.send_message(message.chat.id, "Select game mode", reply_markup=mode_selector())


def make_move(message):
    move = message.text  # TODO check input
    gm.move(int(move))
    win_check(message)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith('mode'))
def callback_query(call):
    gm.reset()
    if call.data == "mode-SP":
        gm.mode = 1
        gm.playerO.name = "AI"
        gm.playerX.name = call.message.chat.first_name
    elif call.data == "mode-MP":
        gm.mode = 2
    start(call.message)


def start(message):
    gm.player = next(gm.cycler)

    if gm.player == gm.playerO and gm.mode == 1:
        gm.move(gm.ai_move())
        win_check(message)
    elif gm.player.name == 'Draw':
        win_check(message)
    else:
        bot.send_message(message.chat.id, gm.board())
        bot.send_message(message.chat.id, f"Player: {gm.player.name} ( {gm.player.sym} )\nEnter [1-9] to play")
        bot.register_next_step_handler(message, make_move)


def win_check(message):
    winner = gm.win_check()
    if winner:
        bot.send_message(message.chat.id, gm.board())
        text = f"Winner: {winner.name}\n\n"
        for i in logic.Players.player_list:
            text += f"{i.name}: {i.total_score}\n"
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Play again?", reply_markup=mode_selector())
    else:
        start(message)


if __name__ == '__main__':
    gm = logic.Game()
    bot.infinity_polling()
