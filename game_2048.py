import tkinter as tk
import random
import math


# function to start the game, main function
def start_2048():
    class Game(tk.Tk):
        # board variable
        board = []
        # to create probability distribution to randomly select next tile number
        new_tile_selection = [2, 2, 2, 2, 2, 2, 4]
        # tile colors for different numbered tiles
        tile_colors = ["#f5f5f5", "#e0f2f8", "#b8dbe5", "#71b1bd", "#27819f", "#0073b9", "#7fa8d7", "#615ea6",
                       "#2f3490",
                       "#1c1862", "#9c005d", "#c80048"]

        score = 0
        highscore = 0
        scorestring = 0
        highscorestring = 0

        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            self.buttonframe = tk.Frame(self)
            self.square = {}
            self.scorestring = tk.StringVar(self)
            self.scorestring.set("0")
            self.highscorestring = tk.StringVar(self)
            self.highscorestring.set("0")
            self.create_widgets()
            # size of window
            self.canvas = tk.Canvas(
                self, width=800, height=800, borderwidth=5, highlightthickness=0)
            self.canvas.pack(side="top", fill="both", expand="false")

            # start new game
            self.new_game()

        def add_new_tile(self):
            # select random index from probability distribution
            index = random.randint(0, 6)
            while not self.is_full():
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                # retry if block of board is filled
                if self.board[x][y] != 0:
                    continue
                self.board[x][y] = self.new_tile_selection[index]

                # print new tile
                x1 = y * 210
                y1 = x * 210
                x2 = x1 + 210 - 5
                y2 = y1 + 210 - 5
                num = self.board[x][y]
                if num == 2:
                    self.square[x, y] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e0f2f8", tags="rect",
                                                                     outline="", width=0)
                    self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill="#ffb459", text="2")
                elif num == 4:
                    self.square[x, y] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#b8dbe5", tags="rect",
                                                                     outline="", width=0)
                    self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill="#ffb459", text="4")

                break

        # Returns True if board is full
        def is_full(self):
            for i in range(0, 4):
                for j in range(0, 4):
                    if self.board[i][j] == 0:
                        return False
            return True

        # Prints game board
        def print_board(self):
            cellwidth = 210
            cellheight = 210

            for column in range(4):
                for row in range(4):
                    x1 = column * cellwidth
                    y1 = row * cellheight
                    x2 = x1 + cellwidth - 5
                    y2 = y1 + cellheight - 5
                    num = self.board[row][column]
                    self.print_tile(row, column, x1, y1, x2, y2, num)

        # prints a single tile
        def print_tile(self, row, column, x1, y1, x2, y2, num):
            current_tile_color = self.tile_colors[0]
            if num > 0:
                current_tile_color = self.tile_colors[int(math.log2(num))]
            self.square[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                                    fill=current_tile_color, tags="rect",
                                                                    outline="")
            if num != 0:
                text_color = "#494949"
                if num > 4:
                    text_color = "white"
                self.canvas.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill=text_color, text=str(num))

        def create_widgets(self):
            self.buttonframe = tk.Frame(self)
            self.buttonframe.grid(row=2, column=0, columnspan=4)
            tk.Button(self.buttonframe, text="New Game",
                      command=self.new_game).grid(row=0, column=0)
            tk.Label(self.buttonframe, text="Score:").grid(row=0, column=1)
            tk.Label(self.buttonframe, textvariable=self.scorestring).grid(
                row=0, column=2)
            tk.Label(self.buttonframe, text="Record:").grid(row=0, column=3)
            tk.Label(self.buttonframe, textvariable=self.highscorestring).grid(
                row=0, column=4)
            self.buttonframe.pack(side="top")

        # actions to perform for which key pressed
        def key_pressed(self, event):
            # move all tiles downward if pressed down arrow key
            if event.keysym == 'Down':
                for j in range(0, 4):
                    shift = 0
                    for i in range(3, -1, -1):
                        if self.board[i][j] == 0:
                            shift += 1
                        else:
                            if i - 1 >= 0 and self.board[i - 1][j] == self.board[i][j]:
                                self.board[i][j] *= 2
                                self.score += self.board[i][j]
                                self.board[i - 1][j] = 0
                            elif i - 2 >= 0 and self.board[i - 1][j] == 0 and self.board[i - 2][j] == self.board[i][j]:
                                self.board[i][j] *= 2
                                self.score += self.board[i][j]
                                self.board[i - 2][j] = 0
                            elif i == 3 and self.board[2][j] + self.board[1][j] == 0 and self.board[0][j] == \
                                    self.board[3][
                                        j]:
                                self.board[3][j] *= 2
                                self.score += self.board[3][j]
                                self.board[0][j] = 0
                            if shift > 0:
                                self.board[i + shift][j] = self.board[i][j]
                                self.board[i][j] = 0
                self.print_board()
                self.add_new_tile()
                self.is_over()

            # move all tiles in right direction if pressed right arrow key
            elif event.keysym == 'Right':
                for i in range(0, 4):
                    shift = 0
                    for j in range(3, -1, -1):
                        if self.board[i][j] == 0:
                            shift += 1
                        else:
                            if j - 1 >= 0 and self.board[i][j - 1] == self.board[i][j]:
                                self.board[i][j] *= 2
                                self.score += self.board[i][j]
                                self.board[i][j - 1] = 0
                            elif j - 2 >= 0 and self.board[i][j - 1] == 0 and self.board[i][j - 2] == self.board[i][j]:
                                self.board[i][j] *= 2
                                self.score += self.board[i][j]
                                self.board[i][j - 2] = 0
                            elif j == 3 and self.board[i][2] + self.board[i][1] == 0 and self.board[0][j] == \
                                    self.board[3][
                                        j]:
                                self.board[i][3] *= 2
                                self.score += self.board[i][3]
                                self.board[i][0] = 0
                            if shift > 0:
                                self.board[i][j + shift] = self.board[i][j]
                                self.board[i][j] = 0
                self.print_board()
                self.add_new_tile()
                self.is_over()

            # move all tiles in left direction if left arrow key is pressed
            elif event.keysym == 'Left':
                for i in range(0, 4):
                    shift = 0
                    for j in range(0, 4):
                        if self.board[i][j] == 0:
                            shift += 1
                        else:
                            if j + 1 < 4 and self.board[i][j + 1] == self.board[i][j]:
                                self.board[i][j] *= 2
                                self.score += self.board[i][j]
                                self.board[i][j + 1] = 0
                            elif j + 2 < 4 and self.board[i][j + 1] == 0 and self.board[i][j + 2] == self.board[i][j]:
                                self.board[i][j] *= 2
                                self.score += self.board[i][j]
                                self.board[i][j + 2] = 0
                            elif j == 0 and self.board[i][1] + self.board[i][2] == 0 and self.board[i][3] == \
                                    self.board[i][
                                        0]:
                                self.board[i][0] *= 2
                                self.score += self.board[i][0]
                                self.board[i][3] = 0
                            if shift > 0:
                                self.board[i][j - shift] = self.board[i][j]
                                self.board[i][j] = 0
                self.print_board()
                self.add_new_tile()
                self.is_over()

            # move all tiles in up direction is up arrow key is pressed
            elif event.keysym == 'Up':
                for j in range(0, 4):
                    shift = 0
                    for i in range(0, 4):
                        if self.board[i][j] == 0:
                            shift += 1
                        else:
                            if i + 1 < 4 and self.board[i + 1][j] == self.board[i][j]:
                                self.board[i][j] *= 2
                                self.score += self.board[i][j]
                                self.board[i + 1][j] = 0
                            elif i + 2 < 4 and self.board[i + 1][j] == 0 and self.board[i + 2][j] == self.board[i][j]:
                                self.board[i][j] *= 2
                                self.score += self.board[i][j]
                                self.board[i + 2][j] = 0
                            elif i == 0 and self.board[1][j] + self.board[2][j] == 0 and self.board[3][j] == \
                                    self.board[0][
                                        j]:
                                self.board[0][j] *= 2
                                self.score += self.board[0][j]
                                self.board[3][j] = 0
                            if shift > 0:
                                self.board[i - shift][j] = self.board[i][j]
                                self.board[i][j] = 0
                self.print_board()
                self.add_new_tile()
                self.is_over()
            self.scorestring.set(str(self.score))
            if self.score > self.highscore:
                self.highscore = self.score
                self.highscorestring.set(str(self.highscore))

        # initialize and start a new game
        def new_game(self):
            self.score = 0
            self.scorestring.set("0")
            # clean and reinitialize board
            self.board = []
            self.board.append([0, 0, 0, 0])
            self.board.append([0, 0, 0, 0])
            self.board.append([0, 0, 0, 0])
            self.board.append([0, 0, 0, 0])
            while True:
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                if self.board[x][y] == 0:
                    self.board[x][y] = 2
                    break

            index = random.randint(0, 6)
            while not self.is_full():
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                if self.board[x][y] == 0:
                    self.board[x][y] = self.new_tile_selection[index]
                    break
            self.print_board()

        # check and take action if game is over
        def is_over(self):

            # conditions at which game is over
            for i in range(0, 4):
                for j in range(0, 4):
                    if self.board[i][j] == 2048:
                        self.you_won()
            for i in range(0, 4):
                for j in range(0, 4):
                    if self.board[i][j] == 0:
                        return False
            for i in range(0, 4):
                for j in range(0, 3):
                    if self.board[i][j] == self.board[i][j + 1]:
                        return False
            for j in range(0, 4):
                for i in range(0, 3):
                    if self.board[i][j] == self.board[i + 1][j]:
                        return False

            # print game over
            gameover = [["G", "A", "M", "E", ], ["O", "V", "E", "R"], [
                "", "", "", ""], ["", "", "", ""]]
            cellwidth = 210
            cellheight = 210
            self.square = {}

            for column in range(4):
                for row in range(4):
                    x1 = column * cellwidth
                    y1 = row * cellheight
                    x2 = x1 + cellwidth - 10
                    y2 = y1 + cellheight - 10
                    self.square[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e0f2f8", tags="rect",
                                                                            outline="")
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill="#494949",
                                            text=gameover[row][column])
            return True

        # print you won
        def you_won(self):
            gameover = [["Y", "O", "U", "", ], ["W", "O", "N", "!"], [
                "", "", "", ""], ["", "", "", ""]]
            cellwidth = 210
            cellheight = 210
            self.square = {}
            for column in range(4):
                for row in range(4):
                    x1 = column * cellwidth
                    y1 = row * cellheight
                    x2 = x1 + cellwidth - 5
                    y2 = y1 + cellheight - 5
                    self.square[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e0f2f8", tags="rect",
                                                                            outline="")
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill="#494949",
                                            text=gameover[row][column])

    app = Game()
    app.bind_all('<Key>', app.key_pressed)
    app.wm_title("2048 Game")
    app.minsize(840, 850)
    app.maxsize(840, 850)
    app.mainloop()
