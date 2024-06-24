# CS305 Park University
# Project Solution Code
# Game-Playing Agents

# implememntation of reversi
# https://www.mathsisfun.com/games/reversi.html

# For your project, you must complete the game search implementation (note the
# TODO comments below) as well as develop a competitve heuristic for your
# tournament entry. 

from masProblem import Node
from gameClient import GameClient
from gameClient import IllegalMove
from copy import deepcopy



starting_board = {
            'white': {(4, 4), (5, 5)},
            'black': {(4, 5), (5, 4)}
}     

            
def is_board_coordinate(c):
    return type(c) == int and c >= 1 and c <= 8

def is_board_coordinates(t):
    """Determines if t is a proper description of coordinates on the board
       First element is an integer between 1 and 8 representing the row
         (higher numbers are further up)
       Second element is an integer between 1 and 8 representing the column
         (higher numbers to the right)
    """
    return type(t) == tuple and len(t) == 2 and \
           is_board_coordinate(t[0]) and \
           is_board_coordinate(t[1])

class Reversi(Node):
    def __init__(self, isMax=True, move=None, prior_moves=[], newboard=starting_board):
        """Initializes the game node.
           isMax is True when it is white's turn and false when it is black's
           move is a 2-tuple of coordinates (from, to) as validated by is_coordinates
           prior_moves is a list of moves taken in the game so far
           newboard is a board dictionary determining piece locations (see starting_board)
           """
        super().__init__(str(move), isMax, None, None)
        self.prior_moves = [move] + prior_moves if move else []
        self.board = deepcopy(newboard)
        
        # process move if it is indicated
        if move:
            # validate move
            if not is_board_coordinates(move):
                raise IllegalMove("not a valid Chad move format")
            
            piece = self.tile_type(move)
            
            if piece != '.':
                raise IllegalMove("playing piece already at " + str(move))
            
            if move not in self.legal_moves():
                raise IllegalMove(('white' if isMax else 'black') + " player cannot legally move to " + str(move)) 
            
            # Process placement / capture
            self.process_move(move)
            # Add move to move history and flip turn
            self.move = move
            self.isMax = not self.isMax

            # Skip turn if no moves
            if not list(self.legal_moves()):  
                self.isMax = not self.isMax
            self.move = move
            self.isMax = not self.isMax
            
            # skip turn if no moves
            if not list(self.legal_moves()):
                self.isMax = not self.isMax
            
    def process_move(self, move):
        """Processes a move, capturing opponent pieces as needed."""

        player_color = 'white' if self.isMax else 'black'
        opponent_color = 'black' if self.isMax else 'white'
        self.board[player_color].add(move)  # Place the piece on the board

        directions = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1),   # right
            (-1, -1), # up-left
            (-1, 1),  # up-right
            (1, -1),  # down-left
            (1, 1)    # down-right
        ]

        for check_x, check_y in directions:
            x, y = move
            path = []

            while True:
                x += check_x
                y += check_y
                if not self.is_within_board((x, y)) or (x, y) in self.board[player_color]:
                    break
                if (x, y) in self.board[opponent_color]:
                    path.append((x, y))
                else:
                    path = []  # Clear path if an empty square or a player's own piece is found
                    break

            if self.is_within_board((x, y)) and (x, y) in self.board[player_color]:
                for p in path:
                    self.board[opponent_color].remove(p)
                    self.board[player_color].add(p)

    def print_board(self):
        """prints a human-readable description of the board using
           the characters in tile_type (below)"""
        for r in range(8,0,-1):
            print(r, end=" ")
            for c in range(1,9):
                print(self.tile_type((r, c)), end="")
            print('')
        print('  12345678')
    
    def tile_type(self, p):
        """determines the type of tile.
             O - white piece 
             # - black piece
             . - unoccupied space
        """
        if p in self.board['white']:
            return 'O'
        elif p in self.board['black']:
            return '#'
        else:
            return '.'
    
    def occupied(self, p):
        """determines if a player's piece occupies this tile or not"""
        c = self.tile_type(p)
        return c != '.'          
    
    def isLeaf(self):
        """returns true of this is a leaf node"""
        # turn would have already been skipped if only one player had no moves
        return not list(self.legal_moves())

        
    def legal_moves(self):
        """determines all legal moves from this game state"""
        legal_moves = []
        for row in range(1, 9):
            for col in range(1, 9):
                if not self.occupied((row, col)):  # Check if the tile is empty
                    if self.is_move_legal((row, col)):
                        legal_moves.append((row, col))
        return legal_moves

    def is_move_legal(self, move):
        """Determines if a move is legal from the current game state."""
        player_color = 'white' if self.isMax else 'black'
        opponent_color = 'black' if self.isMax else 'white'

        directions = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1),   # right
            (-1, -1), # up-left
            (-1, 1),  # up-right
            (1, -1),  # down-left
            (1, 1)    # down-right
        ]

        for check_x, check_y in directions:
            x, y = move
            x += check_x
            y += check_y
            if self.is_within_board((x, y)) and (x, y) in self.board[opponent_color]:
                while self.is_within_board((x, y)) and (x, y) in self.board[opponent_color]:
                    x += check_x
                    y += check_y
                if self.is_within_board((x, y)) and (x, y) in self.board[player_color]:
                    return True
        return False

    def is_within_board(self, position):
        """Checks if a position is within the board."""
        row, col = position
        check = 1 <= row <= 8 and 1 <= col <= 8
        return check

    def children(self):
        """computes child nodes for this node"""
        child_nodes = []
        for move in self.legal_moves():
            child_nodes.append(Reversi(self.isMax, move, self.prior_moves, self.board))
        return child_nodes
    

    def evaluate(self):
        """heuristic that returns a value between -1 and 1"""
        # Count the number of pieces for each player
        white_count = len(self.board['white'])
        black_count = len(self.board['black'])

        # Game over condition
        if self.isLeaf():
            if white_count > black_count:
                return 1  # White wins
            elif black_count > white_count:
                return -1  # Black wins
            else:
                return 0  # Draw

        # Heuristic for states
        total_pieces = white_count + black_count
        return (white_count - black_count) / total_pieces

def main():
    c = GameClient(Reversi, None, None) # human vs human
    #c = GameClient(Reversi, None, Reversi) # human vs AI
    #c = GameClient(Reversi, Reversi, Reversi) # AI vs AI
    c.run_game()
    
if __name__ == '__main__':
    main()

