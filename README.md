# tictactoe

How to run the program:
python basic_tree.py
Runs the basic tic tac toe program and outputs to the command line
python tree.py
Runs the extra credit GUI tic tac toe program.

Project Team:
Frank Cipollone - tree structure/extra credit
Kim Ngo - search algorithm/improvements
Kendra Bilardello - search algorithm/improvements

Artificial Intelligence Project 1

There are three classes:

	tictactoe:

		holds a single game state of tic tac toe, and has a couple of functions to use on the game state including:

			win_state_x: returns true if x has won the game

			win_state_o: returns true if o has won the game

			get_game_chilren: returns a list of tictactoe objects which represents each next possible game state based on whose move is next

			print_state: prints the gamestate
	Node:

		represents a node in the tree. Has a parent variable to point to its parents node, and a list that holds its children. It also holds a tictactoe object. Functions:

			get_leaves: most useful function, returns a list of all leaves in the nodes subtree

			get_children: gets the list of the immediate children. Empty list if no children

			insert_child: adds a child node

			print_state: prints the gamestate it holds

			win_state_x: returns true if x has won the game in its gamestate

			win_state_o: returns true if o has won the game in its gamestate

	Tree:

		the tree object, holds the root node -- all other nodes are reachable from here. Also holds the current node, which can be 
		changed as the game is played. Has three useful functions:
		
			fill_game_tree(first_player, node): fills up the tree under a given node with all possible games based on whose move is 
			next.
			
			end_state: returns true if the state is an end state -- either a win or no more possible moves.
			
			set_currentNode: sets the current node

I added an example program at the bottom of the file



