#!/usr/bin/python

class tictactoe(object):
	def __init__(self, string = ""):
		if string == "":
			self.gameState = [["", "", ""], ["", "", ""], ["", "", ""]]
		else:
			places = string.split(",")
			if len(places) != 9:
				self.gameState = [["", "", ""], ["", "", ""], ["", "", ""]]
			else:
				self.gameState = []
				for row in range(0,3):
					self.gameState.append(list())
					for col in range(0,3):
						self.gameState[row].append(places[row*3 + col])
	def three_in_a_row(self, player):
		for it in range(0,3):
			if self.gameState[it][0] == player and self.gameState[it][1] == player and self.gameState[it][2] == player:
				return True
			if self.gameState[0][it] == player and self.gameState[1][it] == player and self.gameState[2][it] == player:
				return True
		if self.gameState[0][0] == player and self.gameState[1][1] == player and self.gameState[2][2] == player:
			return True
		if self.gameState[0][2] == player and self.gameState[1][1] == player and self.gameState[2][0] == player:
			return True
		return False
	def win_state_x(self):
		if self.three_in_a_row('x') and not(self.three_in_a_row('o')):
			return True
		return False
	def win_state_o(self):
		if self.three_in_a_row('o') and not(self.three_in_a_row('x')):
			return True
		return False
	def get_game_children(self, player):
		returnList = []
		for row in range(0,3):
			for col in range(0,3):
				if self.gameState[row][col] != 'x' and self.gameState[row][col] != 'o' :
					stateString = ""
					for row_return in range(0,3):
						for col_return in range(0,3):
							if row == row_return and col == col_return:
								if row_return == 2 and col_return == 2:
									stateString += player
								else:
									stateString += player + ","
							else:
								if row_return == 2 and col_return == 2:
									stateString += self.gameState[row_return][col_return]
								else:
									stateString += self.gameState[row_return][col_return] + ","
					returnList.append(tictactoe(stateString))
		return returnList

	def two_in_a_row(self, player):
		# Checks for potential win and returns position to block: x,y
		for y in range(0,3):	# Check horizontal
			if self.gameState[y][1] == player and self.gameState[y][0] == player and self.gameState[y][2] == ' ':
				return [2,y]
			elif self.gameState[y][1] == player and self.gameState[y][1] == player and self.gameState[y][0] == ' ':
				return [0,y]
			elif self.gameState[y][0] == player and self.gameState[y][2] == player and self.gameState[y][1] == ' ':
				return [1,y]
		for x in range(0,3): # Check vertical
			if self.gameState[1][x] == player and self.gameState[0][x] == player and self.gameState[2][x] == ' ':
				return [x,2]
			elif self.gameState[1][x] == player and self.gameState[2][x] == player and self.gameState[0][x] == ' ':
				return [x,0]
			elif self.gameState[0][x] == player and self.gameState[2][x] == player and self.gameState[1][x] == ' ':
				return [x,1]
		# Check diagonal
		if self.gameState[1][1] == player and self.gameState[0][0] == player and self.gameState[2][2] == ' ':
			return [2,2]
		elif self.gameState[1][1] == player and self.gameState[2][2] == player and self.gameState[0][0] == ' ':
			return [0,0]
		elif self.gameState[1][1] == player and self.gameState[2][0] == player and self.gameState[0][2] == ' ':
			return [2,0]
		elif self.gameState[1][1] == player and self.gameState[0][2] == player and self.gameState[2][0] == ' ':
			return [0,2]
		elif self.gameState[0][0] == player and self.gameState[2][2] == player and self.gameState[1][1] == ' ':
			return [1,1]
		elif self.gameState[0][2] == player and self.gameState[2][0] == player and self.gameState[1][1] == ' ':
			return [1,1]
		return None 

	def print_state(self):
		returnString = ""
		for row in range(0,3):
			returnString += " "
			for col in range(0,3):
				returnString += self.gameState[row][col]
				if col < 2:
					returnString += " | "
			if row < 2:
				returnString += "\n-----------"
			returnString += "\n"
		print returnString


class Node(object):
	def __init__(self, gameState):
		self.gameState = gameState
		self.parent = None
		self.children = []
		self.depth = None
	def get_leaves(self):
		returnList = []
		if len(self.children) == 0:
			returnList.append(self)
		else:
			for node in self.children:
				for leaf in node.get_leaves():
					returnList.append(leaf)
		return returnList
	def get_children(self):
		return self.children
	def insert_child(self, node):
		node.parent = self
		node.depth = self.depth+1
		self.children.append(node)
	def print_state(self):
		self.gameState.print_state()
	
	def win_state_x(self):
		return self.gameState.win_state_x()

	def win_state_o(self):
		return self.gameState.win_state_o()

	def two_in_a_row(self, player):
		return self.gameState.two_in_a_row(player) 

	def get_gameState(self):
		return self.gameState.gameState


