import collections
import sys
import ErrorModel as EM

second_string = []
first_string = []
diagonal_mov = 'diagonal'
left_mov = '  left  '
up_mov = '   up   '
stop_mov = '  stop  '
trans_mov = ' trans '
score_file = 'matrix.txt'
gap_penalty = -1
h = 0
w = 0
value_matrix = [[]]
movement_matrix = [[]]
optimum_score = 0
max_print = 60


def read_strings(f, s):
    global first_string
    global second_string
    global h
    global w
    global value_matrix
    global movement_matrix
    first_string = f
    second_string = s
    h = len(first_string) + 1
    w = len(second_string) + 1
    value_matrix = [[0 for x in range(w)] for y in range(h)]
    movement_matrix = [['' for x in range(w)] for y in range(h)]


def print_matrix(matrix):
    global h
    global w
    for i in range(h):
        for j in range(w):
            print(matrix[i][j], end=' ')
        print()


def get_score(first_index, second_index):
    global first_string
    global second_string
    first_letter = first_string[first_index - 1]
    second_letter = second_string[second_index - 1]
    if first_letter == second_letter:
        return 0
    else:
        return -1


def align():
    global second_string
    global first_string
    global gap_penalty
    global value_matrix
    global movement_matrix
    global w
    global h
    global left_mov
    global up_mov
    global diagonal_mov
    global stop_mov
    global optimum_score
    ###
    value_matrix[0][0] = 0
    movement_matrix[0][0] = stop_mov
    for i in range(1, h):
        value_matrix[i][0] = i * gap_penalty
        movement_matrix[i][0] = up_mov
    for j in range(1, w):
        value_matrix[0][j] = j * gap_penalty
        movement_matrix[0][j] = left_mov
    for i in range(1, h):
        for j in range(1, w):
            diagonal = value_matrix[i - 1][j - 1] + get_score(i, j)
            up = value_matrix[i - 1][j] + gap_penalty
            left = value_matrix[i][j - 1] + gap_penalty
            if i-1 and j-1 and first_string[i-1]==second_string[j-2] and first_string[i-2] == second_string[j-1]:
                transpose = value_matrix[i-2][j-2] - 1
            else:
                transpose = -100000000;
            choices = [left, up, diagonal,transpose]
            maximum = max(choices)
            index = choices.index(maximum)
            if index == 3:
                movement_matrix[i][j] = trans_mov
                value_matrix[i][j] = transpose
            elif index == 2:
                value_matrix[i][j] = diagonal
                movement_matrix[i][j] = diagonal_mov
            elif index == 1:
                value_matrix[i][j] = up
                movement_matrix[i][j] = up_mov
            elif index == 0:
                value_matrix[i][j] = left
                movement_matrix[i][j] = left_mov
    optimum_score = value_matrix[h-1][w-1]


def traceback():
    global first_string
    global second_string
    global movement_matrix
    global w
    global h
    global stop_mov
    global left_mov
    global diagonal_mov
    global up_mov
    current = movement_matrix[h - 1][w - 1]
    i = h - 1
    j = w - 1
    movement_list = []
    while current is not stop_mov:
        if current == diagonal_mov:
            i -= 1
            j -= 1
        elif current == up_mov:
            i -= 1
        elif current == left_mov:
            j -= 1
        else:
            i -= 2
            j -= 2
        movement_list.append(current)
        current = movement_matrix[i][j]
    movement_list.reverse()
    first_aligned = []
    second_aligned = []
    i = 0
    j = 0
    for mov in movement_list:
        if mov == diagonal_mov:
            first_aligned.append(first_string[i])
            second_aligned.append(second_string[j])
            EM.sub_confusion_matrix[first_string[i]][second_string[j]] += 1
            i += 1
            j += 1
        elif mov == left_mov:
            first_aligned.append('-')
            second_aligned.append(second_string[j])
            if i:
                EM.ins_confusion_matrix[first_string[i-1]][second_string[j]] += 1
            else:
                EM.ins_confusion_matrix[' '][second_string[j]] += 1
            j += 1
        elif mov == up_mov:
            first_aligned.append(first_string[i])
            second_aligned.append('-')
            if i:
                EM.del_confusion_matrix[first_string[i-1]][first_string[i]] += 1
            else:
                EM.del_confusion_matrix[' '][first_string[i]] += 1
            i += 1

        elif mov == trans_mov:
            first_aligned.append(first_string[i])
            second_aligned.append(first_string[i])
            first_aligned.append(first_string[i+1])
            second_aligned.append(first_string[i+1])
            EM.trans_confusion_matrix[first_string[i]][first_string[i+1]] += 1
            i += 2
            j += 2

    return [first_aligned,second_aligned]


def separate(value):
    for i in range(value):
        print('=',end='')
    print()


def print_result(align_result):
    global optimum_score
    global max_print
    print('OPTIMUM SCORE = ', optimum_score)
    alignment = []
    length = len(align_result[0])
    print(align_result[0])
    print(align_result[1])
    for i in range(length):
        if align_result[0][i] == align_result[1][i]:
            alignment.append('|')
        elif align_result[0][i] == '-':
            alignment.append(' ')
        elif align_result[1][i] == '-':
            alignment.append(' ')
        else:
            if 0 < 1 :
                alignment.append(':')
            else:
                alignment.append('.')
    separation = 0
    for x in range(int(length / max_print) + 1):
        j = x * max_print
        k = x * max_print + max_print
        if k >= length:
            k = length
        separation = k-j
        separate(2*separation)
        for i in range(j, k):
            print(align_result[0][i], end=' ')
        print()
        for i in range(j, k):
            print(alignment[i], end=' ')
        print()
        for i in range(j, k):
            print(align_result[1][i], end=' ')
        print()
        if k == length:
            break
    separate(2*separation)


def update_confusion_matrix(f,s):
    read_strings(f,s)
    align()
    traceback()
