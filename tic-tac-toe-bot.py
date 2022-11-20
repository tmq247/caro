import telebot
from telebot.types import InlineKeyboardButton
import logic
import os
from dotenv import load_dotenv, find_dotenv
from keyboa import Keyboa
from textwrap import dedent

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


def board():
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
    player_id = call.from_user.id
    current_player_id = gm.player.id
    if player_id != current_player_id:
        bot.answer_callback_query(call.id, "Wait for your turn")
    else:
        try:
            move = int(move)
        except ValueError:
            bot.answer_callback_query(call.id, "Cell occupied")
        else:
            gm.move(move)
            win_check(call.message)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith('players'))
def get_players(call):
    player_id = call.from_user.id
    player_name = call.from_user.first_name

    if player_id not in [gm.playerX.id, gm.playerO.id]:
        if not gm.playerX.id:
            gm.playerX.name = player_name
            gm.playerX.id = player_id
            bot.send_message(call.message.chat.id, f"Player 1: {player_name} ({gm.playerX.sym})")
        elif not gm.playerO.id:
            gm.playerO.name = player_name
            gm.playerO.id = player_id
            bot.send_message(call.message.chat.id, f"Player 2: {player_name} ({gm.playerO.sym})")
    else:
        bot.answer_callback_query(call.id, "Wait for player 2")

    if gm.playerO.id and gm.playerX.id:
        gm.reset()
        start(call.message)


@bot.message_handler(commands=['start'], chat_types=["group"])
def begin(message):
    bot.send_message(message.chat.id, "Tic-tac-toe: Multiplayer")
    gm.full_reset()
    gm.mode = 2
    gm.playerO.id = None
    gm.playerX.id = None
    keyboard = Keyboa(items=InlineKeyboardButton("Play", callback_data='players'), items_in_row=2)
    bot.send_message(chat_id=message.chat.id, text="Waiting for players...", reply_markup=keyboard())


@bot.message_handler(commands=['start'], chat_types=["private"])
def begin(message):
    bot.send_message(message.chat.id, "Tic-tac-toe: Single player")
    gm.reset()
    gm.mode = 1
    gm.playerO.name = "AI"
    gm.playerX.id = message.chat.id
    gm.playerX.name = message.chat.first_name
    start(message)


@bot.message_handler(commands=['help'], chat_types=["group", "private"])
def begin(message):
    text = """
    Hello! 
    This is a tic-tac-toe bot. You can play in single mode against AI
    or in multiplayer mode in groups (add the bot to your group to play).
    Bot username: @tic_tac_t0e_bot
    New game: /start
    """
    bot.send_message(message.chat.id, dedent(text))


@bot.message_handler(commands=['cancel'], chat_types=["group", "private"])
def begin(message):
    bot.send_message(message.chat.id, "Game cancelled")
    gm.full_reset()


def start(message):
    gm.player = next(gm.cycler)

    if message.chat.id in message_ids:
        print("delete: ", message_ids)
        for message_id in message_ids[message.chat.id]:
            bot.delete_message(message.chat.id, message_id)
        message_ids.pop(message.chat.id)

    if gm.player == gm.playerO and gm.mode == 1:
        gm.move(gm.ai_move())
        win_check(message)
    elif gm.player.name == 'Draw':
        win_check(message)
    else:
        text = f"Player: {gm.player.name} ( {gm.player.sym} )\nPress [1-9] to play"
        keyboard = board()
        message_id = bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard()).message_id
        collector(message.chat.id, message_id)


def win_check(message):
    winner = gm.win_check()
    if winner:
        keyboard = board()
        bot.send_message(chat_id=message.chat.id, text=f"Winner: {winner.name}", reply_markup=keyboard())
        text = ""
        for i in logic.Players.player_list:
            text += f"{i.name}: {i.total_score}\n"
        bot.send_message(message.chat.id, text)
        gm.reset()
        buttons = [InlineKeyboardButton("Yes", callback_data='ng yes'),
                   InlineKeyboardButton("No", callback_data='ng no')]
        keyboard = Keyboa(items=buttons, items_in_row=2)
        message_id = bot.send_message(chat_id=message.chat.id, text="Play again?", reply_markup=keyboard()).message_id
        collector(message.chat.id, message_id)
    else:
        start(message)


def collector(chat_id, message_id):
    if chat_id in message_ids.keys():
        message_ids[chat_id].append(message_id)
    else:
        message_ids[chat_id] = [message_id]


if __name__ == '__main__':
    message_ids = {}
    gm = logic.Game()
    gm.playerO.sym = "⚪"
    gm.playerX.sym = "❌"
    bot.infinity_polling()
