#!/usr/bin/python
import copy
import sys
import random
import Tkinter
import time

from Tkinter import *

last_state_list = list()
current_state_list = list()

class tictactoe(object):
	def __init__(self, gameState=['.','.','.','.','.','.','.','.','.']):
		self.gameState = gameState

	#Check if 3 in a row in any way on the board
	def three_in_a_row(self, player):
		for it in range(0,3):
			if self.gameState[it*3] == player and self.gameState[3*it+1] == player and self.gameState[3*it+2] == player: #horizontally
				return True
			if self.gameState[it] == player and self.gameState[it+3] == player and self.gameState[it+6] == player: #vertically
				return True
		if self.gameState[0] == player and self.gameState[4] == player and self.gameState[8] == player: #diagonally
			return True
		if self.gameState[6] == player and self.gameState[4] == player and self.gameState[2] == player: #diagonally
			return True
		return False
	
	#If there are 3 x's in a row, x's win		
	def win_state_x(self):
		if self.three_in_a_row('x') and not(self.three_in_a_row('o')):
			return True
		return False
	#If there are 3 o's in a row, o's win
	def win_state_o(self):
		if self.three_in_a_row('o') and not(self.three_in_a_row('x')):
			return True
		return False

	#Returns the game children of the gameState
	def get_game_children(self, player):
		empty = []
		for pos in range(len(self.gameState)):
			if self.gameState[pos] == '.':
				newState = list(self.gameState)
				newState[pos] = player
				empty.append(newState)
		return empty

	#Checks if 2 in a row in any way on the board
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


	def trump(self, player, player2):
		if (self.gameState[0] == player or self.gameState[2] == player or self.gameState[6] == player or self.gameState[8] == player) and self.gameState[4] == '.':
			return 4
		if (self.gameState[0] == player or self.gameState[2] == player or self.gameState[6] == player or self.gameState[8] == player) and self.gameState[4] == player2:
			pick = [1,3,5,7]
			while True:
				check = random.choice(pick)
				if check != player or check != player2:
					return check
		#If they play in the middle, play in 2 corners
		if (self.gameState[4] == player):
			pick = [0,2,6,8]
			while True:
				check = random.choice(pick)
				if check != player or check != player2:
					return check
		return None

	#Prints the game board
	def print_state(self):
		string = str()
		for i in range(0,9):
			if i%3 == 0 and i != 0:
				print string
				string = str()
			string += self.gameState[i] + " "
		print string + "\n"

	#Gets last gamestate in a list (to compare for AI move)
	def get_AI_lastmove(self):
		global last_state_list
		last_state_list = self.gameState[:]

	#Gets current gamestate in a list (to compare for AI move)
	def get_AI_currmove(self):
		global current_state_list
		current_state_list = self.gameState[:]


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
	def get_AI_lastmove(self):
		self.tictactoe.get_AI_lastmove()
	def get_AI_currmove(self):
		self.tictactoe.get_AI_currmove()
	def trump(self, player):
		self.tictactoe.trump(player, player2)

class Tree(object):
	def __init__(self, root):
		root.depth = 0
		self.root = root
		self.currentNode = self.root
		self.lastNode = self.currentNode
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
			return True
		elif self.currentNode.tictactoe.win_state_o():
			return True
		elif len(self.currentNode.get_children()) <= 0:
			return True
		return False

	def end_state_print(self):
		if self.currentNode.tictactoe.win_state_x():
			print "Player 1 has won the game.\n"
		elif self.currentNode.tictactoe.win_state_o():
			print "Player 2 has won the game.\n"
		elif len(self.currentNode.get_children()) <= 0:
			print "The game is a tie.\n"

def valid_position(currentNode, position):
	# Converts position 1-9 and returns position x,y or None,None if invalid
	position = int(position)
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
	elif turn%2 == 1:
		two_in_a_row = currentNode.tictactoe.two_in_a_row('x')
	if two_in_a_row != None:
		pos = two_in_a_row
		for n in range(0, len(children)):
			if (turn%2 == 0 and children[n].get_gameState()[pos] == 'x') or (turn%2 == 1 and children[n].get_gameState()[pos] == 'o'):
				return n


	#Trump move
	trump = None
	if turn%2 == 0:
		trump = currentNode.tictactoe.trump('o', 'x')
	elif turn%2 == 1:
		trump = currentNode.tictactoe.trump('x', 'o')
	if trump != None:
		pos = trump
		for n in range(0, len(children)):
			if (turn%2 == 0 and children[n].get_gameState()[pos] == 'x') or (turn%2 == 1 and children[n].get_gameState()[pos] == 'o'):
				return n
		
	#print "Didn't need to make a trump move"
	# Checks for move with highest chance of winning using minimax algorithm

	for i in range(0,len(children)):
		#score = [0]
		score = 0
		for n in children[i].get_leaves():
			if (n.tictactoe.win_state_x() and turn%2 == 1) or (n.tictactoe.win_state_o() and turn%2 == 0):
				score += 10
				#score.append(10-(n.depth-currentNode.depth))
			elif n.tictactoe.win_state_o():
				score -= 10
				#score.append((n.depth-currentNode.depth)-10)
		if turn%2 == 0: # highest score is the optimal move for x
			#if max(score) > most_wins:
				#most_wins = max(score)
			if score > most_wins:
				most_wins = score
			best_node = i
		else: # lowest score is optimal move for o
			#if max(score) < most_wins:
				#most_wins = max(score)
			if score < most_wins:
				most_wins = score
			best_node = i
	return best_node

