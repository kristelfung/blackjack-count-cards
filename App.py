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
      self.player_turn()
    
  def deal_cards(self):
    """ Deals cards to Dealer and Player. """
    self.table.deal(self.dealer, self.player)
    self.table.calculate_count(self.player.hand.cards)
    self.table.calculate_count([self.dealer.hand.cards[0]])
    self.table.update_count()
  
  def player_turn(self):
    """ Asks for double down / split pairs / insurance if applicable, and
    plays round accordingly. """
    def double_down_wrapper(buttons, table):
      for btn in buttons:
        btn.destroy()
      self.player.double_down(table)
    
    def insurance_wrapper(buttons, table):
      for btn in buttons:
        btn.destroy()
      self.player.ask_insurance(table)
    
    def split_pairs_wrapper(buttons, table):
      for btn in buttons:
        btn.destroy()
      self.player.split_pairs(table)
    
    def play_hand_wrapper(buttons, table, hand):
      for btn in buttons:
        btn.destroy()
      self.player.play_hand(table, hand)
    
    if (self.player.can_double_down or self.player.can_insurance
        or self.player.can_split_pairs):
      buttons = []
      if self.player.can_double_down:
        dd_button = Button(self, text="Double Down (D)", command= lambda: double_down_wrapper(buttons, self.table))
        buttons.append(dd_button)
        dd_button.pack()
      if self.player.can_insurance:
        button_ins = Button(self, text="Insurance (I)", command= lambda: insurance_wrapper(buttons, self.table))
        buttons.append(button_ins)
        button_ins.pack()
      if self.player.can_split_pairs:
        button_sp = Button(self, text="Split Pairs (S)", command= lambda: split_pairs_wrapper(buttons, self.table))
        buttons.append(button_sp)
        button_sp.pack()
      button_normal = Button(self, text="Normal Round (N)", command= lambda: play_hand_wrapper(buttons, self.table, self.player.hand))
      buttons.append(button_normal)
      button_normal.pack()
    else:
      self.player.play_hand(self.table, self.player.hand)
  
  def quit(self):
    self.master.destroy()
