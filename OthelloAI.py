import random
import copy
import tkinter as tk

class UserAI:
    def choose_move(self, board, player):
        return None

class OthelloGUI(tk.Tk):
    def __init__(self, board, game):
        super().__init__()
        self.board = board
        self.game = game
        self.title("Othello")
        self.board_size = 8
        self.cell_size = 50
        self.canvas = tk.Canvas(self, width=self.cell_size * self.board_size, height=self.cell_size * self.board_size, bg="darkgreen")
        self.canvas.pack()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        for i in range(self.board_size + 1):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.board_size * self.cell_size)
            self.canvas.create_line(0, i * self.cell_size, self.board_size * self.cell_size, i * self.cell_size)

        self.canvas.bind("<Button-1>", self.game.user_click)

        self.update_display()

    def update_display(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board.board[x][y] == -1:
                    self.canvas.create_oval(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill="black")
                elif self.board.board[x][y] == 1:
                    self.canvas.create_oval(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill="white")

        self.canvas.update()

    def on_closing(self):
        self.destroy()
        self.quit()

class OthelloBoard:
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.board[3][3] = self.board[4][4] = 1
        self.board[3][4] = self.board[4][3] = -1

    def display(self):
        for row in self.board:
            print(' '.join(['B' if x == -1 else 'W' if x == 1 else '.' for x in row]))
        print()

    def is_valid_move(self, move, player):
        x, y = move
        if self.board[x][y] != 0:
            return False

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == -player:
                    while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] != 0:
                        nx += dx
                        ny += dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == player:
                            return True

        return False

    def get_valid_moves(self, player):
        moves = [(x, y) for x in range(self.board_size) for y in range(self.board_size) if self.is_valid_move((x, y), player)]
        return moves

    def has_valid_moves(self, player):
        return any(self.is_valid_move((x, y), player) for x in range(self.board_size) for y in range(self.board_size))

    def make_move(self, move, player):
        x, y = move
        self.board[x][y] = player

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == -player:
                    while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] != 0:
                        nx += dx
                        ny += dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == player:
                            nx -= dx
                            ny -= dy
                            while (nx, ny) != (x, y):
                                self.board[nx][ny] = player
                                nx -= dx
                                ny -= dy
                            break

    def count_pieces(self):
        black_count = sum(row.count(-1) for row in self.board)
        white_count = sum(row.count(1) for row in self.board)
        return black_count, white_count

    def get_winner(self):
        black_count, white_count = self.count_pieces()
        if black_count > white_count:
            return -1
        elif black_count < white_count:
            return 1
        else:
            return 0

    def copy_board(self):
        new_board = OthelloBoard(board_size=self.board_size)
        new_board.board = [row.copy() for row in self.board]
        return new_board

    def game_over(self):
        return not (self.has_valid_moves(1) or self.has_valid_moves(-1))

    def copy(self):
        new_board = OthelloBoard()
        new_board.board = copy.deepcopy(self.board)
        return new_board

class RandomAI:
    def choose_move(self, board, player):
        moves = board.get_valid_moves(player)
        return random.choice(moves) if moves else None

class MinimaxAI:
    def __init__(self, depth):
        self.depth = depth
        self.BOARD_WEIGHTS = [
            [120, -20, 20,  5,  5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20,  5,  5, 20, -20, 120]
        ]

    def choose_move(self, board, player):
        _, move = self.minimax(board, player, self.depth, float('-inf'), float('inf'))
        return move

    def minimax(self, board, player, depth, alpha, beta):
        if depth == 0 or board.game_over():
            return self.evaluate(board, player), None

        best_value = float('-inf') if player == 1 else float('inf')
        best_move = None

        moves = board.get_valid_moves(player)
        moves.sort(key=lambda move: self.evaluate(board, player), reverse=True)

        for move in moves:
            next_board = board.copy()
            next_board.make_move(move, player)
            value, _ = self.minimax(next_board, -player, depth - 1, alpha, beta)

            if player == 1:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, best_move

    def evaluate(self, board, player):
        score = 0
        for x in range(board.board_size):
            for y in range(board.board_size):
                if board.board[x][y] == player:
                    score += self.BOARD_WEIGHTS[x][y]
                elif board.board[x][y] == -player:
                    score -= self.BOARD_WEIGHTS[x][y]
        return score

class Game:
    def __init__(self, board, ai_black, ai_white):
        self.board = board
        self.ai_black = ai_black
        self.ai_white = ai_white
        self.gui = OthelloGUI(board, self)

    def user_click(self, event):
        x = event.y // self.gui.cell_size
        y = event.x // self.gui.cell_size

        if self.board.is_valid_move((x, y), -1):
            self.board.make_move((x, y), -1)
            self.play()

    def play(self):
        self.gui.update_display()

        if not self.board.has_valid_moves(1):
            if not self.board.has_valid_moves(-1):
                self.gui.update_display()
                self.gui.mainloop()
                return
            return

        move = self.ai_white.choose_move(self.board, 1)
        if move is not None:
            self.board.make_move(move, 1)

        self.gui.update_display()

def main():
    board = OthelloBoard()
    ai_black = MinimaxAI(depth=5)
    ai_white = MinimaxAI(depth=5)

    game = Game(board, ai_black, ai_white)
    game.play()
    game.gui.mainloop()

main()