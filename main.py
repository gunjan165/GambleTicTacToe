import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy_board import Board,GameScreen


class TicTacToe(App):
    
    def build(self):
        self.game  = GameScreen()
        return self.game


if __name__ == '__main__':
    TicTacToe().run()
