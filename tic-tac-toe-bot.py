import telebot
from telebot.types import InlineKeyboardButton
import logic
import os
from dotenv import load_dotenv, find_dotenv
from keyboa import Keyboa
from textwrap import dedent

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('6226805699:AAE1T96RKSjs06kNID7VW9xVsYaSOFDI92o'))


class States:
    def __init__(self):
        self.instance = {}
        self.message_ids = {}

    def set_gm(self, chat_id, gm):
        if chat_id not in self.instance.keys():
            gm.playerO.sym = "⚪"
            gm.playerX.sym = "❌"
            self.instance[chat_id] = gm

    def get_gm(self, chat_id):
        return self.instance[chat_id]

    def set_last_message(self, chat_id, message_id):
        if chat_id in self.message_ids.keys():
            self.message_ids[chat_id].append(message_id)
        else:
            self.message_ids[chat_id] = [message_id]

    def pop_last_message(self, chat_id):
        if chat_id in self.message_ids:
            for message_id in self.message_ids[chat_id]:
                bot.delete_message(chat_id, message_id)
            self.message_ids.pop(chat_id)


def board(gm):
    buttons = []
    for i in gm.spaces:
        buttons.append(InlineKeyboardButton(f'{i}', callback_data=f'move {i}'))
    keyboard = Keyboa(items=buttons, items_in_row=3)
    return keyboard


@bot.callback_query_handler(func=lambda call: True and call.data.startswith('ng'))
def new_game_check(call):
    new = call.data.split()[1]
    if new == 'yes':
        start(call.message)
    else:
        bot.send_message(call.message.chat.id, "Game over!")


@bot.callback_query_handler(func=lambda call: True and call.data.startswith('move'))
def move_check(call):
    move = call.data.split()
    move = move[1]
    gm = s.get_gm(call.message.chat.id)
    player_id = call.from_user.id
    current_player_id = gm.player.id
    if player_id != current_player_id:
        bot.answer_callback_query(call.id, "Chờ đợi đến lượt của bạn")
    else:
        try:
            move = int(move)
        except ValueError:
            bot.answer_callback_query(call.id, "Ô đã bị chiếm")
        else:
            gm.move(move)
            win_check(call.message)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith('người chơi'))
def get_players(call):
    player_id = call.from_user.id
    player_name = call.from_user.first_name
    gm = s.get_gm(call.message.chat.id)

    if player_id not in [gm.playerX.id, gm.playerO.id]:
        if not gm.playerX.id:
            gm.playerX.name = player_name
            gm.playerX.id = player_id
            bot.send_message(call.message.chat.id, f"Người chơi 1: {player_name} ({gm.playerX.sym})")
        elif not gm.playerO.id:
            gm.playerO.name = player_name
            gm.playerO.id = player_id
            bot.send_message(call.message.chat.id, f"Người chơi 2: {player_name} ({gm.playerO.sym})")
    else:
        bot.answer_callback_query(call.id, "Chờ người chơi 2")

    if gm.playerO.id and gm.playerX.id:
        gm.reset()
        start(call.message)


@bot.message_handler(commands=['start'], chat_types=['group'])
def begin_mp(message):
    bot.send_message(message.chat.id, "Caro: nhiều người chơi")
    gm = logic.Game()
    s.set_gm(message.chat.id, gm)
    gm.full_reset()
    gm.mode = 2
    gm.playerO.id = None
    gm.playerX.id = None
    keyboard = Keyboa(items=InlineKeyboardButton('Play', callback_data='players'), items_in_row=2)
    bot.send_message(chat_id=message.chat.id, text="Chờ người chơi...", reply_markup=keyboard())


@bot.message_handler(commands=['start'], chat_types=['private'])
def begin_sp(message):
    bot.send_message(message.chat.id, "Caro: 1 người chơi")
    gm = logic.Game()
    s.set_gm(message.chat.id, gm)
    gm.reset()
    gm.mode = 1
    gm.playerO.name = 'AI'
    gm.playerX.id = message.chat.id
    gm.playerX.name = message.chat.first_name
    start(message)


@bot.message_handler(commands=['help'], chat_types=['group', 'private'])
def help_message(message):
    text = """
   Xin chào!
    Đây là một bot Caro. Bạn có thể chơi ở chế độ đơn chống lại AI
    hoặc ở chế độ nhiều người chơi theo nhóm (thêm bot vào nhóm của bạn để chơi).
    Tên người dùng bot: @tic_tac_t0e_bot
    New game: /start
    """
    bot.send_message(message.chat.id, dedent(text))


@bot.message_handler(commands=['cancel'], chat_types=['group', 'private'])
def begin(message):
    bot.send_message(message.chat.id, 'Trò chơi bị hủy')
    gm = s.get_gm(message.chat.id)
    gm.full_reset()


def start(message):
    gm = s.get_gm(message.chat.id)
    gm.player = next(gm.cycler)
    s.pop_last_message(message.chat.id)

    if gm.player.id == 1 and gm.mode == 1:
        gm.move(gm.ai_move())
        win_check(message)
    elif gm.player.name == 'Draw':
        win_check(message)
    else:
        text = f"Player: {gm.player.name} ( {gm.player.sym} )\nNhấn [1-9] để chơi"
        keyboard = board(gm)
        message_id = bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard()).message_id
        s.set_last_message(message.chat.id, message_id)


def win_check(message):
    gm = s.get_gm(message.chat.id)
    winner = gm.win_check()
    if winner:
        keyboard = board(gm)
        bot.send_message(chat_id=message.chat.id, text=f"Người thắng: {winner.name}", reply_markup=keyboard())
        text = ""
        for i in gm.player_list:
            text += f"{i.name}: {i.total_score}\n"
        bot.send_message(message.chat.id, text)
        gm.reset()
        buttons = [InlineKeyboardButton('Yes', callback_data='ng yes'),
                   InlineKeyboardButton('No', callback_data='ng no')]
        keyboard = Keyboa(items=buttons, items_in_row=2)
        message_id = bot.send_message(chat_id=message.chat.id, text="Chơi lại?", reply_markup=keyboard()).message_id
        s.set_last_message(message.chat.id, message_id)
    else:
        start(message)


if __name__ == '__main__':
    s = States()
    bot.infinity_polling()
