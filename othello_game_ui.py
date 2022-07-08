import othello_game_logic


def get_user_outputs() -> list:
    '''TAKES WHAT THE USER WANTS TO GENERATE'''
    List = []
    value = 0
    while (value != 5):
        List.append(input())
        value += 1
    return List


def ask_for_move() -> 'move':
    '''Takes user input for moves they want on the board'''
    while True:
        try:
            f = input()
            f = f.split(' ')
            if len(f) != 2:
                raise SyntaxError
            else:
                game_state.check_if_in_valid_moves(int(f[0])-1, int(f[1])-1)
            print('VALID')
            return (int(f[0]), int(f[1]))
        except:
            print('INVALID')





def format_game_board(b: [list]) -> None:
        ''' Prints game board out. '''
        L = list(game_state.show_score())
        print ('B: {} W: {}'.format(L[0], L[1]))
        for row in range(game_state._rows):
            for col in range(game_state._columns):
                if game_state._board[row][col] == '':
                    print('. ', sep=' ', end='')
                elif game_state._board[row][col] == 'B':
                    print('B ', sep=' ', end='')
                elif game_state._board[row][col] == 'W':
                    print('W ', sep=' ', end='')
                if col == game_state._columns-1:
                    print()
    

    
        

if __name__ == '__main__':
        
    print('FULL')
    L = get_user_outputs()
    game_state = othello_game_logic.GameState(int(L[0]),int(L[1]),L[2],L[3],)
    win_method = L[4]
    current_board = game_state.board()
    print(game_state._board)
    while True:
        game_state._valid_moves_list = []
        game_state.List = []
        game_state.look_for_tiles_list = []
        format_game_board(game_state._copy_game_board(current_board))
        game_state.look_for_tiles()
        game_state.look_for_valid_moves()

        if game_state.game_over() == True:
            game_state._opposite_turn()
            game_state.look_for_valid_moves()

        if win_method == '>':
            if game_state.game_over() == True:
                game_state._copy_game_board(current_board)
                winner = game_state.most_points_wins()
                print('WINNER: {}'.format(winner))
                break
        elif win_method == '<':
            if game_state.game_over() == True:
                game_state._copy_game_board(current_board)
                winner = game_state.least_points_wins()
                print('WINNER: {}'.format(winner))
                break 
        
        print('TURN: {}'.format(game_state._turn))

        P = ask_for_move()
        game_state.check_eight_sides(P[0]-1,P[1]-1)
        game_state.flip_tile()
        current_board = game_state._board
        current_board
        game_state._opposite_turn()

