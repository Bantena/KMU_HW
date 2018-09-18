class GaussElimination:
    def __init__(self, matrix):
        self.matrix = matrix
        self.row, self.col = 0, 0
        self.row_length, self.col_length = len(matrix), len(matrix[0])

    def fowardEliminate(self):
        while self.row < self.row_length or self.col < (self.col_length - 1):
            # check pivot not 0
            pivot = self.matrix[self.row][self.col]

            if pivot == 0:
                toggle = True

                for idx in range(self.row + 1, self.row_length):
                    if self.matrix[idx][self.col] != 0:
                        self.interchangeMatrix(idx, self.row)
                        toggle = False
                        break

                if toggle:
                    self.col += 1
                    continue

            # setting pivot
            pivot = self.matrix[self.row][self.col]

            # make leading 1
            self.scaleMatrix(pivot, self.row)

            # make 0 element
            for idx in range(self.row + 1, self.row_length):
                if self.matrix[idx][self.col] != 0:
                    self.replaceMatrix(self.matrix[idx][self.col], self.row, idx)

            self.row += 1
            self.col += 1

    def backEliminate(self):
        self.row, self.col = 0, 0

        while self.row < self.row_length or self.col < self.col_length - 1:
            # check pivot not 0
            if self.matrix[self.row][self.col] != 1:
                self.col += 1
                continue

            # setting pivot
            pivot = self.matrix[self.row][self.col]

            # make 0 element
            for idx in range(self.row - 1, -1, -1):
                if self.matrix[idx][self.col] != 0:
                    self.replaceMatrix(self.matrix[idx][self.col], self.row, idx)

            self.row += 1
            self.col += 1

    def interchangeMatrix(self, row1, row2):
        self.matrix[row1], self.matrix[row2] = self.matrix[row2], self.matrix[row1]

    def scaleMatrix(self, coefficient, row):
        for col in range(self.col_length):
            self.matrix[row][col] /= coefficient

    def replaceMatrix(self, coefficient, pivot_row, target_row):
        for col in range(self.col_length):
            self.matrix[target_row][col] = -1 * coefficient * self.matrix[pivot_row][col] + self.matrix[target_row][col]