#!/usr/bin/env python2.7
# coding: utf-8
#
# An AI that solves a tile game.
#
# CAUTION:  The spacing in here is just that: spacing.
# don't use tabs if editing this, please.

import time
import math
import sys
import os
import signal
import copy
from heapq import *
from os import listdir, system
from random import choice

class Board():
    '''
    Represents a shuffleable board.  Upon initialization, the board
    becomes shuffled based on a constant field.
    Within the board there are several squares.  Each of them
    initially labeled 1 through N^2, and the tile labeled zero is the one
    that is blank.

    The board can be printed as well, but this requires UTF-8 in order to
    function properly.
    '''

    def __init__(s, size):
        s.size = size

        s.board = [[(1 + x + y * s.size) % s.size**2 \
                for x in range(s.size)]\
                for y in range(s.size)]

        s.position = (s.size - 1, s.size - 1)
        s.board_goal = copy.deepcopy(s.board) # Victory state.
        s.shuffle(1000 * s.size ** 2)

    def set_tiles(s, tiles):
        s.board = tiles
        s.position = s.find_tile(0)

    def shuffle(s, count=1, no_redundant=False):
        for x in range(count):
            move = choice([0, 1, 2, 3])
            if move == 0:
                s.move_up()
            elif move == 1:
                s.move_down()
            elif move == 2:
                s.move_left()
            else: # 3  
                s.move_right()

    def on_right_edge(s):
        '''
        Determines if we're on the right
        edge of the board.
        '''
        return s.position[1] ==  s.size - 1
    
    def on_left_edge(s):
        '''
        Determines if we're on the left edge
        of the board.
        '''
        return s.position[1] == 0
    
    def on_top_edge(s):
        '''
        Determines if we're on the top edge
        of the board.
        '''
        return s.position[0] == 0

    def on_bottom_edge(s):
        '''
        Determines if we're on the bottom
        edge of the board.
        '''
        return s.position[0] == s.size - 1

    def move_up(s):
        if not s.on_top_edge():
            s._switch_tiles(s.position[0], s.position[1], \
                            s.position[0] - 1, s.position[1])

    def move_down(s):
        if not s.on_bottom_edge():
            s._switch_tiles(s.position[0], s.position[1], \
                            s.position[0] + 1, s.position[1])

    def move_left(s):
        if not s.on_left_edge():
            s._switch_tiles(s.position[0], s.position[1], \
                            s.position[0], s.position[1] - 1)
    def move_right(s):
        if not s.on_right_edge():
            s._switch_tiles(s.position[0], s.position[1], \
                            s.position[0], s.position[1] + 1)

    def _switch_tiles(s, r, c, r_prime, c_prime):
        temp = s.board[r][c]
        s.board[r][c] = s.board[r_prime][c_prime]
        s.board[r_prime][c_prime] = temp
        s.position = (r_prime, c_prime)

    def is_solved(s):
        return s.board == s.board_goal

    def manhattan(s):
        '''
        Gets the manhattan distance of all tiles (except for the
        player tile on the board's position) and returns the
        value.
        '''
        total_distance = 0
        for tile in range(1, s.size**2):
            location = s.find_tile(tile)
            destination = ((tile - 1) / s.size, (tile - 1) % s.size)
            distance = abs(location[0] - destination[0]) + abs(location[1] - destination[1])
            total_distance += distance
        return total_distance

    def find_tile(s, n):
        for row in range(s.size):
            for column in range(s.size):
                if s.board[row][column] == n:
                    return (row, column)

    def _print(s):
        # Get the number of digits for the longest number.
        max_num = s.size**2 - 1
        digits = len(str(max_num))

        # The line_str string gets the max digit length
        # and puts a padding of two on either end.
        line_str = "─" * (digits + 4)
        top_str = "┌" + ((line_str + "┬") * \
                        (s.size - 1)) + line_str + "┐"
        row_str = "├" + ((line_str + "┼") * \
                        (s.size - 1)) + line_str + "┤"
        bottom_str = "└" + ((line_str + "┴") * \
                            (s.size - 1)) + line_str + "┘"

        print top_str
        print row_str
        for row in s.board:
            
            for x in range(digits / 2):
                print '│' + (((' ' * (digits + 4)) + '│') * len(row))
            
            for c in row:
                c_str = str(c)
                c_padding = ' ' * (digits - len(c_str))
                if c_str == '0':
                    c_str = ' '
                print '│ ', c_str, c_padding,
            print '│'

            for x in range(digits / 2):
                print '│' + (((' ' * (digits + 4)) + '│') * len(row))

            print row_str
        print bottom_str

