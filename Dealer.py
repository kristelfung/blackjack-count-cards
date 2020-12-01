from tkinter import *
from Hand import Hand

class Dealer:
  """
  Dealer class

  Attributes:
    hand: Hand class representing dealer's hand
  """
  def __init__(self):
    self.hand = None

  def init_cards(self, hand, player):
    """ Receives an initial hand frmo the table. Evaluates to see if Dealer
    has natural, and if Player can buy insurance."""
    self.hand = Hand(hand)
    
    if self.hand.value == 21:
      self.hand.natural = True
    if self.hand.cards[0][0] == "A":
      player.can_insurance = True
    
    self.label_cards = Label(text=self.hand.cards[0][2] + "[Hidden]")
    self.label_cards.pack()

  def print_one_card(self):
    print("Dealer's hand: ")
    self.hand.print_one()

  def print_hand(self):
    print("Dealer's hand: ")
    print(self.hand)

  def play(self, table):
    self.print_hand()
    while self.hand.value < 17:
      print("Dealer hits.")
      table.deal_one_card(self.hand)
      self.print_hand()

  def reset(self):
    self.hand = None
