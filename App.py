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
    # Initialize Table with 4 Decks, Player and Dealer
    self.table = Table(num_decks=4)
    self.player = Player(self.master)
    self.dealer = Dealer()
    
    self.start_button = Button(self, text="Start (S)", command=self.start)
    self.start_button.pack()
    self.quit_button = Button(self, text="Quit (Q)", command=self.quit)
    self.quit_button.pack()
  
  def start(self):
    self.start_button.destroy()
    self.play_round()
  
  def play_round(self):
    self.table.check_shoe_size()
    self.table.display_count()
    self.player.ask_bet()
    self.deal_cards()
    self.player_turn()
    
  def deal_cards(self):
    self.table.deal(self.dealer, self.player)
    self.label_playercards = Label(text=self.player.hand)
    self.label_playercards.pack()
    self.label_dealercards = Label(text=self.dealer.hand.cards[0])
    self.label_dealercards.pack()
    
  
  def player_turn(self):
    print("player turn")
  
  def quit(self):
    self.master.destroy()
