import telebot
import random
import token_id

bot = telebot.TeleBot(token_id.token_id())


@bot.message_handler(content_types=['text'])
def start_game(massage):
    global field
    global player_id
    global count_move
    field = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    count_move = 0
    player_id = random.choice([0, 1])
    if massage.text == '/start':
        msg = bot.send_message(massage.from_user.id,
                               ('Введите "/play", чтобы провести жеребьёвку.'))
        bot.register_next_step_handler(msg, player_move)
    else:
        msg = bot.send_message(massage.from_user.id,
                               ('Введите "/start", чтобы сыграть.'))
        bot.register_next_step_handler(msg, start_game)


def player_move(massage):
    global count_move
    if massage.text == '/play':
        if player_id == 0:
            msg = bot.send_message(
                massage.from_user.id, (f'{feild_print()}\nВведите номер клетки, чтобы поставить X'))
            bot.register_next_step_handler(msg, player_move)
        if player_id == 1:
            bot_move()
            count_move += 1
            msg = bot.send_message(massage.from_user.id, (
                f'{feild_print()}\nБот сделал свой ход.\nВведите номер клетки, чтобы поставить X'))
            bot.register_next_step_handler(msg, player_move)
    else:
        n = massage.text
        if n in field:
            field[field.index(n)] = 'X'
            count_move += 1
            if count_move == 9:
                msg = bot.send_message(
                    massage.from_user.id, (f'{feild_print()}\nНичья!\nВведите "/start", чтобы сыграть ещё раз.'))
                return bot.register_next_step_handler(msg, start_game)
            if not win(field):
                bot_move()
                count_move += 1
                if count_move == 9:
                    msg = bot.send_message(
                        massage.from_user.id, (f'{feild_print()}\nНичья!\nВведите "/start", чтобы сыграть ещё раз.'))
                    return bot.register_next_step_handler(msg, start_game)
                if not win(field):
                    msg = bot.send_message(massage.from_user.id, (
                        f'{feild_print()}\nБот сделал свой ход.\nВведите номер клетки, чтобы поставить X'))
                    bot.register_next_step_handler(msg, player_move)
                else:
                    msg = bot.send_message(massage.from_user.id, (
                        f'{feild_print()}\nБот выиграл!\nВведите "/start", чтобы сыграть ещё раз.'))
                    bot.register_next_step_handler(msg, start_game)
            else:
                msg = bot.send_message(massage.from_user.id, (
                    f'{feild_print()}\nВы выиграли!\nВведите "/start", чтобы сыграть ещё раз.'))
                bot.register_next_step_handler(msg, start_game)
        else:
            msg = bot.send_message(
                massage.from_user.id, (f'{feild_print()}\nОшибка! Неверный ввод!'))
            bot.register_next_step_handler(msg, player_move)


def win(field_win):
    win_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for i in range(8):
        if field_win[win_list[i][0]] == field_win[win_list[i][1]] == field_win[win_list[i][2]]:
            return True
    return False


def bot_move():
    n = 0
    win_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for i in range(8):
        if (field[win_list[i][0]] == field[win_list[i][1]] and field[win_list[i][2]].isdigit()):
            return bot_place(win_list[i][2]+1)
        if (field[win_list[i][1]] == field[win_list[i][2]] and field[win_list[i][0]].isdigit()):
            return bot_place(win_list[i][0]+1)
        if (field[win_list[i][0]] == field[win_list[i][2]] and field[win_list[i][1]].isdigit()):
            return bot_place(win_list[i][1]+1)
    if n == 0:
        temp = [i for i in field if i != 'X' and i != 'O']
        return bot_place(random.choice(temp))


def bot_place(n):
    field[field.index(str(n))] = 'O'


def feild_print():
    return (f'\
--------------------------\n\
|   {field[0]}   |   {field[1]}   |   {field[2]}   |\n\
--------------------------\n\
|   {field[3]}   |   {field[4]}   |   {field[5]}   |\n\
--------------------------\n\
|   {field[6]}   |   {field[7]}   |   {field[8]}   |\n\
--------------------------')


bot.polling(none_stop=True, interval=0)
