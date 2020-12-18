import tkinter as tk
import random
from Deck import Deck
from PIL import ImageTk, Image

class Table:
  """
  Table class 

  Attributes:
    parent: the parent App class
    shoe: list of cards in the form [['A', 'AS'], ['A', 'AH'], ...]
    count: current running count
    shoe_size: default number of cards in the shoe
    num_decks: number of decks in the shoe
  """

  def __init__(self, parent, num_decks):
    """Initializes Table. Appends Decks to shoe, shuffles shoe and creates window
    displaying count."""
    self.parent = parent
    self.shoe = []
    self.count = 0
    self.shoe_size = num_decks * 52
    self.num_decks = num_decks
    for deck in range(num_decks):
      d = Deck()
      self.shoe += d.cards
    self.shuffle()
    
    self.create_window()
  
  def create_window(self):
    """Creates window for Table, displaying Running Count and True Count."""
    self.parent.status_frame.grid_columnconfigure((0), weight=1)
    self.parent.status_frame.grid_rowconfigure((0, 1), weight=1)
    
    self.label_rc = tk.Label(self.parent.status_frame, text="Running Count is " + str(self.count))
    self.label_rc.grid(row=0, column=0)
    self.label_tc = tk.Label(self.parent.status_frame, text="True Count is " + str(self.count / 4))
    self.label_tc.grid(row=1, column=0)
    
    self.parent.table_frame.grid_columnconfigure((0), weight=1)
    self.parent.table_frame.grid_rowconfigure((0), weight=1)
    
    self.label_deck = tk.Label(self.parent.table_frame, text="Shoe (" + str(len(self.shoe)) + ")")
    self.label_deck.grid(row=0, column=0)
    
    img = ImageTk.PhotoImage(Image.open("images/back.jpg").resize((70, 105)))
    self.label_deck_img = tk.Label(self.parent.table_frame, image=img)
    self.label_deck_img.photo = img
    self.label_deck_img.grid(row=1, column=0)
    
  def shuffle(self):
    """Shuffles the shoe."""
    random.shuffle(self.shoe)

  def deal_cards(self, dealer, player):
    """Deals cards to Dealer and Player."""
    dealer.init_cards([self.shoe.pop(), self.shoe.pop()], player)
    player.init_cards([self.shoe.pop(), self.shoe.pop()])
    self.update_count(player.hand.cards)
    self.update_count([dealer.hand.cards[0]])
    self.update_shoe_label()

  def deal_one_card(self, hand):
    """Deals one card (used for Player and Dealer hit)."""
    card_hand = [self.shoe.pop()]
    hand.receive_cards(card_hand)
    self.update_count(card_hand)
    self.update_shoe_label()

  def update_count(self, cards):
    """Updates count of the Table based on cards and updates count Labels."""
    low = [2, 3, 4, 5, 6] # +1
    high = [10, "J", "Q", "K", "A"] # -1
    for card in cards:
      if card[0] in low:
        self.count += 1
      elif card[0] in high:
        self.count -= 1
    self.label_rc.config(text="Running Count is " + str(self.count))
    self.label_tc.config(text="True Count is " + str(self.count / 4))

  def check_shoe_size(self):
    """Checks if we need to reshuffle shoe, and reshuffles if 1/3 cards
    have been used."""
    if len(self.shoe) < self.shoe_size // 3:
      self.count = 0
      self.shoe = []
      for deck in range(self.num_decks):
        d = Deck()
        self.shoe += d.cards
      self.shuffle()
      self.update_count([])
  
  def update_shoe_label(self):
    self.label_deck.config(text="Shoe (" + str(len(self.shoe)) + ")")