def print_move(turn):
	sys.stdout.write("Move #" + str(turn+1) + ": enter choice for player " + str(turn%2+1) + " : ")

def print_AImove(turn, position):
	sys.stdout.write("Move #" + str(turn+1) + ": enter choice for player " + str(turn%2+1) + " : " + str(position) + "\n\n")




class PlayGame:
	def __init__(self, comp):
		self.t = Tree(Node(tictactoe()))
		self.t.fill_game_tree('x', self.t.root)
		self.COMPUTER = comp
		self.turn = 0
	def reset(self, comp):
		self.t.currentNode = self.t.root
		self.COMPUTER = comp
		self.turn = 0

	def compare_states(self,last_state, current_state):
		last_state.get_AI_lastmove()
		current_state.get_AI_currmove()
		
		for i in range(0,9):
			if current_state_list[i] != last_state_list[i]:
				return i+1
	def playGame(self, inputNum = 0):
		###Example usage
		#initialize a tree with a root node with an empty game state
		#print "Setting up game tree"
		#fill up the game tree. This sets each nodes children to be the game states of the next possible moves
 # keeps track of player's turn; x == 0, o == 1

		# User input for single or dual agent

		#self.t.currentNode.print_state()
		# Game loop
		if(not(self.t.end_state())):
			children = self.t.currentNode.get_children()

			# User input
			if self.COMPUTER == 1 and self.turn%2 == 0:
				#print_move(turn)
				position = inputNum
				pos = valid_position(self.t.currentNode, position)
				while pos == None:
					#print "Invalid input. Please enter a number 1-9 that corresponds to an empty position"
					#print_move(self.turn)
					return -1

				for child in children:
					if child.get_gameState()[pos] == 'x':
						self.t.currentNode = child
				#print_move(turn, position)

			# AI
			else:
				self.t.lastNode = copy.copy(self.t.currentNode) #Keeps track of last gamestate
				best_node = minimax(self.turn, self.t.currentNode, children)
				self.t.currentNode = children[best_node]
				#pos variable is the move the AI takes
				pos = self.compare_states(self.t.lastNode, self.t.currentNode) #Compares last and curr state
				#print_AImove(turn, pos)
			#self.t.currentNode.print_state()
			self.turn+=1
			if self.t.currentNode.tictactoe.win_state_x() or self.t.currentNode.tictactoe.win_state_o():
				return 0
			return 1
		else:
			return 0



def print_move(turn):
	sys.stdout.write("Move #" + str(turn+1) + ": enter choice for player " + str(turn%2+1) + " : ")

def print_AImove(turn, position):
	sys.stdout.write("Move #" + str(turn+1) + ": enter choice for player " + str(turn%2+1) + " : " + str(position) + "\n\n")

def compare_states(last_state, current_state):
	last_state.get_AI_lastmove()
	current_state.get_AI_currmove()
	
	for i in range(0,9):
		if current_state_list[i] != last_state_list[i]:
			return i+1

