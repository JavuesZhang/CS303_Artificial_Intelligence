import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
DIR = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
WEIGHT1 = np.asarray([[1000, -200, 60, 40, 40, 60, -200, 1000],
                      [-200, -500, -5, -5, -5, -5, -500, -200],
                      [60, -5, 3, 2, 2, 3, -5,
                       60], [40, -5, 2, 1, 1, 2, -5, 40],
                      [40, -5, 2, 1, 1, 2, -5, 40],
                      [60, -5, 3, 2, 2, 3, -5, 60],
                      [-200, -500, -5, -5, -5, -5, -500, -200],
                      [1000, -200, 60, 40, 40, 60, -200, 1000]])
WEIGHT2 = np.ones([8, 8], dtype=int)
MAX_INF = float("inf")
MIN_INF = float("-inf")
# table, active, stable, eat
STATUS = {
    0: np.asarray([1, 50, 500, -20]),
    1: np.asarray([1, 150, 400, -10]),
    2: np.asarray([1, 100, 300, -5]),
    3: np.asarray([1, 80, 250, 0]),
    4: np.asarray([0.5, 50, 150, 50]),
    5: np.asarray([0, 50, 100, 200])
}
DEPTH = np.asarray([4, 3, 3, 3, 5, 9])


class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        self.status = 0

    def go(self, chessboard):
        self.candidate_list.clear()
        self.candidate_list = AI.find_all_valid_move(chessboard, self.color)
        self.get_status(chessboard)
        if len(self.candidate_list) > 1:
            best_val, best_move = AI.alpha_beta(chessboard, -99999999,
                                                99999999, self.color,
                                                self.color, 2, self.status)
            self.candidate_list.append(best_move)
            best_val, best_move = AI.alpha_beta(chessboard, -99999999,
                                                99999999, self.color,
                                                self.color, 3, self.status)
            self.candidate_list.append(best_move)
            best_val, best_move = AI.alpha_beta(chessboard, -99999999,
                                                99999999, self.color,
                                                self.color, 4, self.status)
            self.candidate_list.append(best_move)

    def get_status(self, chessboard):
        cnt = 0
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] != 0:
                    cnt = cnt + 1
        cnt -= 3
        if cnt < 15:
            self.statuc = 0
        else:
            if cnt < 30:
                self.status = 1
            else:
                if cnt < 40:
                    self.status = 2
                else:
                    if cnt < 50:
                        self.status = 3
                    else:
                        if cnt < 60:
                            self.status = 4
                        else:
                            self.status = 5

    def valid_pos(chessboard, pos, direction, color):
        x = pos[0] + direction[0]
        y = pos[1] + direction[1]
        return x >= 0 and x <= 7 and y >= 0 and y <= 7 and chessboard[x][
            y] == color

    def go_direction(pos, direction):
        x = pos[0] + direction[0]
        y = pos[1] + direction[1]
        return (x, y)

    def find_all_valid_move(chessboard, color):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        move_list = []

        antiColor = -color
        for point in idx:
            for direction in DIR:
                if AI.valid_pos(chessboard, point, direction, antiColor):
                    temp_point = point
                    while AI.valid_pos(chessboard, temp_point, direction,
                                       antiColor):
                        temp_point = AI.go_direction(temp_point, direction)
                    if AI.valid_pos(chessboard, temp_point, direction, color):
                        move_list.append(point)
        move_list = list(set(move_list))
        return move_list

    def alpha_beta(chessboard, alpha, beta, self_color, color, depth, status):
        if depth <= 0:
            return AI.evaluate(chessboard, self_color, status), ()

        move_list = AI.find_all_valid_move(chessboard, color)
        if move_list == []:
            if AI.find_all_valid_move(chessboard, -color) == []:
                return AI.evaluate(chessboard, self_color, status), ()
            val, move_tmp = AI.alpha_beta(chessboard, alpha, beta, self_color,
                                          -color, depth, status)
            return val, move_tmp

        max_val = MIN_INF
        min_val = MAX_INF
        best_move = ()
        for move in move_list:
            board, val3 = AI.make_move(chessboard, move, color)
            val, move_tmp = AI.alpha_beta(board, alpha, beta, self_color,
                                          -color, depth - 1, status)
            val += val3 * STATUS[status][3]
            if color == self_color:
                if val > alpha:
                    if val > beta:
                        return val, move
                    alpha = val
                if val > max_val:
                    max_val = val
                    best_move = move
            else:
                # val = -val
                if val < beta:
                    if val < alpha:
                        return val, move
                    beta = val
                if val < min_val:
                    min_val = val
                    best_move = move

        if color == self_color:
            return max_val, best_move
        else:
            return min_val, best_move

    def evaluate(chessboard, color, status):
        val1 = 0
        val2 = 0
        val3 = 0
        weight = WEIGHT1
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] == color:
                    # if not (ptl == color and (
                    #     (i == 0 and j == 1) or
                    #     (i == 1 and j == 0))) and not (ptr == color and (
                    #         (i == 0 and j == 6) or
                    #         (i == 1 and j == 7))) and not (pbl == color and (
                    #             (i == 7 and j == 1) or
                    #             (i == 6 and j == 0))) and not (
                    #                 pbr == color and ((i == 7 and j == 6) or
                    #                                     (i == 6 and j == 7))):
                    #     val1 += weight[i][j]
                    val1 += weight[i][j]
                else:
                    if chessboard[i][j] == -color:
                        val1 -= weight[i][j]
        move_list = AI.find_all_valid_move(chessboard, color)
        val2 = len(move_list)
        move_list = AI.find_all_valid_move(chessboard, -color)
        val2 -= len(move_list)
        val3 = AI.stable(chessboard, color)
        val3 -= AI.stable(chessboard, -color)
        arr = STATUS[status]

        return val1 * arr[0] + val2 * arr[1] + val3 * arr[2]

    def stable(chessboard, color):
        ptl = chessboard[0][0]
        pbl = chessboard[7][0]
        ptr = chessboard[0][7]
        pbr = chessboard[7][7]
        isFound = np.zeros([8, 8], dtype=int)

        corner = 5
        edge = 1
        num = 0
        max_len = 8
        if ptl == color:
            for i in range(8):
                if chessboard[i][0] == color:
                    j = 0
                    while j < max_len and chessboard[i][j] == color:
                        if not isFound[i][j]:
                            num += corner
                            isFound[i][j] = 1
                        j += 1
                    max_len = j
        max_len = 8
        if pbl == color:
            for i in range(8):
                if chessboard[7 - i][0] == color:
                    j = 0
                    while j < max_len and chessboard[7 - i][j] == color:
                        if not isFound[7 - i][j]:
                            num += corner
                            isFound[7 - i][j] = 1
                        j += 1
                    max_len = j
        max_len = 8
        if ptr == color:
            for i in range(8):
                if chessboard[i][7] == color:
                    j = 0
                    while j < max_len and chessboard[i][7 - j] == color:
                        if not isFound[i][7 - j]:
                            num += corner
                            isFound[i][7 - j] = 1
                        j += 1
                    max_len = j
        max_len = 8
        if pbr == color:
            for i in range(8):
                if chessboard[7 - i][7] == color:
                    j = 0
                    while j < max_len and chessboard[7 - i][7 - j] == color:
                        if not isFound[7 - i][7 - j]:
                            num += corner
                            isFound[7 - i][7 - j] = 1
                        j += 1
                    max_len = j

        stt = 0
        stt_num = 0
        for i in range(8):
            thisColor = chessboard[i][0]
            found = isFound[i][0]
            if thisColor == color and stt > -1:
                stt += 1
                if not found:
                    stt_num += 1
                    isFound[i][0] = 1
                continue
            if thisColor == -color:
                if stt > 0:
                    num += stt_num
                stt = 0
                stt_num = 0
            if thisColor == 0:
                stt = -1
                stt_num = -1
        stt = 0
        stt_num = 0
        for i in range(8):
            thisColor = chessboard[i][7]
            found = isFound[i][7]
            if thisColor == color and stt > -1:
                stt += 1
                if not found:
                    stt_num += 1
                    isFound[i][7] = 1
                continue
            if thisColor == -color:
                if stt > 0:
                    num += stt_num
                stt = 0
                stt_num = 0
            if thisColor == 0:
                stt = -1
                stt_num = -1
        stt = 0
        stt_num = 0
        for i in range(8):
            thisColor = chessboard[0][i]
            found = isFound[0][i]
            if thisColor == color and stt > -1:
                stt += 1
                if not found:
                    stt_num += 1
                    isFound[0][i] = 1
                continue
            if thisColor == -color:
                if stt > 0:
                    num += stt_num
                stt = 0
                stt_num = 0
            if thisColor == 0:
                stt = -1
                stt_num = -1
        stt = 0
        stt_num = 0
        for i in range(8):
            thisColor = chessboard[7][i]
            found = isFound[7][i]
            if thisColor == color and stt > -1:
                stt += 1
                if not found:
                    stt_num += 1
                    isFound[7][i] = 1
                continue
            if thisColor == -color:
                if stt > 0:
                    num += stt_num
                stt = 0
                stt_num = 0
            if thisColor == 0:
                stt = -1
                stt_num = -1
        return num

    def make_move(chessboard, move, my_color):
        board = np.array(chessboard)
        x, y = move
        val = 0
        board[x][y] = my_color
        for d in range(8):
            i = x + DIR[d][0]
            j = y + DIR[d][1]
            while 0 <= i and i < 8 and 0 <= j and j < 8 and board[i][
                    j] == -my_color:
                i += DIR[d][0]
                j += DIR[d][1]
            if 0 <= i and i < 8 and 0 <= j and j < 8 and board[i][
                    j] == my_color:
                while True:
                    i -= DIR[d][0]
                    j -= DIR[d][1]
                    if i == x and j == y:
                        break
                    board[i][j] = my_color
                    val += 1
        return board, val
