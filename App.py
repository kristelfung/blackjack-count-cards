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
    """ Initializes Table with 4 decks, Player, and Dealer.
    Create Start and Quit button. """
    self.table = Table(num_decks=4)
    self.player = Player(self.master)
    self.dealer = Dealer()
    
    self.start_button = Button(self, text="Start (S)", command=self.start)
    self.start_button.pack()
    self.quit_button = Button(self, text="Quit (Q)", command=self.quit)
    self.quit_button.pack()
  
  def start(self):
    """ Begins game. """
    self.start_button.destroy()
    self.play_round()
  
  def play_round(self):
    """ Handles an entire round between Player and Dealer. """
    self.table.check_shoe_size()
    self.table.display_count()
    self.player.ask_bet()
    self.deal_cards()
    self.evaluate_deal()
    self.player_turn()
    
  def deal_cards(self):
    """ Deals and displays cards. """
    self.table.deal(self.dealer, self.player)
    print(self.player.hand)
    self.label_playercards = Label(text=self.player.hand)
    self.label_playercards.pack()
    self.label_dealercards = Label(text=self.dealer.hand.cards[0][2] + "[Hidden]")
    self.label_dealercards.pack()
    
  def evaluate_deal(self):
    """ Checks if Player or Dealer has naturals, and checks if Player
    can double down / split pairs / insurance. Update count of Table."""
    if self.player.hand.value == 21:
      self.player.hand.natural = True
    if self.dealer.hand.value == 21:
      self.dealer.hand.natural = True
    if self.player.hand.value == 9 or self.player.hand.value == 10 or self.player.hand.value == 11:
      self.player.can_double_down = True
    if self.player.hand.cards[0][0] == self.player.hand.cards[1][0]:
      self.player.can_split_pairs = True
    if self.dealer.hand.cards[0][0] == "A":
      self.player.can_insurance = True
    self.table.calculate_count(self.player.hand.cards)
    self.table.calculate_count([self.dealer.hand.cards[0]])
    self.table.update_count()
  
  def player_turn(self):
    print("player turn")
  
  def quit(self):
    self.master.destroy()
