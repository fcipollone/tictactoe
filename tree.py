#!/usr/bin/python

class tictactoe(object):
	def __init__(self, gameState=['.','.','.','.','.','.','.','.','.']):
		self.gameState = gameState

	def three_in_a_row(self, player):
		for it in range(0,3):
			if self.gameState[it*3] == player and self.gameState[3*it+1] == player and self.gameState[3*it+2] == player:
				return True
			if self.gameState[it] == player and self.gameState[it+3] == player and self.gameState[it+6] == player:
				return True
		if self.gameState[0] == player and self.gameState[4] == player and self.gameState[8] == player:
			return True
		if self.gameState[6] == player and self.gameState[4] == player and self.gameState[2] == player:
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
		empty = []
		for pos in range(len(self.gameState)):
			if self.gameState[pos] == '.':
				newState = list(self.gameState)
				newState[pos] = player
				empty.append(newState)
		return empty

	def two_in_a_row(self, player):
		#Horizontal
		for it in range(0,3):
			if self.gameState[it*3] == player and self.gameState[3*it+1] == player and self.gameState[3*it+2] == '.':
				return 3*it+2
			elif self.gameState[it*3] == player and self.gameState[3*it+1] == '.' and self.gameState[3*it+2] == player:
				return 3*it+1
			elif self.gameState[it*3] == '.' and self.gameState[3*it+1] == player and self.gameState[3*it+2] == player:
				return 3*it
	
		#Vertical
		for it in range(0,3):
			if self.gameState[it] == player and self.gameState[it+3] == player and self.gameState[it+6] == '.':
				return it+6
			elif self.gameState[it] == player and self.gameState[it+3] == '.' and self.gameState[it+6] == player:
				return it+3
			elif self.gameState[it] == '.' and self.gameState[it+3] == player and self.gameState[it+6] == player:
				return it
	
		#Diagonal
		if self.gameState[0] == player and self.gameState[4] == player and self.gameState[8] == '.':
			return 8
		elif self.gameState[0] == player and self.gameState[4] == '.' and self.gameState[8] == player:
			return 4
		elif self.gameState[0] == '.' and self.gameState[4] == player and self.gameState[8] == player:
			return 0
		elif self.gameState[6] == player and self.gameState[4] == player and self.gameState[2] == '.':
			return 2
		elif self.gameState[6] == player and self.gameState[4] == '.' and self.gameState[2] == player:
			return 4
		elif self.gameState[6] == '.' and self.gameState[4] == player and self.gameState[2] == player:
			return 6

		return None


	def print_state(self):
		returnString = ""
		#for i in range(0,9):
		#	returnString += " "
		#	returnString += self.gameState[i]
		#	if i != 2 or i != 5 or i != 8:
		#		returnString += " | "
		##	if i == 2 or i == 5:
		#		returnString += "\n-----------"
		#	#returnString += "\n"
		#print returnString

		string = str()
		for i in range(0,9):
			if i%3 == 0 and i != 0:
				print string
				string = str()
			string += self.gameState[i] + " "
		print string + "\n"





class Node(object):
	def __init__(self, tictactoe):
		self.tictactoe = tictactoe
		self.gameState = self.tictactoe.gameState
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
		self.tictactoe.print_state()

	def get_gameState(self):
		return self.gameState
	

class Tree(object):
	def __init__(self, root):
		root.depth = 0
		self.root = root
		self.currentNode = self.root
	def fill_game_tree(self, first_player, node):
		if (not(node.tictactoe.win_state_o()) and not(node.tictactoe.win_state_x())):
			gameStates = node.tictactoe.get_game_children(first_player)
			for s in gameStates:
				n = Node(tictactoe(s))
				node.insert_child(n)
				if first_player == 'x':
					self.fill_game_tree('o',n)
				else:
					self.fill_game_tree('x',n)

	def set_currentNode(self, node):
		self.currentNode = node

	def end_state(self):
		if self.currentNode.tictactoe.win_state_x():
			print "Player 1 has won"
			return True
		elif self.currentNode.tictactoe.win_state_o():
			print "Player 2 has won"
			return True
		elif len(self.currentNode.get_children()) <= 0:
			print "The game is a tie."
			return True
		return False

def valid_position(currentNode, position):
	# Converts position 1-9 and returns position x,y or None,None if invalid
	position = int(position)
	#x,y = convert_position(position)
	#if [x,y] != [None,None]:
	if currentNode.get_gameState()[position-1] != '.':
			return None
	return position-1

def minimax(turn, currentNode, children):
	best_node = 0
	most_wins = 0

	# Guarantees to make the winning move
	for i in range(0,len(children)):
		if turn%2 == 0 and children[i].tictactoe.win_state_x() or turn%2 == 1 and children[i].tictactoe.win_state_o():
			return i
		
	# Blocks other player from winning
	two_in_a_row = None
	if turn%2 == 0:
		two_in_a_row = currentNode.tictactoe.two_in_a_row('o')
		#print "x", two_in_a_row
	elif turn%2 == 1:
		two_in_a_row = currentNode.tictactoe.two_in_a_row('x')
		#print "o", two_in_a_row
	if two_in_a_row != None:
		#print two_in_a_row
		pos = two_in_a_row
		for n in range(0, len(children)):
			if (turn%2 == 0 and children[n].get_gameState()[pos] == 'x') or (turn%2 == 1 and children[n].get_gameState()[pos] == 'o'):
				#print "OPTIMAL"
				#print children[n].get_gameState()
				return n

	# Checks for move with highest chance of winning using minimax algorithm
	for i in range(0,len(children)):
		score = [0]
		#score = 0
		for n in children[i].get_leaves():
			if (n.tictactoe.win_state_x() and turn%2 == 1) or (n.tictactoe.win_state_o() and turn%2 == 0):
				#score += 10
				score.append(10-(n.depth-currentNode.depth))
			elif n.tictactoe.win_state_o():
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
	#pos = convert_position(position)
	print "Move #" + str(turn+1) + ": player " + str(turn%2+1) + " plays " + str(position) + ":"

if __name__ == "__main__":
	###Example usage
	#initialize a tree with a root node with an empty game state
	print "Setting up game tree"
	t = Tree(Node(tictactoe()))
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
			pos = valid_position(t.currentNode, position)
			while pos == None:
				print "Invalid input. Please enter a number 1-9 that corresponds to an empty position"
				pos = valid_position(t.currentNode, input('> '))
			for child in children:
				if child.get_gameState()[pos] == 'x':
					t.currentNode = child
			print_move(turn, position)

		# AI
		else:
			best_node = minimax(turn, t.currentNode, children)
			t.currentNode = children[best_node]
			#print_move(turn, 1000)
		t.currentNode.print_state()
		turn+=1
