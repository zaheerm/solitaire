#!/usr/bin/python
import copy

class BoardPosition:
    def __init__(self, x, y, covered):
        self.x = x
        self.y = y
        self.covered = covered
        self.left = None
        self.right = None
        self.up = None
        self.down = None

    def __repr__(self):
        covered = "o"
        if self.covered:
            covered = "*"
        return "%s: (%d, %d)" % (covered, self.x, self.y)

class AbstractBoard:
    positions = [] # array of all board positions
    spaces = [] # array of spaces
    indexed_positions = {} # positions indexed by (x,y)
    height = 0
    width = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def remove_marble(self, (x, y)):
        pos = self.indexed_positions.get((x,y))
        self.remove_marble_pos(pos)

    def remove_marble_pos(self, pos):
        if pos and pos.covered:
            self.spaces.append(pos)
            pos.covered = False

    def add_marble(self, (x, y)):
        pos = self.indexed_positions.get((x,y))
        self.add_marble_pos(pos)

    def add_marble_pos(self, pos):
        if pos and not pos.covered:
            self.spaces.remove(pos)
            pos.covered = True

    def has_marble(self, (x, y)):
        pos = self.indexed_positions.get((x,y))
        if pos:
            return pos.covered
        return False

    def get_number_marbles(self):
        return len(self.positions) - len(self.spaces)

    def possible_moves(self):
        moves = []
        for s in self.spaces:
            if s.left and s.left.covered and s.left.left and \
                s.left.left.covered:
                moves.append((s.left.left, s.left, s))
            if s.right and s.right.covered and s.right.right and \
                s.right.right.covered:
                moves.append((s.right.right, s.right, s))
            if s.up and s.up.covered and s.up.up and s.up.up.covered:
                moves.append((s.up.up, s.up, s))
            if s.down and s.down.covered and s.down.down and \
                s.down.down.covered:
                moves.append((s.down.down, s.down, s))
        return moves

    def make_move(self, (marble1, marble2, space)):
        if marble1.covered and marble2.covered and not space.covered:
            self.remove_marble_pos(marble1)
            self.remove_marble_pos(marble2)
            self.add_marble_pos(space)

    def undo_move(self, (marble1, marble2, space)):
        if not marble1.covered and not marble2.covered and space.covered:
            self.remove_marble_pos(space)
            self.add_marble_pos(marble1)
            self.add_marble_pos(marble2)

    def __repr__(self):
        str = ""
        for y in range(0, self.height):
            row = ""
            for x in range(0, self.width):
                pos = self.indexed_positions.get((x,y), None)
                if pos is None:
                    row = "%s  " % row
                else:
                    if pos.covered:
                        row = "%s *" % row
                    else:
                        row = "%s o" % row
            str = "%s%s\n" % (str, row)
        return str

class RectangleSolitaire(AbstractBoard):
    def __init__(self, width, height):
        AbstractBoard.__init__(self, width, height)
        for x in range(0, width):
            for y in range(0, height):
                pos = BoardPosition(x, y, True)
                self.positions.append(pos)
                self.indexed_positions[(x,y)] = pos
        # put in left, right, up, down associations
        for x in range(0, width):
            for y in range(0, height):
                pos = self.indexed_positions[(x, y)]
                if x > 0:
                    pos.left = self.indexed_positions[(x - 1, y)]
                if x < width - 1:
                    pos.right = self.indexed_positions[(x + 1, y)]
                if y > 0:
                    pos.up = self.indexed_positions[(x, y - 1)]
                if y < height - 1:
                    pos.down = self.indexed_positions[(x, y + 1)]

class EuropeanSolitaire(AbstractBoard):
    def __init__(self):
        AbstractBoard.__init__(self, 7, 7)
        for x in range(0, self.width):
            for y in range(0, self.height):
                if (y > 1 and y < 5) or (x > 1 and x < 5) or \
                    ((y == 1 or y == 5) and (x > 0 and x < 6)) or \
                    ((x == 1 or x == 5) and (y > 0 and y < 6)):
                    pos = BoardPosition(x, y, True)
                    self.positions.append(pos)
                    self.indexed_positions[(x,y)] = pos
        # put in left, right, up, down associations
        for x in range(0, self.width):
            for y in range(0, self.height):
                pos = self.indexed_positions.get((x, y))
                if pos:
                    pos.left = self.indexed_positions.get((x - 1, y), None)
                    pos.right = self.indexed_positions.get((x + 1, y), None)
                    pos.up = self.indexed_positions.get((x, y - 1), None)
                    pos.down = self.indexed_positions.get((x, y + 1), None)

def solve(board):
    #print "allmoves: %r" % allmoves
    allmoves = []
    completed_moves = {} # completed moves at depth level level -> [move]
    lowest = len(board.positions)
    last_move = None
    level = 0
    while True:
        moves = board.possible_moves()
        print "moves made so far: %d possible moves: %d level: %d" % (len(allmoves), len(moves), level)
        m = None
        while moves:
            m = moves.pop()
            if level in completed_moves:
                there = False
                for c in completed_moves[level]:
                    if c == m:
                        #print "move %r is already made" % (m,)
                        there = True
                        break
                if there:
                    m = None
                    continue
            break
        #print "move to attempt: %r" % (m,)
        if not m:
            marbles = board.get_number_marbles()
            print "finished with %d left" % marbles
            if lowest > marbles:
                lowest = marbles
                print "lowest so far %d" % marbles
            if marbles == 1:
                print "Solution: %r" % allmoves
                print board
                break
            #print "Undoing move: %r" % (last_move,)
            # undo last move for this dfs
            board.undo_move(last_move)
            if level in completed_moves:
                print "Removing moves made in level %d" % (level,)
                del completed_moves[level]
            level = level - 1
            if len(allmoves) == 0:
                break
            allmoves.pop()
            if len(allmoves) == 0:
                last_move = None
            else:
                last_move = allmoves[-1]
        else:
            #print "Considering move %r with completed moves: %r" % (m,completed_moves.get(level, None))
            board.make_move(m)
            allmoves.append(m)
            last_move = m
            if level in completed_moves:
                completed_moves[level].append(m)
            else:
                completed_moves[level] = [m]
            level = level + 1

#board = Board()
#board.remove_marble((1, 3))
#lowest = board.get_number_marbles()

sboard = EuropeanSolitaire()
sboard.remove_marble((3, 1))
print sboard.has_marble((3, 1))
print sboard.has_marble((1, 3))
print sboard
#print board.possible_moves()
#print board.get_number_marbles()
solve(sboard)
