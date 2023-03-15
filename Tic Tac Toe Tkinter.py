from tkinter import *


class TicTacToe:

    def __init__(self, compvar: bool, frontend: list, banner) -> None:

        self.computer = compvar.get()
        self.frontend = frontend

        self.board_O = 0
        self.board_X = 0

        self.turn    = True
        self.running = True
        self.banner  = banner
        self.compvar = compvar


    def player_turn(self, cord) -> None:

        if not self.running or (self.board_X | self.board_O) & (1 << cord):
            return
        
        if self.turn:
            self.board_O ^= 1 << cord
        elif not self.turn:
            self.board_X ^= 1 << cord
        
        self.turn = not self.turn

        self.update_game()

        if self.computer:
            self.computer_turn()
    

    def computer_turn(self) -> None:

        if not self.running:
            return

        eval = TicTacToe.minimax(self.board_O, self.board_X, self.turn)
        self.board_X ^= 1 << eval[2]

        self.update_game()

        self.turn = not self.turn


    @staticmethod
    def minimax(pos_O, pos_X, is_max_player: bool, depth=0) -> tuple:

        static_eval = TicTacToe.static_eval(pos_O, pos_X)

        if static_eval is not None:
            return (static_eval, depth)

        board = pos_O | pos_X
        
        if is_max_player:
            max_val = [-2]

            for i in range(9):
                if board & (1 << i) == 0:
                    val = TicTacToe.minimax(pos_O ^ (1 << i), pos_X, False, depth + 1)

                    if val[0] > max_val[0] or (val[0] == max_val[1] and val[1] < max_val[1]):
                        max_val = (val[0], val[1], i)

            return max_val
        else:
            min_val = [2]
            
            for i in range(9):
                if board & (1 << i) == 0:
                    val = TicTacToe.minimax(pos_O, pos_X ^ (1 << i), True, depth + 1)

                    if val[0] < min_val[0] or (val[0] == min_val[1] and val[1] < min_val[1]):
                        min_val = (val[0], val[1], i)

            return min_val
    

    @staticmethod
    def static_eval(board_O, board_X) -> int:

        CONDITIONS = [
            0b001001001, 0b111000000, 0b100010001,
            0b010010010, 0b000111000, 0b001010100,
            0b100100100, 0b000000111
        ]

        for condition in CONDITIONS:
            if (condition & board_O) == condition:
                return 1
            if (condition & board_X) == condition:
                return -1

        if board_O | board_X == 511:
            return 0
    

    def update_game(self) -> None:

        for g in range(9):
            button = self.frontend[g//3][g%3]
            
            if 1 << g & self.board_O:
                button["text"] = "O"
                button["fg"] = "#D0E4CD"
            elif 1 << g & self.board_X:
                button["text"] = "X"
                button["fg"] = "#535454"
        
        winlose = self.static_eval(self.board_O, self.board_X)

        if winlose == -1:
            self.banner["text"] = "  X wins! ⟳"
            self.draw_winning_line(False)
        elif winlose == 1:
            self.banner["text"] = "  O wins! ⟳"
            self.draw_winning_line(True)
        elif winlose == 0:
            self.banner["text"] = "   Draw!  ⟳"
        
        if winlose is not None:
            self.running = False
    

    def draw_winning_line(self, is_O: bool) -> None:

        CONDITIONS = [
            0b001001001, 0b111000000, 0b100010001,
            0b010010010, 0b000111000, 0b001010100,
            0b100100100, 0b000000111
        ]

        board = self.board_O if is_O else self.board_X

        for condition in CONDITIONS:
            if (condition & board) == condition:
                for i in range(9):
                    if condition & (1 << i):
                        self.frontend[i//3][i%3]["fg"] = "#0072A3"
                return

    
    def restart(self, _, force=False, computer=None) -> None:

        if computer is not None:
            self.compvar.set(computer)
        

        if self.running and not force:
            return

        for row in self.frontend:
            for button in row:
                button["text"] = ""

        self.banner["text"] = "Tic Tac Toe"
        
        self.running = True
        self.board_O = 0
        self.board_X = 0
        self.turn = True
        self.computer = self.compvar.get()


def main():

    root = Tk()

    root.title("Tic Tac Toe")
    root.geometry("250x375")
    root.resizable(False, False)
    root.configure(bg="#13B9A8", pady=10)

    computer = IntVar(value=1)
    game = None

    menubar = Menu(root)
    options = Menu(menubar, tearoff=0)
    newgame = Menu(options, tearoff=0)
    
    menubar.add_cascade(label="Options",  menu=options)
    options.add_cascade(label="New game", menu=newgame)

    newgame.add_radiobutton(label="1 player",  command=lambda:game.restart(None, True, True))
    newgame.add_radiobutton(label="2 players", command=lambda:game.restart(None, True, False))
    
    options.add_separator()
    options.add_command(label="quit", command=root.destroy)
    root.config(menu=menubar)


    #Main game
    frm = Frame(root, width=250, height=300, bg="#0D9688")
    lbl = Label(root, text="Tic Tac Toe", font="Helvtica 28 bold", fg="#D0E4CD", bg="#13B9A8", pady=5)
    
    lbl.pack(side="top")
    frm.pack(side="bottom")

    button_grid = [[None]*3 for _ in range(3)]
    game = TicTacToe(computer, button_grid, lbl)

    lbl.bind("<ButtonRelease-1>", game.restart)

    for row in range(3):
        for col in range(3):
            button = Label(frm, height=2, width=3, font="ariel 26 bold", bg="#13B9A8")

            button.bind("<ButtonRelease-1>", lambda _, x=row, y=col: game.player_turn(3*x + y))
            button_grid[row][col] = button

            padx_r = 0 if col == 0 else 5
            padx_l = 0 if col == 2 else 5
            pady_u = 0 if row == 0 else 5
            pady_d = 0 if row == 2 else 5

            button.grid(row=row, column=col, padx=(padx_r, padx_l), pady=(pady_u, pady_d))

    root.mainloop()

if __name__ == "__main__":
    main()