class _AISolverBase:

    '''
    Determines the move we took.
    '''
    RIGHT = 'R'
    LEFT = 'L'
    UP = 'U'
    DOWN = 'D'

    def __init__(s, board):
            '''
            Determines the last move made.
            '''
            s._last_move = ''     
            
            '''
            A heap containing tuples of
            the last evaluated heuristic
            as well as the state of the board.
            '''
            s._frontier = []

            '''
            Determines the moves we've taken to get to
            a solution.
            '''
            s._move_list = []
            s.board = copy.deepcopy(board)
            s.board_initial = copy.deepcopy(board)
            s.depth = 0
            s.total_expanded_nodes = 0
            s._expand_moves()
            print "INITIAL"
            s.board._print()

    def solve(s):
        '''
        Solves the board and queues up the moves.
        '''
        pass

    def _expand_moves(s):
        '''
        Expands the moves from the current game tree
        node.
        '''
        pass

    def _move(s, dir):
        '''
        Moves in the specified direction.
        '''
        if dir == s.UP:
            s.board.move_up()
        elif dir == s.DOWN:
            s.board.move_down()
        elif dir == s.LEFT:
            s.board.move_left()
        elif dir == s.RIGHT: # Right
            s.board.move_right()
        else:
            return False
        return True

    def _play(s):
        '''
        Plays through the moves that got to the solution.
        '''
        pass

class MoveTree:
    '''
    A tree of game moves.
    '''

    def __init__(s, parent=None, depth=0):
        s.left = None
        s.right = None
        s.up = None
        s.down = None
        s.parent = parent
        s.depth = depth

    def get_common_parent(s, node, move_stack=[]):
        '''
        Finds the common parent between this and
        another node and returns a reference to
        that node. If the move stack is passed, then
        the moves taken will be returned so that going
        from the common parent to the other node will
        be easy
        '''

        this_depth  = s.depth
        other_depth = node.depth

        s_ref = s
        diff = abs(this_depth - other_depth)

        if this_depth > other_depth:
            for x in range(diff):
                s_ref = s_ref.parent
        elif this_depth < other_depth:
            for x in range(diff):
                move_stack.append(node)
                node = node.parent
        '''
        Here we assume the nodes are of
        equal depth, at which point we return
        the objects once their references are
        equal.  Until then we climb to the root
        of the tree.
        '''
        while (s_ref != node):
            s_ref = s_ref.parent
            move_stack.append(node)
            node = node.parent

        return node

class AISolver1(_AISolverBase):

    def solve(s):
        while True:
            tuple_ = heappop(s._frontier)

            #  Restore this node's state.
            s.depth = tuple_[1]
            s._last_move = tuple_[2]
            s.board.set_tiles(tuple_[3])
            s._move_list = (tuple_[4])
            s._move_list.append(s._last_move)

            '''
            If the heuristic minus the number
            of moves deep in the tree is zero,
            then we've found a solution!
            (Only should work with A*)
            '''
            if tuple_[0] - s.depth == 0:
                print "Yay!", s.depth, s._move_list
                s.depth = 0
                s._play()
                exit(0)

            s._expand_moves()


    def _expand_moves(s):
        '''
        Prioritizes the next few moves.
        '''
        b = s.board
        s.depth += 1
        s.total_expanded_nodes += 1

        '''
        Only store a position if it's not going to undo something
        we've already done, or if we're on the edge of the board.
        '''
        if (not b.on_right_edge() and s._last_move != s.LEFT):
            s._move_and_queue(s.RIGHT)
                
        if (not b.on_top_edge() and s._last_move != s.DOWN):
            s._move_and_queue(s.UP)
            
        if (not b.on_left_edge() and s._last_move != s.RIGHT):
            s._move_and_queue(s.LEFT)

        if (not b.on_bottom_edge() and s._last_move != s.UP):
            s._move_and_queue(s.DOWN)

    def _move_and_queue(s, dir):
        '''
        Moves to board to a new state.
        This is done by copying the state of the
        board and then moving that board to the state
        in question.  This state is then evaluated
        and placed on the frontier.
        '''
        new_state = [row[:] for row in s.board.board]
        prev_state = s.board.board
        s.board.set_tiles(new_state)

        # Don't queue anything that isn't a valid move.
        if (not s._move(dir)):
            return

        heuristic = s.depth + s.board.manhattan()
        if s.total_expanded_nodes % 1000 == 0:
            print "NODES:", s.total_expanded_nodes, "DEPTH:", s.depth, "MANHA:", s.board.manhattan(), "MOVE:", dir
        heappush(s._frontier, (heuristic, s.depth, dir, new_state, s._move_list[:]))
        s.board.set_tiles(prev_state)
    
    def _play(s):
        s.board = s.board_initial
        while True:
            _clear()
            s.board._print()
            print s.depth

            if s._move_list.__len__() < 1:
                break
            
            move = s._move_list.pop(0)
            raw_input("Press [Enter] To Continue")

            if not s._move(move):
                print "Unrecognized move!"
                break

            s.depth += 1

        print "Done!"

class AISolver2(_AISolverBase):

    def __init__(s):

        # Make move tree first so call to _expand_moves
        # functions the way it should.
        s._move_tree = MoveTree()
        _AISolverBase.__init__(s)

    def solve(s):
        pass

def _clear():
    ''' Clears the screen '''
    if (os.name == 'nt'):
        system('cls')
    else:
        system('clear')

def _main():
    print "Creating board. . ."

    size = 3
    if sys.argv.__len__() > 1:
        size = int(sys.argv[1])
        if size < 3:
            size = 3


    b = Board(size)
    _clear()
    cpu = AISolver1(b)
    cpu.solve()

if __name__ == '__main__':
   _main() 
