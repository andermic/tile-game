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

    Shuffle_Count = 1000000

    def __init__(s, size):
        s.size = size

        s.board = [[(1 + x + y * s.size) % s.size**2 \
                for x in range(s.size)]\
                for y in range(s.size)]

        s._pos = (s.size - 1, s.size - 1)
        s.board_goal = copy.deepcopy(s.board) # Victory state.

    def shuffle(s, count=1):
        for x in range(count):
            print x

    def move_up(s):
        if s._pos[0] > 0:
            s._switch_tiles(s._pos[0], s._pos[1], \
                            s._pos[0] - 1, s._pos[1])

    def move_down(s):
        if s._pos[0] < s.size:
            s._switch_tiles(s._pos[0], s._pos[1], \
                            s._pos[0] + 1, s._pos[1])

    def move_left(s):
        if s._pos[1] > 0:
            s._switch_tiles(s._pos[0], s._pos[1], \
                            s._pos[0], s._pos[1] - 1)
    def move_right(s):
        if s._pos[1] < s.size:
            s._switch_tiles(s._pos[0], s._pos[1], \
                            s._pos[0], s._pos[1] + 1)

    def _switch_tiles(s, r, c, r_prime, c_prime):
        temp = s.board[r][c]
        s.board[r][c] = s.board[r_prime][c_prime]
        s.board[r_prime][c_prime] = temp
        s._pos = (r_prime, c_prime)

    def _print(s):
        for x in s.board:
            print x

def _main():
    b = Board(5)
    b.move_up()
    b._print()
    b.move_left()
    b._print()
    b.move_down()
    b._print()
    b.move_right()
    b._print()

if __name__ == '__main__':
   _main() 
