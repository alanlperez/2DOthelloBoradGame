import tkinter
import othello_game_logic
import point

DEFAULT_FONT = ('Helvetica', 14)

class OthelloApplication:
    def __init__(self,rows, columns, player_one,top_left_player, rules):
        self._not_root_window = tkinter.Toplevel()

        
        self.rows = int(rows)
        self.columns = int(columns)
        player_one = player_one
        top_left_player = top_left_player
        self._rules = rules

        self._game = othello_game_logic.GameState(self.rows, self.columns, player_one, top_left_player)
        self._gui_board = self._game.board()

        self._turn_text = tkinter.StringVar()
        self._turn_text.set(self._turn_or_win())

        turn = tkinter.Label(master = self._not_root_window, textvariable = self._turn_text)

        turn.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tkinter.N +
                  tkinter.S + tkinter.W + tkinter.E)

        self._canvas = tkinter.Canvas(master = self._not_root_window, width = 500, height = 400,
                                      background = '#00FF00')

        self._canvas.grid(row = 1, column = 0, sticky = tkinter.N + tkinter.S +tkinter.W +
                          tkinter.E)

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        

        self._not_root_window.rowconfigure(0, weight = 0)
        self._not_root_window.rowconfigure(1, weight = 1)
        self._not_root_window.columnconfigure(0, weight = 1)



    def start(self) -> None:
        '''activates GUI and hands over control to tkinter'''
        self._not_root_window.mainloop()
    
    def show(self) -> None:
        self._not_root_window.grab_set()
        self._not_root_window.wait_window()
                

    def _turn_or_win(self) -> str:
        '''returns string describing whose turn/win it is'''

        self._game.look_for_tiles()
        self._game.look_for_valid_moves()
        L = list(self._game.show_score())

        if not self._game.game_over():
            text = 'Rules: FULL, B: {} W: {},  {}\'s Turn'.format(L[0], L[1], self._game._turn)

        if self._game.game_over() == True:
            self._game._opposite_turn()
            self._game.look_for_valid_moves()
            text = 'Rules: FULL, B: {} W: {},  {}\'s Turn'.format(L[0], L[1], self._game._turn)
            

        if self._rules == '>':
            if self._game.game_over() == True:
                winner = self._game.most_points_wins()
                text = 'Rules: FULL, B: {} W: {},  WINNER: {}'.format(L[0], L[1], winner)
                
        elif self._rules == '<':
            if self._game.game_over() == True:
                winner = self._game.least_points_wins()
                text = 'Rules: FULL, B: {} W: {},  WINNER: {}'.format(L[0], L[1], winner)
        return text
        
                 

    def _get_canvas_dimensions(self) -> (int, int):
        '''return current width and height of the canvas'''
        return self._canvas.winfo_width(), self._canvas.winfo_height()

    def _on_canvas_clicked(self, event:tkinter.Event) -> None:
        '''
        generates a event.x and event.y coordinate to determine where
        the click occured and then calls the appropriate functions to redraw
        the board with the letter created by the click if the move is legal
        '''
        
        width, height = self._get_canvas_dimensions()

        click_point = point.from_pixel(
            (event.x, event.y), (width, height))

        self._handle_click(click_point)
        self._turn_text.set(self._turn_or_win())

        self._draw_board()

    def _handle_click(self, click_point: point.Point) -> None:
        '''runs functions to determine if a valid tictactoe move '''
        try:
            self._game.check_if_in_valid_moves(self._get_square(click_point)[0],self._get_square(click_point)[1])

            self._game.check_eight_sides(self._get_square(click_point)[0],self._get_square(click_point)[1])
            self._game.flip_tile()
            if not self._game.game_over():
                self._game._opposite_turn()

        except:
            pass
            

    def _get_square(self, click_point: point.Point) -> (int, int):
        '''returns row and column of the board where board was clicked'''
        point_x, point_y = click_point.frac()

        for n in range(self.columns):
            upper_col = (n + 1) / self.columns
            lower_col = n / self.columns

      

            if lower_col < point_x < upper_col:
                click_col = n

        for n in range(self.rows):
            upper_row = (n + 1) / self.rows
            lower_row = n / self.rows

            if lower_row < point_y < upper_row:
                click_row = n
        


        return (click_row, click_col)

    def _on_canvas_resized(self, event:tkinter.Event) -> None:
        self._draw_board()

    def _draw_board(self) -> None:
        '''draw the current board'''
        self._canvas.delete(tkinter.ALL)

        width, height = self._get_canvas_dimensions()

        self._draw_grid(width, height)
        self._draw_letters(width, height)

    def _draw_grid(self, canvas_width, canvas_height) -> None:
        '''draws the grid created by dividing the canvas into rows/columns'''
        for row in range(self.rows - 1):
            self._canvas.create_line(
                0, (canvas_height * ((1 + row) / self.rows )),
                canvas_width, (canvas_height * (( 1 + row)) / self.rows))

        for col in range(self.columns -1):
            self._canvas.create_line(
                (canvas_width * ((1 + col) / self.columns)), 0,
                (canvas_width * ((1 + col) / self.columns)), canvas_height)

    def _draw_letters(self, canvas_width, canvas_height) -> None:
        '''draws any letters currently on the board'''
        self._gui_board  = self._game._board
        for row in range(self.rows):
            for col in range(self.columns):
                if self._gui_board[row][col] == 'B':
                    self._canvas.create_oval(
                        (canvas_width * ((col) / self.columns)), (canvas_height * (row / self.rows)),
                        (canvas_width * ((1 + col) / self.columns)), (canvas_height * ((row + 1)/ self.rows)),
                        fill = 'black', outline = 'black')

                elif self._gui_board[row][col] == 'W':
                    self._canvas.create_oval(
                        (canvas_width * ((col) / self.columns)), (canvas_height * (row / self.rows)),
                        (canvas_width * ((1 + col)/self.columns)), (canvas_height * ((row + 1)/self.rows)),
                        fill = 'white', outline = 'white')

            
            
            
            
    
            


