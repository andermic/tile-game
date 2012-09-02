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

    def move_up(s):
        if s.position[0] > 0:
            s._switch_tiles(s.position[0], s.position[1], \
                            s.position[0] - 1, s.position[1])

    def move_down(s):
        if s.position[0] < s.size - 1:
            s._switch_tiles(s.position[0], s.position[1], \
                            s.position[0] + 1, s.position[1])

    def move_left(s):
        if s.position[1] > 0:
            s._switch_tiles(s.position[0], s.position[1], \
                            s.position[0], s.position[1] - 1)
    def move_right(s):
        if s.position[1] < s.size - 1:
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

class AISolver():


    '''
    A heap containing tuples of
    the last evaluated heuristic
    as well as the state of the board.
    '''
    _frontier = []

    '''
    Determines the moves we've taken to get to
    a solution.
    '''
    _move_list = []

    '''
    Determines the move we took.
    '''
    RIGHT = 'R'
    LEFT = 'L'
    UP = 'U'
    DOWN = 'D'

    '''
    Determines the last move made.
    '''
    _last_move = ''

    def __init__(s, board):
        s.board = copy.deepcopy(board)
        s.depth = 0
        s.total_moves = 0
        s._queue_position(s.UP)

    def solve(s):
        while True:
            tuple_ = heappop(s._frontier)

            #  Restore this node's state.
            s._restore_board(tuple_[1])
            s.depth = tuple_[1]

            if s.depth > 0:
                s._move_list.append(tuple_[2])
                s._move(tuple_[2])

            if s.total_moves > -1:
                s.board._print()
                print "Loops:", s.total_moves, \
                        "Depth:", s.depth, \
                        "Man:", s.board.manhattan(), \
                        "Heur:", tuple_[0], \
                        "Moves:", s._move_list 

            '''
            If the heuristic minus the number
            of moves deep in the tree is zero,
            then we've found a solution!
            (Only should work with A*)
            '''
            if tuple_[0] - s.depth == 0:
                print "Yay!"
                s.board._print()
                print s._move_list
                exit(0)

            '''
            Sleep for debugging (heuristic evaluation still
            seems to really suck).
            '''
            #time.sleep(5)
            s._expand_moves()


    def _expand_moves(s):
        '''
        Prioritizes the next few moves.
        '''
        b = s.board
        s.depth += 1
        s.total_moves += 1

        if s._move_list.__len__() > 0:
            last_move = s._move_list[-1]
        else:
            last_move = ''

        # TODO: This is a little silly.  There's
        # probably a better way to do this.
        if (b.position[1] < b.size - 1 and last_move != s.LEFT):
            s.board.move_right()
            s._queue_position(s.RIGHT)
            s.board.move_left()
                
        if (b.position[0] > 0 and last_move != s.DOWN):
            s.board.move_up()
            s._queue_position(s.UP)
            s.board.move_down()
            
        if (b.position[1] > 0 and last_move != s.RIGHT):
            s.board.move_left()
            s._queue_position(s.LEFT)
            s.board.move_right()

        if (b.position[0] < b.size - 1 and last_move != s.UP):
            s.board.move_down()
            s._queue_position(s.DOWN)
            #s.board.move_up() # Only doing this so we can print the board.

        # TODO: Get rid of duplicate positions in the
        # heap.  Also make sure to queue up on the moves
        # we've made when going back through the loop!

    def _queue_position(s, move):
        '''
        Puts the current position, having been evaulated by
        the heuristic, onto the frontier.
        '''
        heuristic = s.depth + s.board.manhattan()
        print s._move_list
        print move, s.depth, heuristic
        heappush(s._frontier, (heuristic, s.depth, move))

    def _restore_board(s, moves):
        if moves < s.depth:
            print "REVERSING:", s._move_list
            print "TO:", moves, "moves"
            for x in range(s._move_list.__len__() - moves):
                s._reverse_move(s._move_list.pop())

    def _move(s, dir):
        if dir == s.UP:
            s.board.move_up()
        elif dir == s.DOWN:
            s.board.move_down()
        elif dir == s.LEFT:
            s.board.move_left()
        else: # Right
            s.board.move_right()

    def _reverse_move(s, dir):
        if dir == s.UP:
            s.board.move_down()
        elif dir == s.DOWN:
            s.board.move_up()
        elif dir == s.LEFT:
            s.board.move_right()
        else: # RIGHT
            s.board.move_left()
        
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
    cpu = AISolver(b)
    cpu.solve()

if __name__ == '__main__':
   _main() 
