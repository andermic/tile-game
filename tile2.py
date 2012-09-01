#!/usr/bin/env python2.7
# coding: utf-8
#
# An AI that solves a tile game.
#
# CAUTION:  The spacing in here is just that: spacing.
# don't use tabs if editing this, please.

import time
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
    becomes shuffled based on a constant feild.
    Within the board there are several squares.  Each of them
    initially labeled 1-N^2, and the tile labeled zero is the one
    that is blank.
    '''

    _shuffleCount = 100

    def __init__(s, size):
        s.size = size

        s.board = [[(1 + x + y * s.size) % s.size**2 \
                for x in range(s.size)]\
                for y in range(s.size)]

        s._pos = (s.size - 1, s.size - 1)
        s.board_goal = copy.deepcopy(s.board) # Victory state.
        s._shuffleCount *= s.size**2
        s.shuffle(s._shuffleCount)

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
        if s._pos[0] > 0:
            s._switch_tiles(s._pos[0], s._pos[1], \
                            s._pos[0] - 1, s._pos[1])

    def move_down(s):
        if s._pos[0] < s.size - 1:
            s._switch_tiles(s._pos[0], s._pos[1], \
                            s._pos[0] + 1, s._pos[1])

    def move_left(s):
        if s._pos[1] > 0:
            s._switch_tiles(s._pos[0], s._pos[1], \
                            s._pos[0], s._pos[1] - 1)
    def move_right(s):
        if s._pos[1] < s.size - 1:
            s._switch_tiles(s._pos[0], s._pos[1], \
                            s._pos[0], s._pos[1] + 1)

    def _switch_tiles(s, r, c, r_prime, c_prime):
        temp = s.board[r][c]
        s.board[r][c] = s.board[r_prime][c_prime]
        s.board[r_prime][c_prime] = temp
        s._pos = (r_prime, c_prime)



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

def _main():
    print "Creating board. . ."
    size = 3
    if sys.argv.__len__() > 1:
        size = int(sys.argv[1])
        if size < 3:
            size = 3
    b = Board(size)
    b._print()

if __name__ == '__main__':
   _main() 
