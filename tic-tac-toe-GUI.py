from tkinter import *
from tkinter.ttk import *
import logic

window = Tk()
window.geometry("300x300")
window.title("Tic Tac Toe")
window.eval('tk::PlaceWindow . center')
gm = logic.Game()
gm.playerO.sym = "⚪"
gm.playerX.sym = "❌"


def start(mode):
    hello.pack_forget()
    gm.mode = mode
    gm.player = next(gm.cycler)
    info['text'] = gm.player.name
    for i in range(len(gm.spaces)):
        buttons[i].configure(text=gm.spaces[i])

    if gm.player == gm.playerO and gm.mode == 1:
        gm.move(gm.ai_move())
        win_check()
    elif gm.player.name == 'Draw':
        win_check()


def win_check():
    winner = gm.win_check()
    if winner:
        text = f"Winner: {winner.name}"
        for i in gm.player_list:
            text += f"\n{i.name}: {i.total_score}"
        top = Toplevel(window)
        top.geometry("100x130")
        top.title("Game over")
        Label(top, text=text).pack()
        Button(top, text="Again", command=lambda: [gm.reset(), start(gm.mode), top.destroy()]).pack()
        Button(top, text="Quit", command=quit).pack()
        window.eval(f'tk::PlaceWindow {str(top)} center')
    start(gm.mode)


def check_input(play):
    if isinstance(gm.spaces[play], int):
        gm.move(play + 1)
        win_check()
    else:
        info['text'] = "Cell occupied"


btn_nr = 0
buttons = []

board = Frame()
for x in range(1, 4):
    for y in range(1, 4):
        buttons.append(Button(board, text=gm.spaces[btn_nr], command=lambda n=btn_nr: check_input(n)))
        buttons[btn_nr].grid(row=x, column=y, ipady=25, ipadx=10)
        btn_nr += 1

label = Frame()
info = Label(label, text="Select game mode")
info.pack()

hello = Frame()
Button(hello, text="Single player", command=lambda: [start(1), hello.pack_forget()]).grid(column=1, row=1)
Button(hello, text="Multiplayer", command=lambda: [start(2), hello.pack_forget()]).grid(column=2, row=1)

board.pack()
label.pack()
hello.pack()

if __name__ == '__main__':
    window.mainloop()
