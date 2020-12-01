from tkinter import *
import random
from Deck import Deck

class Table:
  """
  Table class 

  Attributes:
    shoe: list of cards in the form [['A', 1, 'A♠'], ['A', 2, 'A♥'], ...]
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

  def shuffle(self):
    random.shuffle(self.shoe)

  def deal(self, dealer, player):
    dealer.init_cards([self.shoe.pop(), self.shoe.pop()])
    player.init_cards([self.shoe.pop(), self.shoe.pop()])

  def deal_one_card(self, hand):
    card_hand = [self.shoe.pop()]
    hand.receive_cards(card_hand)

  def calculate_count(self, cards):
    low = [2, 3, 4, 5, 6] # +1
    high = [10, "J", "Q", "K", "A"] # -1
    for card in cards:
      if card[0] in low:
        self.count += 1
      elif card[0] in high:
        self.count -= 1

  def check_shoe_size(self):
    if len(self.shoe) < self.shoe_size // 3:
      print("1/3 cards used up; reshuffling shoe.")
      self.count = 0
      self.shoe = []
      for deck in range(self.num_decks):
        d = Deck()
        self.shoe += d.cards
      self.shuffle()

  def display_count(self):
    rc = Label(text="Running Count is " + str(self.count))
    rc.pack()
    tc = Label(text="True Count is " + str(self.count / 4))
    tc.pack()
