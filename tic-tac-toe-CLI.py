import logic
from termcolor import colored


def start():
    gm.player = next(gm.cycler)

    if gm.player == gm.playerO and gm.mode == 1:
        gm.move(gm.ai_move())
    elif gm.player.name == 'Draw':
        pass
    else:
        print(gm.board())
        print(f"Player: ( {gm.player.sym} )")
        gm.move(check_input("Enter [1-9] to play, [0] to exit:\n", gm.spaces))

    winner = gm.win_check()
    if winner:
        print(gm.board())
        print('=' * 20)
        print(f"Winner: {winner.name}")
        for i in logic.Players.player_list:
            print(f"{i.name}: {i.total_score}")
        print('=' * 20)
        again()

    start()


def again():
    _again = check_input("Play again?\n[1]: New game\n[2]: Exit\n", (1, 2))
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
            print("Enter a number")
            continue
        else:
            return var


if __name__ == '__main__':
    gm = logic.Game()
    gm.playerO.sym = colored("O", "blue", attrs=["bold"])
    gm.playerX.sym = colored("X", "red", attrs=["bold"])
    print("Tic-tac-toe")
    gm.mode = check_input("Select game mode\n[1]: Single player\n[2]: Multiplayer\n", (1, 2))
    start()
