import numpy as np

chessboard = np.array([[0, 1, -1, -1, -1, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, -1, -1, -1, 1, 0, 0]])

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


def draw(board):
    print('\\begin{figure}[hbt]\n\\centering\n\\begin{tikzpicture}[scale = .8]\n\\draw (0,0) grid (8,8);')
    black = np.where(board == COLOR_BLACK)
    black_point = list(zip(black[0], black[1]))
    for idx in black_point:
        print(f'\\shade[ball, ball color=black] ({idx[1] + 0.5} , {7 - idx[0] + 0.5}) circle (0.45cm);')
    white = np.where(board == COLOR_WHITE)
    white_point = list(zip(white[0], white[1]))
    for idx in white_point:
        print(f'\\shade[ball, ball color=white] ({idx[1] + 0.5} , {7 - idx[0] + 0.5}) circle (0.45cm);')
    print('\\end{tikzpicture}  \n\\caption{pic name}  \n\\label{fig:xxx}\n\\end{figure}')


if __name__ == '__main__':
    draw(chessboard)
