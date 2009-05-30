#!/usr/bin/python
import copy

class Marble:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "M: %d,%d" % (self.x, self.y)

class Move:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "%r - %r" % (self.a, self.b)

class Board:
    blanks = [ (0, 0), (0, 1), (0, 5), (0, 6), (1, 0), (1, 6), (5, 0), (5, 6),\
        (6, 0), (6, 1), (6, 5), (6, 6)]

    def __init__(self):
        self.board = {}
        for i in range(0,7):
            self.board[i] = {}
            for j in range(0,7):
                if (i,j) in self.blanks:
                    self.board[i][j] = None
                else:
                    self.board[i][j] = Marble(i, j)

    def remove_marble(self, (x, y)):
        self.board[x][y] = 0

    def add_marble(self, (x, y)):
        self.board[x][y] = Marble(x, y)

    def has_marble(self, (x, y)):
        return self.board[x][y] is not None and self.board[x][y] != 0

    def get_marble(self, (x, y)):
        return self.board[x][y]

    def get_inbetween_move(self, (fromx, fromy), (tox, toy)):
        x = fromx
        y = fromy
        if fromx == tox:
            y = (toy + fromy)/2
        elif fromy == toy:
            x = (tox + fromx)/2
        return (x, y)

    def can_move(self, (fromx, fromy), (tox, toy)):
        if not self.has_marble((fromx, fromy)):
            return False
        if self.has_marble((tox, toy)):
            return False
        x, y = self.get_inbetween_move((fromx, fromy), (tox, toy))
        if not self.has_marble((x, y)):
            return False
        return True

    def make_move(self, move):
        fromx = move.a.x
        fromy = move.a.y
        tox = move.b.x
        toy = move.b.y
        if not self.can_move((fromx, fromy), (tox, toy)):
            return False
        x, y = self.get_inbetween_move((fromx, fromy), (tox, toy))
        self.remove_marble((fromx, fromy))
        self.remove_marble((x, y))
        self.add_marble((tox, toy))
        return True

    def get_spaces(self):
        spaces = []
        for row in range(0, 7):
            for col in range(0, 7):
                if self.board[row][col] == 0:
                    spaces.append((row, col))
        return spaces

    def get_adjacent_marbles(self, (x, y)):
        adjacent = []
        ax = x
        ay = y + 1
        if ay <= 6:
            if self.has_marble((ax, ay)):
                adjacent.append(self.get_marble((ax, ay)))
        ay = y - 1
        if ay >= 0:
            if self.has_marble((ax, ay)):
                adjacent.append(self.get_marble((ax, ay)))
        ax = x + 1
        ay = y
        if ax <= 6:
            if self.has_marble((ax, ay)):
                adjacent.append(self.get_marble((ax, ay)))
        ax = x - 1
        if ax >= 0:
            if self.has_marble((ax, ay)):
                adjacent.append(self.get_marble((ax, ay)))
        return adjacent

    def get_possible_moves(self, space):
        moves = []
        for m in self.get_adjacent_marbles(space):
            for i in self.get_adjacent_marbles((m.x, m.y)):
                if space[0] == i.x or space[1] == i.y:
                    moves.append(Move(i, Marble(space[0], space[1])))
        return moves

    def possible_moves(self):
        spaces = self.get_spaces()
        allmoves = []
        for space in spaces:
            moves = self.get_possible_moves(space)
            allmoves.extend(moves)
        return allmoves

    def get_number_marbles(self):
        total = 0
        for row in range(0, 7):
            for col in range(0, 7):
                if self.board[row][col] is not None and self.board[row][col] != 0:
                    total = total + 1
        return total

    def __repr__(self):
        str = ""
        for row in range(0, 7):
            for col in range(0, 7):
                if self.board[row][col] is None:
                    str = "%s  " % str
                elif self.board[row][col] == 0:
                    str = "%s 0" % str
                else:
                    str = "%s *" % str
            str = "%s\n" % str
        return str

lowest = 1000

def solve(board, allmoves):
    global lowest
    #print "allmoves: %r" % allmoves
    moves = board.possible_moves()
    if not moves:
        marbles = board.get_number_marbles()
        if lowest > marbles:
            lowest = marbles
            print "lowest so far %d" % marbles
        if marbles == 1:
            print "Solution: %r" % moves
        return
    for m in moves:
        b = copy.deepcopy(board)
        b.make_move(m)
        am = copy.copy(allmoves)
        am.append(m)
        solve(b, am)

board = Board()
board.remove_marble((1, 3))
lowest = board.get_number_marbles()

solve(board, [])
#print board
#print "num marbles: %d" % board.get_number_marbles()
