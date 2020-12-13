import tkinter as tk
from Hand import Hand

class Dealer:
  """
  Dealer class

  Attributes:
    hand: Hand class representing dealer's hand
  """
  def __init__(self, dealer_frame):
    self.dealer_frame = dealer_frame
    self.hand = None

  def init_cards(self, hand, player):
    """ Receives an initial hand frmo the table. Evaluates to see if Dealer
    has natural, and if Player can buy insurance."""
    self.hand = Hand(hand)
    
    if self.hand.value == 21:
      self.hand.natural = True
    if self.hand.cards[0][0] == "A":
      player.can_insurance = True
    
    self.label_cards = tk.Label(self.dealer_frame, text=self.hand.cards[0][2] + "[Hidden]")
    self.label_cards.pack()

  def play(self, table, action_frame):
    self.label_dealer_hits = tk.Label(action_frame)
    self.label_dealer_hits.pack()
    self.label_cards.config(text=self.hand)
    table.update_count([self.hand.cards[1]]) # Card overturned
    hits = 0
    while self.hand.value < 17:
      table.deal_one_card(self.hand)
      self.label_cards.config(text=self.hand)
      hits += 1
    self.label_dealer_hits.config(text="Dealer hits " + str(hits) + " times.")

  def reset(self):
    self.hand = None
