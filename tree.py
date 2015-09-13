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
		self.children.append(node)
	def print_state(self):
		self.gameState.print_state()
		
	def win_state_x(self):
		return self.gameState.win_state_x()

	def win_state_o(self):
		return self.gameState.win_state_o()




class Tree(object):
	def __init__(self, root):
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
		if (not(self.currentNode.gameState.win_state_o()) and not(self.currentNode.gameState.win_state_x())):
			if len(self.currentNode.get_children()) > 0:
				return False
		return True

if __name__ == "__main__":
	###Example usage
	#initialize a tree with a root node with an empty game state
	t = Tree(Node(tictactoe(" , , , , , , , , ")))
	#fill up the game tree. This sets each nodes children to be the game states of the next possible moves
	t.fill_game_tree('x', t.root)
	while(not(t.end_state())):
		best_node = 0
		most_wins = 0
		for i in range(0,len(t.currentNode.get_children())):
			##perform some calculations -- here is where you compare which move is best
			wins = 0
			for n in t.currentNode.get_children()[i].get_leaves():
				if n.win_state_x():
					wins+=1
			if wins > most_wins:
				most_wins = wins
				best_node = i
		t.currentNode = t.currentNode.get_children()[best_node]
		t.currentNode.print_state()





