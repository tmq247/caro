import logic
from termcolor import colored
from tabulate import tabulate


def start():
    gm.player = next(gm.cycler)

    if gm.player == gm.playerO and gm.mode == 1:
        gm.move(gm.ai_move())
    elif gm.player.name == 'Draw':
        pass
    else:
        print(board())
        print(f"Người chơi: ( {gm.player.sym} )")
        gm.move(check_input("Bấm [1-9] để chơi, [0] để thoát:\n", gm.spaces))

    winner = gm.win_check()
    if winner:
        print(board())
        print('=' * 20)
        print(f"Winner: {winner.name}")
        for i in gm.player_list:
            print(f"{i.name}: {i.total_score}")
        print('=' * 20)
        again()

    start()


def board():
    brd = []
    for i in range(0, len(gm.spaces), 3):
        brd.append(gm.spaces[i:i + 3])
    return tabulate(brd, tablefmt="rounded_grid")


def again():
    _again = check_input("Chơi lại?\n[1]: Game mới\n[2]: Thoát\n", (1, 2))
    if _again == 1:
        gm.reset()
        start()
    else:
        exit(0)


def check_input(text, values):
    while True:
        var = input(text)
        try:
            var = int(var)
            if var == 0:
                exit(0)
            elif var not in values:
                raise ValueError
        except ValueError:
            print("Chọn 1 số")
            continue
        else:
            return var


if __name__ == '__main__':
    gm = logic.Game()
    gm.playerO.sym = colored("O", "blue", attrs=["bold"])
    gm.playerX.sym = colored("X", "red", attrs=["bold"])
    print("Tic-tac-toe")
    gm.mode = check_input("Chọn chế độ\n[1]: 1 người\n[2]: Nhiều người\n", (1, 2))
    start()
