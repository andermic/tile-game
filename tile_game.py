#!/usr/bin/env python2.7
#
# This is an AI that solves a tile game!
#

import pygame, time, sys, os
from heapq import *
from os import listdir, system
from pygame.locals import *
from random import choice


class Game():
	move_count = -1

	def __init__(s, size):
		s.N = size
		s.board_initial = [[(1+j+i*s.N)%(s.N*s.N) for j in range(N)] for i in range(N)]
		s.board = [[(1+j+i*s.N)%(s.N*s.N) for j in range(N)] for i in range(N)]
		s.shuffle(10000)
		
		if 'record.txt' not in listdir('.'):
			open('record%d.txt' % s.N,'w').write('999')
		s.record = int(open('record%d.txt' % s.N,'r').read())

		screen = pygame.display.set_mode((150, 50))
		pygame.display.set_caption('Tile Game')
		clock = pygame.time.Clock()
		while True:
			clock.tick(60)
			for event in pygame.event.get():
				s.event_handler(event)

	def display(s, b):
		hori_divider = ' ----' * s.N + ' '
		vert_divider = '|    ' * s.N + '|'
		if (os.name == 'nt'):
			system('cls')
		else:
			system('clear')
		for i in range(s.N):
			print hori_divider
			print vert_divider
			for j in range(s.N):
				print '|',
				print_str = str(b[i][j])
				if b[i][j] < 10:
					print_str = '0' + print_str
				if print_str == '00':
					print_str = '  '
				print print_str,
			print '|'
			print vert_divider
		print hori_divider
		s.move_count += 1
		print 'Moves made: %d' % s.move_count
		print 'Manhattan distances: %d' % s.manhattan_weighted(b)
		
	def find_tile(s,b,tile):
		for i in range(s.N):
			for j in range(s.N):
				if b[i][j] == tile:
					return i,j

	def finish(s, b=None):
		print 'Done! It took you %d moves.' % s.move_count
		if s.move_count < s.record:
			print 'You beat your previous record of %d moves!' % s.record
			open('record%d.txt' % s.N,'w').write(str(s.move_count))
		else:
			print 'Your currect record is %d moves.' % s.record
		exit()

	def move_up(s, b, disp, check):
		zero = s.find_tile(b, 0)
		if zero[0] != 0:
			b[zero[0]][zero[1]], b[zero[0]-1][zero[1]] = \
			 b[zero[0]-1][zero[1]], b[zero[0]][zero[1]]
		else:
			return None
		if disp:
			s.display(b)
		if check and b == s.board_initial:
			return "finish"
		return b

	def move_down(s, b, disp, check):
		zero = s.find_tile(b, 0)
		if zero[0] != s.N-1:
			b[zero[0]][zero[1]], b[zero[0]+1][zero[1]] = \
			 b[zero[0]+1][zero[1]], b[zero[0]][zero[1]]
		else:
			return None
		if disp:
			s.display(b)
		if check and b == s.board_initial:
			return "finish"
		return b

	def move_left(s, b, disp, check):
		zero = s.find_tile(b, 0)
		if zero[1] != 0:
			b[zero[0]][zero[1]], b[zero[0]][zero[1]-1] = \
			 b[zero[0]][zero[1]-1], b[zero[0]][zero[1]]
		else:
			return None
		if disp:
			s.display(b)
		if check and b == s.board_initial:
			return "finish"
		return b
		
	def move_right(s, b, disp, check):
		zero = s.find_tile(b, 0)
		if zero[1] != s.N-1:
			b[zero[0]][zero[1]], b[zero[0]][zero[1]+1] = \
			 b[zero[0]][zero[1]+1], b[zero[0]][zero[1]]
		else:
			return None
		if disp:
			s.display(b)
		if check and b == s.board_initial:
			return "finish"
		return b

	def move(s, b, dir, disp, check):
		if dir == 'up':
			return s.move_up(b, disp, check)
		elif dir == 'down':
			return s.move_down(b, disp, check)
		elif dir == 'left':
			return s.move_left(b, disp, check)
		elif dir == 'right':
			return s.move_right(b, disp, check)
		
	def random_move(s, b, no_redundant = False):
		move_dir = choice(['up', 'down', 'left', 'right'])
		return s.move(b, move_dir, False, False)

	def event_handler(s, event):
		if event.type == KEYDOWN:
			if pygame.key.name(event.key) == 'n':
				Game()
			else:
				res = s.move(s.board, pygame.key.name(event.key), True, True)
				if res == None:
					pass
				elif res == "finish":
					s.finish()
				else:
					s.board = res
	
	def manhattan(s, b):
		sum = 0
		for tile in range(1,s.N*s.N):
			actual = list(s.find_tile(b,tile))
			correct = [(tile - 1) / s.N, (tile - 1) % s.N]
			distance = abs(actual[0] - correct[0]) + abs(actual[1] - correct[1])
			sum = sum + distance
		return sum
	
	def manhattan_weighted(s, b):
		sum = 0
		for tile in range(1,s.N*s.N):
			actual = list(s.find_tile(b,tile))
			correct = [(tile - 1) / s.N, (tile - 1) % s.N]
			distance = abs(actual[0] - correct[0]) + abs(actual[1] - correct[1])
			for i in range(s.N-1):
				if correct[0] == i or correct[1] == i:
					distance *= 1
					break
			sum = sum + distance
		return sum

	def shuffle(s, n):
		for i in range(n):
			res = s.random_move(s.board[:])
			if res != None:
				s.board = res
		s.display(s.board)


