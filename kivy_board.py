from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput

from player import Player

class Board(GridLayout):

    grid = None
    symbols = None
    can_mark = False
    def __init__(self, cols=3, **kwargs):

        super(Board, self).__init__(**kwargs)

        self.cols = cols
        self.rows = cols
        
        self.game_board = kwargs['game_board_obj']
        self.grid = [[None for col in range(self.cols)] for row in range(self.rows)]
        self._draw_tiles()


    def _draw_tiles(self):
        """
            Adds the tiles to the grid (widgets to the gridset)
        """
        for row in range(self.rows):
            for col in range(self.cols):
                tile = Button()
                tile.bind(on_press=self._onclick)
                self.grid[row][col] = tile
                self.add_widget(tile)
        
    def _onclick(self, instance):
        """
            Handles a click on a tile
        """
        if self.can_mark:

            if instance.text:
                return None

            instance.text = self.game_board.current_symbol

            self._check_status()
            self.can_mark = False
            self.game_board.reset_round()
            
        

    def _check_status(self):
        """
            Checks board status
        """
        winner = self._get_winner()

        if winner:
            close_button = Button(text='Close')

            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text='%s won the game!' % winner))
            content.add_widget(close_button)

            popup = Popup(title='%s won!' % winner,
                                content=content,
                                size_hint=(.8, .8)).open()

            #close_button.bind(on_release=popup.dismiss)

            self._restart_board()

    def _get_winner(self):
        """
            Returns winning symbol or None
        """

        values = [[col.text for col in row] for row in self.grid]

        # check horizontal
        for row in values:
            result = self._is_same_symbol(row)
            if result:
                return result

        # check vertical
        for row in [list(row) for row in zip(*values)]:
            result = self._is_same_symbol(row)
            if result:
                return result

        # check forward diagonal
        forward_diagonal = [row[col] for col, row in enumerate(values)]
        result = self._is_same_symbol(forward_diagonal)
        if result:
            return result

        # check backwards diagonal
        backwards_diagonal = [row[-col-1] for col, row in enumerate(values)]
        result = self._is_same_symbol(backwards_diagonal)
        if result:
            return result

        #if no coins left then the other player wins
        if self.game_board.player1.coins_left == 0:
            return self.game_board.player2.name
        
        if self.game_board.player2.coins_left == 0:
            return self.game_board.player1.name
        
        # if board is complete and no result => player with higher coins wins
        
        print values
        for row in values:
            for column in row:
                print column
                if column not in ['X', 'O']:
                    return None
        else:
            return self.game_board.player1.name if self.game_board.player1.coins_left > self.game_board.player2.coins_left else self.game_board.player2.name
        
        return None

    def _is_same_symbol(self, row):
        
        first_symbol = row[0]

        if first_symbol in ['X', 'O']:
            for symbol in row:
                if symbol !=  first_symbol:
                    return False
            else:
                return self.game_board.player1.name if first_symbol == 'X' else self.game_board.player2.name
        
        return False
        

    def _restart_board(self):
        for row in self.grid:
            for col in row:
                col.text = ''

class GameScreen(BoxLayout):


    def reset_round(self):

        self.current_player = self.player1
        self.player_label.text = self.current_player.name + " turn to play"
        self.coin_label.text = "You have " + str(self.current_player.coins_left) + " coins left to bet!" 
        self.coin_to_bet.text = 'Bet'

    def check_bet(self,*args):
        print "current bet " , self.current_bet
        print "player coins left " , self.current_player.coins_left

        if self.current_bet is not None and self.current_bet <= self.current_player.coins_left:
            self.bet_done.disabled = False
        else:
            self.bet_done.disabled = True
    
    def set_current_bet(self,*args):
        try:
            self.current_bet = int(args[-1])
        except:
            self.current_bet = None
        
        self.check_bet()

    def reduce_player_coins(self):
        self.current_player.coins_left -= self.current_bet
        self.current_player.last_bet = self.current_bet
    
    def check_bet_winner(self):
        self.coin_to_bet.text = 'Bet'
        if self.player1.last_bet > self.player2.last_bet:
            self.player_label.text = self.player1.name + "won the bet."
            self.coin_label.text = "Please place your mark"
            self.board.can_mark = True
            self.current_symbol = self.player1.symbol
        elif self.player2.last_bet > self.player1.last_bet:
            self.player_label.text = self.player2.name + "won the bet"
            self.coin_label.text = "Please place your mark"
            self.board.can_mark = True
            self.current_symbol = self.player2.symbol
        else:
            self.player1.coins_left += self.player1.last_bet
            self.player2.coins_left += self.player2.last_bet
            self.current_player = self.player1

            self.player_label.text = self.current_player.name + " turn to play"

    def complete_bet(self,*args):
        # deduct bet coins from current player coins
        self.reduce_player_coins()
        
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.player_label.text = self.current_player.name + " turn to play"
            self.coin_label.text =  'You have ' + str(self.current_player.coins_left) + ' coins left to bet!'
            self.coin_to_bet.text = 'Bet'
        else:

            self.check_bet_winner()
            

    def __init__(self, **kwargs):
        
        super(GameScreen, self).__init__()
        
        self.player1 = Player('Player 1', 'X')
        self.player2 = Player('Player 2', 'O')
        self.current_player = self.player1
        self.current_bet = None
        self.current_symbol = None
        self.board = Board(cols=3, game_board_obj = self)

        self.add_widget(self.board)
        
        info_box = BoxLayout(orientation = 'vertical',size_hint = (0.35,0.35))
        self.player_label = Label(text = '%s turn to play!'%self.current_player.name)
        self.coin_label = Label(text = 'You have %s coins left to bet!'% self.current_player.coins_left)
        self.coin_to_bet = TextInput(text='Bet', multiline = False)
        self.coin_to_bet.bind(text = self.set_current_bet)
        self.bet_done = Button(text = 'Confirm Bet!', disabled = True)
        self.bet_done.bind(on_press = self.complete_bet)
        info_box.add_widget(self.player_label)
        info_box.add_widget(self.coin_label)
        info_box.add_widget(self.coin_to_bet)
        info_box.add_widget(self.bet_done)
        self.add_widget(info_box)




