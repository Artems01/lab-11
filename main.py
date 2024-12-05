import tkinter as tk
from tkinter import messagebox


class Checkers:
    # Инициализация игры: создание доски, установка текущего игрока, связывание с UI
    def __init__(self, root):
        self.root = root
        self.root.title("Checkers")
        self.board = self.create_board()
        self.current_player = 'W'  # 'W' for White, 'B' for Black
        self.selected_piece = None
        self.valid_moves = []
        self.create_ui()
        self.center_window(400, 400)

    # Центрирование окна на экране
    def center_window(self, width, height):
        screen_width = root .winfo_screenwidth()
        screen_height = root .winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    # Создание игровой доски с начальным расположением шашек
    def create_board(self):
        board = [['' for _ in range(8)] for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'B'
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'W'
        return board

    # Создание графического интерфейса: холст для отрисовки, обработчик событий клика
    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    # Отрисовка доски и шашек на холсте
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board[row][col]
                if piece:
                    color = 'white' if piece[0] == 'W' else 'black'
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color)
                    if 'Q' in piece: #Add a 'Q' to indicate a queen
                        self.canvas.create_text(x1 + 25, y1 + 25, text='Q', fill='red')

    # Обработка клика мыши: выбор шашки, проверка допустимых ходов, перемещение шашки
    def on_click(self, event):
        col = event.x // 50
        row = event.y // 50

        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.move_piece(row, col)
                if not self.check_game_over():
                    self.current_player = 'B' if self.current_player == 'W' else 'W'  # Switch player
            else:
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()
        else:
            piece = self.board[row][col]
            if piece and piece[0] == self.current_player:
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)
                self.highlight_moves()

    # Подсветка допустимых ходов на доске
    def highlight_moves(self):
        for move in self.valid_moves:
            row, col = move
            x1 = col * 50
            y1 = row * 50
            x2 = x1 + 50
            y2 = y1 + 50
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=3)


    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        is_queen = 'Q' in piece
        valid_moves = []

        if is_queen:  # Queen moves
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    if not self.board[new_row][new_col]:
                        valid_moves.append((new_row, new_col))
                    elif self.board[new_row][new_col][0] != piece[0]:
                        jump_row, jump_col = new_row + dr, new_col + dc
                        if 0 <= jump_row < 8 and 0 <= jump_col < 8 and not self.board[jump_row][jump_col]:
                            valid_moves.append((jump_row, jump_col))
                        break
                    else:
                        break
                    new_row, new_col = new_row + dr, new_col + dc
        else:  # Pawn moves
            directions = [(-1, -1), (-1, 1)] if piece == 'W' else [(1, -1), (1, 1)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if not self.board[new_row][new_col]:
                        valid_moves.append((new_row, new_col))
                    elif self.board[new_row][new_col][0] != piece[0]:
                        jump_row, jump_col = new_row + dr, new_col + dc
                        if 0 <= jump_row < 8 and 0 <= jump_col < 8 and not self.board[jump_row][jump_col]:
                            valid_moves.append((jump_row, jump_col))
        return valid_moves


    def move_piece(self, row, col):
        old_row, old_col = self.selected_piece

        # Если происходит взятие фишки
        if abs(row - old_row) == 2:
            middle_row = (old_row + row) // 2
            middle_col = (old_col + col) // 2
            self.board[middle_row][middle_col] = ''  # Удаляем взятую фишку

        # Перемещаем фишку
        self.board[row][col] = self.board[old_row][old_col]
        self.board[old_row][old_col] = ''
        self.selected_piece = None
        self.valid_moves = []
        self.draw_board()
        self.check_for_queen()  # Проверка продвижения королевы

    # Проверка на превращение пешек в ферзей
    def check_for_queen(self):
        for col in range(8):
            if self.board[0][col] == 'W':
                self.board[0][col] = 'WQ'
            if self.board[7][col] == 'B':
                self.board[7][col] = 'BQ'
        self.draw_board()

    # Проверка на окончание игры
    def check_game_over(self):
        white_pieces = any('W' in row or 'WQ' in row for row in self.board)
        black_pieces = any('B' in row or 'BQ' in row for row in self.board)

        if not white_pieces:
            messagebox.showinfo("Game Over", "Black wins!")
            return True
        elif not black_pieces:
            messagebox.showinfo("Game Over", "White wins!")
            return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    game = Checkers(root)
    root.mainloop()