class Computer_Game(Game):
	already_visited = {}
	frontier = []

	def __init__(s, size):
		s.N = size
		s.board_initial = [[(1+j+i*s.N)%(s.N*s.N) for j in range(s.N)] for i in range(s.N)]
		s.board = [[(1+j+i*s.N)%(s.N*s.N) for j in range(s.N)] for i in range(s.N)]
		s.shuffle(10000)
		
		s.start_time = time.clock()
		s.check_and_update_av([s.board], None)
		
		#(HEURISTIC + DEPTH, HEURISTIC, DEPTH, POSITION)
		s.frontier.append((s.manhattan_weighted(s.board) + 0, s.manhattan_weighted(s.board), 0, s.board))
		
		s.node_count = 1
		while True:
			# Get the best node in the frontier
			best = heappop(s.frontier)
			
			# Expand the node
			if s.node_count % 1000 == 0:
				print s.node_count,
				print best[2],
				print s.manhattan_weighted(best[3])
			children = [s.move([row[:] for row in best[3]], dir, False, True) for dir in ['up', 'down', 'left', 'right']]			
			if "finish" in children:
				s.finish(best[3])
			s.node_count = s.node_count + 1
			current_depth = best[2] + 1

			# Uncomment for A*. Slow but strong solutions.
			children = [(s.manhattan_weighted(c), current_depth, c) for c in s.check_and_update_av(children, best[3])]
			children = [(c[0]+c[1], c[0], c[1], c[2]) for c in children]
			
			# Uncomment for fast but weak solutions.
			#children = [(s.manhattan_weighted(c), s.manhattan_weighted(c), current_depth, c) for c in s.check_and_update_av(children, best[3])]
			
			# Update frontier
			for c in children:
				heappush(s.frontier, c)

	# Keep already_visited in a hierarchical dictionary structure for quick membership testing.
	def check_and_update_av(s, nodes, parent):
		new_nodes = []
		for node in nodes:
			if node == None:
				continue
			add = False
			level = s.already_visited
			for i in range(s.N):
				for j in range(s.N):
					if not add:
						next_level = level.get(node[i][j])
						if next_level == None:
							add = True
					if add:
						level[node[i][j]] = {}
						next_level = level[node[i][j]]
					level = next_level
			if add:
				new_nodes.append(node)
				level["parent"] = parent
		return new_nodes
	
	# Keep already_visited in a heap structure for memory efficiency. Or possibly some kind of encoded-string adhoc hashing system?
	def check_and_update_av2(s, nodes, parent):
		pass
	
	def event_handler(s, event):
		pass
	
	# Walk through a solution
	def finish(s, b):
		total_time = time.clock() - s.start_time
		print "Solution found!"
		raw_input("Press Enter to continue")
		
		boards_stack = [b]
		while True:
			level = s.already_visited
			for i in range(s.N):
				for j in range(s.N):
					level = level[b[i][j]]
			b = level["parent"]
			if b == None:
				break
			boards_stack.append(b)
		
		boards_stack.pop()
		for i in range(len(boards_stack)):
			board = boards_stack.pop()
			s.display(board)
			raw_input("Press Enter to continue")
		
		s.display(s.board_initial)
		print "Calculation time: %s" % str(total_time)
		print "Nodes expanded: %d" % s.node_count
		exit()
	
	def evaluation(s, b, current):
		pass


if __name__ == '__main__':
	pygame.init()
	N = int(sys.argv[1])
	Game(N)
	#Computer_Game(N)

# vim: noexpandtab shiftwidth=4 tabstop=4 
