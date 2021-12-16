import numpy as np
from copy import copy

from board import Board


# 0 - вільна
# 1 - червона
# 2 - синя
# 3 - зелена
# 4 - жовта
# 5 - центр
# 6 - біля останньї

class GameProcess:
    def __init__(self):
        self.directions = np.array([[-1, 0],
                                    [0, 1],
                                    [1, 0],
                                    [0, -1]])
        self.size = 7
        self.field = Board(self.size)
        self.active = False
        self.choosed_color = 1
        self.choosed_dir = 0
        self.step = 0
        self.difficulty = 1

    def clear6(self, f=None):
        if f is None:
            f = self.field
        f.matrix[f.matrix == 6] = 0

    def add(self, color, direction, posY, posX, f=None):
        if f is None:
            f = self.field
        if f.color_nums[color - 1] <= 0:
            return -1
        if color not in [1, 2, 3, 4] or direction not in [0, 1]:
            return -1

        if direction == 0:  # if vertical
            new_board = np.array([[posY, posX], [posY - 1, posX]])
        else: # if horizontal
            new_board = np.array([[posY, posX], [posY, posX + 1]])

        if np.any(new_board > 6) or np.any(new_board < 0):
            return -1
        if f.matrix[new_board[0, 0], new_board[0, 1]] != 0 or f.matrix[new_board[1, 0], new_board[1, 1]] != 0:
            return -1

        f.matrix[new_board[0, 0], new_board[0, 1]], f.matrix[new_board[1, 0], new_board[1, 1]] = color, color

        self.clear6(f) # clearing grey cells

        for d in self.directions: # and placing new grey cells
            for n in new_board:
                neib = n + d
                if np.all(neib >= 0) and np.all(neib < 7):
                    if f.matrix[neib[0], neib[1]] == 0:
                        f.matrix[neib[0], neib[1]] = 6
        f.color_nums[color - 1] -= 1

    def possibility(self, f=None):
        if f is None:
            f = self.field
        res = 0
        for i in range(self.size):
            for j in range(self.size):
                if f.matrix[i, j] == 0:
                    for d in self.directions:
                        pos = np.array([i, j]) + d
                        if np.all(pos >= 0) and np.all(pos < 7) and f.matrix[pos[0], pos[1]] == 0:
                            return 2
                elif f.matrix[i, j] == 6:
                    for d in self.directions:
                        pos = np.array([i, j]) + d
                        if np.all(pos >= 0) \
                                and np.all(pos < 7) \
                                and (f.matrix[pos[0], pos[1]] == 0 or f.matrix[pos[0], pos[1]] == 6):
                            res = 1
        return res

    def clear_group(self, field, color, current_pos):
        for d in self.directions:
            next_pos = current_pos + d
            if np.all(next_pos >= 0) and np.all(next_pos < 7) and field[next_pos[0], next_pos[1]] == color:
                field[next_pos[0], next_pos[1]] = 0
                field = self.clear_group(field, color, next_pos)
        return field

    def n_groups(self, f=None):
        if f is None:
            f = self.field
        res = 0
        field = np.copy(f.matrix)

        for i in range(self.size):
            for j in range(self.size):
                if field[i, j] in [1, 2, 3, 4]:
                    res += 1
                    color = field[i, j]
                    field[i, j] = 0
                    field = self.clear_group(field, color, np.array([i, j]))
        return res

    def get_block(self, i, j, f=None):
        if f is None:
            f = self.field
        return f.matrix[i, j]

    def minimax(self, f, depth, alpha, beta, is_max):
        if depth == 0:
            return self.n_groups(f)

        decission = [1, 0, 0, 0]

        colors = np.array([1, 2, 3, 4])
        possible = self.find_possible(f)

        if len(possible) < 1:
            return self.n_groups(f)

        best_eval = 1000 * ((-1) ** (1 * is_max))
        for c in colors:
            if f.color_nums[c - 1] > 0:
                for p in possible:
                    test_f = self.field_copy(f)
                    if self.add(c, p[0], p[1], p[2], test_f) != -1:
                        eval = self.minimax(test_f, depth - 1, alpha, beta, not is_max)

                        if (eval > best_eval and is_max) or (eval < best_eval and not is_max):
                            decission = [c, p[0], p[1], p[2]]
                            best_eval = eval

                        if is_max:
                            alpha = max(alpha, eval)
                        else:
                            beta = min(beta, eval)

                        if beta <= alpha:
                            if depth == self.difficulty:
                                return decission
                            return best_eval
        if depth == self.difficulty:
            return decission
        return best_eval

    def AI_step(self):
        return self.minimax(self.field_copy(self.field), self.difficulty, -1000, 1000, False)

    def field_copy(self, f):
        res = Board(self.size)
        res.color_nums = copy(f.color_nums)
        res.matrix = np.copy(f.matrix)
        return res

    def find_possible(self, f=None):
        if f is None:
            f = self.field
        matrix = f.matrix
        res = []
        for d in [0, 1]:
            for i in range(self.size):
                for j in range(self.size):
                    neib = np.array([i + self.directions[d][0], j + self.directions[d][1]])
                    if np.all(neib >= 0) and np.all(neib < 7) and matrix[i, j] == 0 and matrix[neib[0], neib[1]] == 0:
                        res.append([d, i, j])
        return np.array(res)