class Tree(object):
	def __init__(self, root):
		root.depth = 0
		self.root = root
		self.currentNode = self.root
	def fill_game_tree(self, first_player, node):
		if (not(node.gameState.win_state_o()) and not(node.gameState.win_state_x())):
			for el in node.gameState.get_game_children(first_player):
				n = Node(el)
				node.insert_child(n)
				if first_player == 'x':
					self.fill_game_tree('o',n)
				else:
					self.fill_game_tree('x',n)

	def set_currentNode(self, node):
		self.currentNode = node

	def end_state(self):
		if self.currentNode.gameState.win_state_x():
			print "Player 1 has won"
			return True
		elif self.currentNode.gameState.win_state_o():
			print "Player 2 has won"
			return True
		elif len(self.currentNode.get_children()) <= 0:
			print "The game is a tie."
			return True
		return False

def valid_position(currentNode, position):
	# Converts position 1-9 and returns position x,y or None,None if invalid
	x,y = None, None
	position = int(position)
	x,y = convert_position(position)
	if [x,y] != [None,None]:
		if currentNode.get_gameState()[y][x] != ' ':
			x,y = None,None
	return [x,y]

def convert_position(position):
	x,y = None, None
	position = int(position)
	if position == 1:
		x,y = 0,0
	elif position == 2:
		x,y = 1,0
	elif position == 3:
		x,y = 2,0
	elif position == 4:
		x,y = 0,1
	elif position == 5:
		x,y = 1,1
	elif position == 6:
		x,y = 2,1
	elif position == 7:
		x,y = 0,2
	elif position == 8:
		x,y = 1,2
	elif position == 9:
		x,y = 2,2
	return [x,y]

def minimax(turn, currentNode, children):
	best_node = 0
	most_wins = 0

	# Guarantees to make the winning move
	for i in range(0,len(children)):
		if turn%2 == 0 and children[i].win_state_x() or turn%2 == 1 and children[i].win_state_o():
			return i
		
	# Blocks other player from winning
	two_in_a_row = None
	if turn%2 == 0:
		two_in_a_row = currentNode.two_in_a_row('o')
		#print "x", two_in_a_row
	elif turn%2 == 1:
		two_in_a_row = currentNode.two_in_a_row('x')
		#print "o", two_in_a_row
	if two_in_a_row != None:
		#print two_in_a_row
		x,y = two_in_a_row
		for n in range(0, len(children)):
			if (turn%2 == 0 and children[n].get_gameState()[y][x] == 'x') or (turn%2 == 1 and children[n].get_gameState()[y][x] == 'o'):
				#print "OPTIMAL"
				#print children[n].get_gameState()
				return n

	# Checks for move with highest chance of winning using minimax algorithm
	for i in range(0,len(children)):
		score = [0]
		#score = 0
		for n in children[i].get_leaves():
			if (n.win_state_x() and turn%2 == 1) or (n.win_state_o() and turn%2 == 0):
				#score += 10
				score.append(10-(n.depth-currentNode.depth))
			elif n.win_state_o():
				#score -= 10
				score.append((n.depth-currentNode.depth)-10)
		if turn%2 == 0: # highest score is the optimal move for x
			if max(score) > most_wins:
				most_wins = max(score)
				#if score > most_wins:
				#most_wins = score
				best_node = i
		else: # lowest score is optimal move for o
			if max(score) < most_wins:
				most_wins = max(score)
				#if score < most_wins:
				#	most_wins = score
				best_node = i
	return best_node

def print_move(turn, position):
	x,y = convert_position(position)
	print "Move #" + str(turn+1) + ": player " + str(turn%2+1) + " plays " + str(position) + ":"

if __name__ == "__main__":
	###Example usage
	#initialize a tree with a root node with an empty game state
	print "Setting up game tree"
	t = Tree(Node(tictactoe(" , , , , , , , , ")))
	#fill up the game tree. This sets each nodes children to be the game states of the next possible moves
	t.fill_game_tree('x', t.root)
	print "Game tree set up. Ready to play"
	turn = 0 # keeps track of player's turn; x == 0, o == 1

	# User input for single or dual agent
	COMPUTER = input('Enter choice (1 for single agent, 2 for dual agents): ')
	while COMPUTER != 1 and COMPUTER != 2:
		COMPUTER = input('Enter choice (1 for single agent, 2 for dual agents): ')

	# Game loop
	while(not(t.end_state())):
		children = t.currentNode.get_children()

		# User input
		if COMPUTER == 1 and turn%2 == 0:
			position = input('> ')			
			x,y = valid_position(t.currentNode, position)
			while [x,y] == [None,None]:
				print "Invalid input. Please enter a number 1-9 that corresponds to an empty position"
				x,y = valid_position(t.currentNode, input('> '))
			for child in children:
				if child.get_gameState()[y][x] == 'x':
					t.currentNode = child
			print_move(turn, position)

		# AI
		else:
			best_node = minimax(turn, t.currentNode, children)
			t.currentNode = children[best_node]
		t.currentNode.print_state()
		turn+=1




