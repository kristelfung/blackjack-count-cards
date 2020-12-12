from tkinter import *
import random
from Deck import Deck

class Table:
  """
  Table class 

  Attributes:
    shoe: list of cards in the form [['A', 3, 'A♠'], ['A', 2, 'A♥'], ...]
    count: current running count
    shoe_size: default number of cards in the shoe
    num_decks: number of decks in the shoe
  """

  def __init__(self, num_decks):
    self.shoe = []
    self.count = 0
    self.shoe_size = num_decks * 52
    self.num_decks = num_decks
    for deck in range(num_decks):
      d = Deck()
      self.shoe += d.cards
    self.shuffle()
#    self.shoe.append([5, 0, '5♦'])
#    self.shoe.append([5, 0, '5♦'])
#    self.shoe.append([5, 0, '5♦'])
#    self.shoe.append([5, 0, '5♦'])
    
    self.label_rc = Label(text="Running Count is " + str(self.count))
    self.label_rc.pack()
    self.label_tc = Label(text="True Count is " + str(self.count / 4))
    self.label_tc.pack()

  def shuffle(self):
    """ Shuffles the shoe. """
    random.shuffle(self.shoe)

  def deal_cards(self, dealer, player):
    """ Deals cards to Dealer and Player. """
    dealer.init_cards([self.shoe.pop(), self.shoe.pop()], player)
    player.init_cards([self.shoe.pop(), self.shoe.pop()])
    self.update_count(player.hand.cards)
    self.update_count([dealer.hand.cards[0]])

  def deal_one_card(self, hand):
    """ Deals one card (used for Player hit). """
    card_hand = [self.shoe.pop()]
    hand.receive_cards(card_hand)
    self.update_count(card_hand)

  def update_count(self, cards):
    """ Updates count of the Table based on cards and updates count Labels. """
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
    """ Checks if we need to reshuffle shoe, and reshuffles if 1/3 cards
    have been used. """
    if len(self.shoe) < self.shoe_size // 3:
      print("1/3 cards used up; reshuffling shoe.")
      self.count = 0
      self.shoe = []
      for deck in range(self.num_decks):
        d = Deck()
        self.shoe += d.cards
      self.shuffle()
      self.update_count([])
