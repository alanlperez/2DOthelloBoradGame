import othello_game_ui

class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass


class GameOverError(Exception):
    '''
    Raised whenever an attempt is made to make a move after the game is
    already over
    '''
    pass


class GameState:
    def __init__(self, rows: int, columns: int, player_one: str, top_left: str):
        '''column, board turn, winner, color, move'''
        self._rows = rows
        self._columns = columns
        self._top_left = top_left
        self._bopposite = 'W'
        self._wopposite = 'B'
#        self._board = None
        self._board = []
        self._directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (-1, -1), (1, 1), (1, -1)]
        self._directions_2 = []
        self._turn = player_one
        self._x_coord = None
        self._y_coord = None
        self._x_coordinate = None
        self._y_coordinate = None
        self._valid_moves_list = []
        self.piece_flip_list = []
        self.adjacent_list = []
        self.List = []
        self.a = 0
        self.b = 0
        self.look_for_tiles_list = []


    
    def board(self) -> [list]:
        'Creates the Board'
 #       self._board = []
        if self._top_left == 'W':

            for row in range(self._rows):
                self._board.append([])
                for col in range(self._columns):
                    self._board[-1].append('')
            self._board[int(self._rows/2) - 1][int(self._columns/2)-1] = 'W'
            self._board[int(self._rows/2)-1][int(self._columns/2)] = 'B'
            self._board[int(self._rows/2)][int(self._columns/2)-1] = 'B'
            self._board[int(self._rows/2)][int(self._columns/2)] = 'W'

        elif self._top_left == 'B':
            for col in range(self._rows):
                self._board.append([])
                for row in range(self._columns):
                    self._board[-1].append('')
            self._board[int(self._rows/2) - 1][int(self._columns/2)-1] = 'B'
            self._board[int(self._rows/2)-1][int(self._columns/2)] = 'W'
            self._board[int(self._rows/2)][int(self._columns/2)-1] = 'W'
            self._board[int(self._rows/2)][int(self._columns/2)] = 'B'
            
        return self._board

    def _copy_game_board(self, board: [[str]]) -> [[str]]:
        'Makes a copy of the board'
        board_copy = []
        for row in range(self._rows):
            board_copy.append([])
            for col in range(self._columns):
                board_copy[-1].append(board[row][col])
        return board_copy


    def _opposite_turn(self) -> str:
        '''switches whose turn it is'''
        if self._turn == 'B':
            self._turn = 'W'
            return self._turn
        elif self._turn == 'W':
            self._turn = 'B'
            return self._turn

    def _other_player(self)-> str:
        '''opposite of who the current player is'''
        if self._turn == 'B':
            return 'W'
        elif self._turn == 'W':
            return 'B'

    def current_player(self) -> str:
        return self._turn
    









    def check_eight_sides(self, x, y):
        '''Takes in the coordinates of piece being placed, checks all eight sides.
        Keeps heading in that direction until it hits the end of the board, an empty space, or another piece.
        If it hits the same colored piece it returns to its original position appending all other pieces along the way'''
        other_tile = self._other_player()
        self.adjacent_list = []

        for direction_for_x, direction_for_y in self._directions:
            self._x_coord = x + direction_for_x
            self._y_coord = y + direction_for_y
            if self._is_valid_row_and_column_number(self._x_coord, self._y_coord) and self._board[self._x_coord][self._y_coord] == other_tile:

               while self._board[self._x_coord][self._y_coord] == other_tile:
                   
                   self._x_coord = self._x_coord + direction_for_x
                   self._y_coord = self._y_coord + direction_for_y

                   if self._is_valid_row_and_column_number(self._x_coord, self._y_coord):

                       if self._board[self._x_coord][self._y_coord] != '': 

                           if self._is_valid_row_and_column_number(self._x_coord, self._y_coord):
                               if self._board[self._x_coord][self._y_coord] == self._turn:
                               
                                   while self._board[self._x_coord][self._y_coord] != self._board[x][y]:
                                       self._x_coord = self._x_coord - direction_for_x
                                       self._y_coord = self._y_coord - direction_for_y
                                       self.adjacent_list.append((self._x_coord, self._y_coord))
                                       self.adjacent_list.append((x,y))
                                       

                   else:
                       break
        return self.adjacent_list




    def flip_tile(self):
        '''flips the tiles saved on attribute list'''
        for tiles in self.adjacent_list:
            if len(self.adjacent_list) == 0:
                raise InvalidMoveError
            else:
                self._board[tiles[0]][tiles[1]] = self._turn
        return self._board

    

        

    def look_for_tiles(self):
        '''checks for any open spaces on the board'''
        self.look_for_tiles_list = []
        for row in range(self._rows):
            for col in range(self._columns):
                if self._board[row][col] == '':
                    self.look_for_tiles_list.append((row,col))



    def look_for_valid_moves(self):
        '''checks for any valid open spaces on the board'''
        other_tile = self._other_player()
        self._valid_moves_list = []
        for direction_for_x, direction_for_y in self._directions:
            for tiles in self.look_for_tiles_list:
                self._x_coordinate = tiles[0] + direction_for_x
                self._y_coordinate = tiles[1] + direction_for_y
                if self._is_valid_row_and_column_number(self._x_coordinate, self._y_coordinate) and self._board[self._x_coordinate][self._y_coordinate] == other_tile and self._board[self._x_coordinate][self._y_coordinate] != '':
                   while self._board[self._x_coordinate][self._y_coordinate] == other_tile:
                       
                       self._x_coordinate = self._x_coordinate + direction_for_x
                       self._y_coordinate = self._y_coordinate + direction_for_y

                       if self._is_valid_row_and_column_number(self._x_coordinate, self._y_coordinate):

                           if self._board[self._x_coordinate][self._y_coordinate] == self._turn: 
                               self._valid_moves_list.append((tiles[0],tiles[1]))

                       else:
                           break

        
        

    def check_if_in_valid_moves(self, x, y):
        '''checks if user input is placed on an open space on the board'''
        a = (x,y)
        if a in self._valid_moves_list:
            return True
        else:
            raise InvalidMoveError
        
    


    def show_score(self) -> 'score':
        '''shows the score of the game'''
        black_score = 0
        white_score = 0
        for List in self._board:
            for pieces in List:
                if pieces == 'B':
                    black_score += 1
                elif pieces == 'W':
                    white_score += 1
        return (black_score, white_score)

    def most_points_wins(self) -> 'winner':
        '''determines if the rules is most tiles on the board wins'''
        winner = None
        if self.game_over():
            if self.show_score()[0] > self.show_score()[1]:
                winner = self._wopposite
            elif self.show_score()[1] > self.show_score()[0]:
                winner = self._bopposite
            else:
                winner = 'NONE'
        return winner


    def least_points_wins(self) -> 'winner':
        '''determines if the rules is least tiles on the board wins'''
        winner = None
        if self.game_over():
            if self.show_score()[1] > self.show_score()[0]:
                winner = self._wopposite
            elif self.show_score()[0] > self.show_score()[1]:
                winner = self._bopposite
            else:
                winner = 'NONE'
        return winner


    def game_over(self):
        '''checks if the game is over'''
        return len(self._valid_moves_list) == 0
        

    


    def _is_valid_row_and_column_number(self, row_number: int, column_numbers: int) -> bool:
        '''checks if a position is on the board'''
        return 0 <= column_numbers < self._columns and 0 <= row_number < self._rows
        

class InvalidMoveError(Exception):
    pass
    