class NameDialog:
    def __init__(self):
        self._dialog_window = tkinter.Toplevel()

        self._who_text = tkinter.StringVar()

        self._who_text.set('Please Enter The Following information:')

        who_label = tkinter.Label(
            master = self._dialog_window, textvariable = self._who_text,
            font = DEFAULT_FONT)

        who_label.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
                       sticky = tkinter.W)





        rows_label = tkinter.Label(master = self._dialog_window, text = 'Rows:',
                                         font = DEFAULT_FONT)

        rows_label.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = tkinter.W)

        optionList = ['4', '6', '8', '10', '12', '14', '16']

        self._rows_var = tkinter.StringVar()

        self._rows_entry = tkinter.OptionMenu(self._dialog_window,self._rows_var, *optionList)

        self._rows_var.set(optionList[0])


        self._rows_entry.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = tkinter.W +
                                    tkinter.E)





        columns_label = tkinter.Label(master = self._dialog_window, text = 'Columns:',
                                        font = DEFAULT_FONT)
        columns_label.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = tkinter.W)
        
        second_optionsList = ['4', '6', '8', '10', '12', '14', '16']

        self._columns_var = tkinter.StringVar()

        self._columns_entry = tkinter.OptionMenu(self._dialog_window,self._columns_var, *second_optionsList)

        self._columns_var.set(second_optionsList[0])

        self._columns_entry.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = tkinter.W +
                                   tkinter.E)




        player_one_label = tkinter.Label(master = self._dialog_window, text = 'Player One "Black: B or White: W":',
                                        font = DEFAULT_FONT)
        player_one_label.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = tkinter.W)

        third_optionsList = ['B', 'W']
        
        self._player_one_var = tkinter.StringVar()

        self._player_one_entry = tkinter.OptionMenu(self._dialog_window,self._player_one_var, *third_optionsList)

        self._player_one_var.set(third_optionsList[0])

        self._player_one_entry.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = tkinter.W +
                                   tkinter.E)





        top_left_label = tkinter.Label(master = self._dialog_window, text = 'Top Left Player "Black: B or White: W":',
                                        font = DEFAULT_FONT)
        top_left_label.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = tkinter.W)

        fourth_optionsList = ['B', 'W']
        
        self._top_left_player_var = tkinter.StringVar()

        self._top_left_player_entry = tkinter.OptionMenu(self._dialog_window,self._top_left_player_var, *fourth_optionsList)

        self._top_left_player_var.set(fourth_optionsList[0])


        self._top_left_player_entry.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = tkinter.W +
                                   tkinter.E)







        rules_label = tkinter.Label(master = self._dialog_window, text = 'Most ">" or Least "<" Pieces Wins:',
                                        font = DEFAULT_FONT)
        rules_label.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = tkinter.W)

        fifth_optionsList = ['>', '<']
        
        self._rules_var = tkinter.StringVar()

        self._rules_entry = tkinter.OptionMenu(self._dialog_window,self._rules_var, *fifth_optionsList)

        self._rules_var.set(fifth_optionsList[0])        
        
        self._rules_entry.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = tkinter.W +
                                   tkinter.E)





      

        button_frame = tkinter.Frame(master = self._dialog_window)

        button_frame.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
                          sticky = tkinter.E +tkinter.S)

        ok_button = tkinter.Button(master = button_frame, text = 'OK', font = DEFAULT_FONT,
                                   command = self._on_ok_button)

        ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
                                       command = self._on_cancel_button)

        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        self._dialog_window.rowconfigure(3, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)

        self._ok_clicked = False
        self._rows = 0
        self._columns = 0
        self._player_one = ''
        self._top_left_player = ''
        self._rules = ''



    def show(self) -> None:
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()


    def was_ok_clicked(self) -> bool:
        return self._ok_clicked

    def get_rows(self) -> int:
        return self._rows

    def get_columns(self) -> int:
        return self._columns

    def get_player_one(self) -> str:
        return self._player_one

    def get_top_left_player(self) -> str:
        return self._top_left_player

    def get_rules(self) -> str:
        return self._rules

    

    def _on_ok_button(self) -> None:
        self._ok_clicked = True

        self._rows = self._rows_var.get()
        self._columns = self._columns_var.get()
        self._player_one = self._player_one_var.get()
        self._top_left_player = self._top_left_player_var.get()
        self._rules = self._rules_var.get()

        
        self._dialog_window.destroy()


    def _on_cancel_button(self) -> None:
        self._dialog_window.destroy()

class GreetingsApplication:
    def __init__(self):
        self._root_window = tkinter.Tk()

        greet_button = tkinter.Button(master = self._root_window, text = 'Play',
                                      font = DEFAULT_FONT, command = self._on_greet)

        greet_button.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tkinter.S)

        self._greeting_text = tkinter.StringVar()
        self._greeting_text.set('Press The Play Button To Start!')

        greeting_label = tkinter.Label(master = self._root_window, textvariable =
                                       self._greeting_text, font = DEFAULT_FONT)

        greeting_label.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = tkinter.N)

        self._root_window.rowconfigure(0, weight = 1)

    def start(self) -> None:
        self._root_window.mainloop()

    def _on_greet(self) -> None:
        dialog = NameDialog()

        dialog.show()



        if dialog.was_ok_clicked():

            rows = dialog.get_rows()
            columns = dialog.get_columns()
            player_one = dialog.get_player_one()
            top_left_player = dialog.get_top_left_player()
            rules = dialog.get_rules()
            self._greeting_text.set('Thanks For Playing! Want to play again?')

            OthelloApp = OthelloApplication(rows, columns, player_one, top_left_player, rules)

            OthelloApp.start()

            

if __name__ == '__main__':
    GreetingsApplication().start()


        
