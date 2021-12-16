import numpy as np


class Board:
    def __init__(self, size):
        self.color_nums = [6, 6, 6, 6]
        self.matrix = np.zeros((size, size), dtype=int)
        self.matrix[int(size / 2), int(size / 2)] = 5
