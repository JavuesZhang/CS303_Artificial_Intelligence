import json
import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
DIR = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
WEIGHT1 = np.asarray([[400, -40, 10, 5, 5, 10, -40, 400],
                      [-40, -65, 1, 1, 1, 1, -65, -40],
                      [10, 1, 3, 2, 2, 3, 1, 10], [5, 1, 2, 1, 1, 2, 1, 5],
                      [5, 1, 2, 1, 1, 2, 1, 5], [10, 1, 3, 2, 2, 3, 1, 10],
                      [-40, -65, 1, 1, 1, 1, -65, -40],
                      [400, -40, 10, 5, 5, 10, -40, 400]])
MAX_INF = float("inf")
MIN_INF = float("-inf")
STATUS = {
    0: np.asarray([1, 0, 0]),
    1: np.asarray([1, 1.5, 0]),
    2: np.asarray([0.5, 0, 5000000])
}


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
        if len(self.candidate_list) > 1:
            best_val, best_move = AI.alpha_beta(chessboard, MIN_INF, MAX_INF,
                                                self.color, self.color, 4,
                                                self.status)
            self.candidate_list.append(best_move)
        self.get_status(chessboard)

    def get_status(self, chessboard):
        cnt = 0
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] != 0:
                    cnt = cnt + 1
        if cnt < 10:
            self.statuc = 0
        else:
            if cnt < 56:
                self.status = 1
            else:
                self.status = 2

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
            if status == 2:
                val += val3 * STATUS[2][2]
            if color == self_color:
                if val > alpha:
                    if val > beta:
                        return val, move
                    alpha = val
                if val > max_val:
                    max_val = val
                    best_move = move
            else:
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

        for i in range(8):
            for j in range(8):
                if chessboard[i][j] == color:
                    val1 += WEIGHT1[i][j]
                else:
                    if chessboard[i][j] == -color:
                        val1 -= WEIGHT1[i][j]

        move_list = AI.find_all_valid_move(chessboard, color)
        val2 = len(move_list)

        arr = STATUS[status]

        return val1 * arr[0] + val2 * arr[1]

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


def place(board, x, y, color):
    if x < 0:
        return False
    board[x][y] = color
    valid = False
    for d in range(8):
        i = x + DIR[d][0]
        j = y + DIR[d][1]
        while 0 <= i and i < 8 and 0 <= j and j < 8 and board[i][j] == -color:
            i += DIR[d][0]
            j += DIR[d][1]
        if 0 <= i and i < 8 and 0 <= j and j < 8 and board[i][j] == color:
            while True:
                i -= DIR[d][0]
                j -= DIR[d][1]
                if i == x and j == y:
                    break
                valid = True
                board[i][j] = color
    return valid


def initBoard():
    fullInput = json.loads(input())
    requests = fullInput["requests"]
    responses = fullInput["responses"]
    board = np.zeros((8, 8), dtype=np.int)
    board[3][4] = board[4][3] = 1
    board[3][3] = board[4][4] = -1
    ai = AI(64, 1, 5)
    ai.color = 1
    if requests[0]["x"] >= 0:
        ai.color = -1
        place(board, requests[0]["x"], requests[0]["y"], -ai.color)
    turn = len(responses)
    for i in range(turn):
        place(board, responses[i]["x"], responses[i]["y"], ai.color)
        place(board, requests[i + 1]["x"], requests[i + 1]["y"], -ai.color)
    return board, ai


board, ai = initBoard()
ai.go(board)
if ai.candidate_list != []:
    go_position = ai.candidate_list[len(ai.candidate_list) -
                                    1]  # randomly choose one, editable
    x, y = go_position
else:
    x, y = (-1, -1)
print(json.dumps({"response": {"x": int(x), "y": int(y)}}))
