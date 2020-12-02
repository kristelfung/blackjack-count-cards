from tkinter import *
from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table

class App(Frame):
  def __init__(self, master=None):
    super(App, self).__init__(master)
    self.initGame()
  
  def initGame(self):
    """ Create Start and Quit button. """
    self.start_button = Button(self, text="Start (S)", command=self.start)
    self.start_button.pack()
    self.quit_button = Button(self, text="Quit (Q)", command=self.quit)
    self.quit_button.pack()
  
  def start(self):
    """ Begins game. Initializes Table with 4 decks, Player, and Dealer. """
    self.start_button.destroy()
    self.table = Table(num_decks=4)
    self.player = Player(self.master)
    self.dealer = Dealer()
    self.play_round()
  
  def play_round(self):
    """ Handles an entire round between Player and Dealer. """
    self.table.check_shoe_size()
    self.player.ask_bet()
    self.deal_cards()
    if not self.player.hand.natural:
      self.player.play(self.table)
    if not self.player.is_bust():
      self.dealer.play(self.table)
      # DO COMPARISON
    else:
      print("Player lost")
    # Play again?
    
  def deal_cards(self):
    """ Deals cards to Dealer and Player. """
    print("dealing")
    self.table.deal(self.dealer, self.player)
    self.table.calculate_count(self.player.hand.cards)
    self.table.calculate_count([self.dealer.hand.cards[0]])
    self.table.update_count()
  
  def quit(self):
    self.master.destroy()