class Application(Frame):

    def callback(self, num):
    	if self.gameState == 1:
    		if self.gameTree.t.currentNode.gameState[num] == '.' and not self.gameTree.t.currentNode.tictactoe.win_state_x() and not self.gameTree.t.currentNode.tictactoe.win_state_o():

	    		r = self.gameTree.playGame(num+1)
	    		if r == 0:
	    			self.update()
	    			#self.clear_all()
	    		pos = compare_states(self.gameTree.t.lastNode, self.gameTree.t.currentNode) #Compares last and curr state	    			
	    		print_AImove(self.gameTree.turn-1, pos)
	    		self.gameTree.t.currentNode.print_state()

	    		r = self.gameTree.playGame()
	    		if r == 0:
	    			self.update()
	    			#self.clear_all()
	    		pos = compare_states(self.gameTree.t.lastNode, self.gameTree.t.currentNode) #Compares last and curr state	    			
	    		print_AImove(self.gameTree.turn-1, pos)
	   	    	self.gameTree.t.currentNode.print_state()

	    		self.update()
	    		self.gameTree.t.end_state_print()




    def update(self):
	    for i in range(0,len(self.placementArray)):
			if self.gameTree.t.currentNode.gameState[i] == '.':
				self.placementArray[i]['text'] = ''
			elif self.gameTree.t.currentNode.gameState[i] == 'x':
				self.placementArray[i]['text'] = 'X'
			elif self.gameTree.t.currentNode.gameState[i] == 'o':
				self.placementArray[i]['text'] = 'O'

    def start1Agent(self):
    	self.gameState = 1

    	for el in self.placementArray:
    		el['state'] = 'normal'
    	self.gameTree.reset(1)
    	self.start2Player['state'] = 'disabled'
    	self.start1Player['state'] = 'disabled'
    	self.clear['state'] = 'normal'
    	print "One Agent Game"
    	self.gameTree.t.currentNode.print_state()



    def start2Agent(self):
    	if self.gameState == 2:
    		if not self.gameTree.t.end_state():
	    		r = self.gameTree.playGame()
	    		pos = compare_states(self.gameTree.t.lastNode, self.gameTree.t.currentNode) #Compares last and curr state
	    		print_AImove(self.gameTree.turn-1, pos)
	    		self.gameTree.t.currentNode.print_state()
	    		self.update()
	    		self.gameTree.t.end_state_print()

    	else:
	    	self.gameState = 2
    		self.start2Player['text'] = "Next"
    		self.start1Player['state'] = 'disabled'
    		self.gameTree.reset(2)
    		self.clear['state'] = 'normal'
    		print "Two Agent Game"
    		self.gameTree.t.currentNode.print_state()


    def clear_all(self):
    	self.update()
    	self.gameState = 0
    	self.start2Player['state'] = 'normal'
    	self.start1Player['state'] = 'normal'
    	self.start2Player['text'] = "Start 2 agent game"
    	for el in self.placementArray:
    		el['state'] = 'disabled'
    	self.gameTree.t.currentNode = self.gameTree.t.root
    	self.update()
    	self.clear['state'] = 'disabled'



    def createWidgets(self):
    	self.gameState = 0
    	self.placementArray = []
    	self.button0 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(0), text = "")
    	self.button1 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(1), text = "")
    	self.button2 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(2), text = "")
    	self.button3 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(3), text = "")
    	self.button4 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(4), text = "")
    	self.button5 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(5), text = "")
    	self.button6 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(6), text = "")
    	self.button7 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(7), text = "")
    	self.button8 = Button(self, font = ("Helvetica", 128), command = lambda: self.callback(8), text = "")
    	self.placementArray.append(self.button0)
    	self.placementArray.append(self.button1)
    	self.placementArray.append(self.button2)
    	self.placementArray.append(self.button3)
    	self.placementArray.append(self.button4)
    	self.placementArray.append(self.button5)
    	self.placementArray.append(self.button6)
    	self.placementArray.append(self.button7)
    	self.placementArray.append(self.button8)
    	count = 0
    	for el in self.placementArray:
    		el.grid(row = 1+int(count/3), column = 1+count % 3)
    		el.config(height=1, width=2)
    		el['state'] = 'disabled'
    		count+=1

    	self.myLabel = Label(self, font = ("Helvetica", 36))
    	self.myLabel["text"] = "Tic Tac Toe"
    	self.myLabel.grid(row = 0, column = 1, columnspan = 3)
    	self.start1Player = Button(self, font = ('Helvetica', 16), text = "Start 1 agent game", command = self.start1Agent)
    	self.start1Player.grid(row=1,column =0)
    	self.start1Player.config(height=6,width=20)
      	self.start2Player = Button(self, font = ('Helvetica', 16), text = "Start 2 agent game", command = self.start2Agent)
    	self.start2Player.grid(row=2,column =0)
    	self.start2Player.config(height=6,width=20)
    	self.clear = Button(self, font = ('Helvetica', 16), text = "Clear", command = self.clear_all)
    	self.clear.grid(row=3,column =0)
    	self.clear.config(height=6,width=20)
    	self.clear['state'] = 'disabled'


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.gameTree = PlayGame(1)
        print "Game Tree Loaded"

if __name__ == '__main__':
	root = Tk()
	app = Application(master=root)
	app.mainloop()
	root.destroy()
